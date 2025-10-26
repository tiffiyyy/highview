import json, os, boto3, base64
from botocore.exceptions import ClientError
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import response, cors_headers, now_iso, normalize_email, make_student_id

dynamodb = boto3.client(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id=os.getenv("key_id"),
    aws_secret_access_key=os.getenv("access_key")
)

# robust body parser (accepts string, dict, base64)
def parse_body(event):
    b = event.get("body")
    if b is None:
        return {}
    if event.get("isBase64Encoded"):
        if isinstance(b, str):
            b = base64.b64decode(b.encode("utf-8")).decode("utf-8")
        else:
            b = base64.b64decode(b).decode("utf-8")
    if isinstance(b, str):
        return json.loads(b or "{}")
    if isinstance(b, (bytes, bytearray)):
        return json.loads(b.decode("utf-8"))
    if isinstance(b, dict):
        return b
    return {}

def handler(event, context):
    # --- CORS preflight ---
    method = (event.get("requestContext", {}).get("http", {}).get("method")
              or event.get("httpMethod", "GET"))
    if method == "OPTIONS":
        return {"statusCode": 204, "headers": cors_headers(), "body": ""}

    # Parse body
    try:
        body = parse_body(event)
    except Exception:
        return response(400, {"message": "Invalid JSON body"})

    required = ("session_id", "first_name", "last_name", "email")
    missing = [k for k in required if not body.get(k)]
    if missing:
        return response(400, {"message": f"Missing fields: {', '.join(missing)}"})

    session_id = str(body["session_id"]).strip()
    first_name = str(body["first_name"]).strip()
    last_name  = str(body["last_name"]).strip()
    email      = normalize_email(body["email"])

    # Verify session exists
    try:
        got = dynamodb.get_item(
            TableName="Session",
            Key={"session_id": {"S": session_id}},
            ProjectionExpression="session_id",
        )
    except ClientError:
        return response(500, {"message": "DynamoDB error checking session"})
    if "Item" not in got:
        return response(404, {"message": "Session not found"})

    # Put attendance (idempotent on student_id + session_id)
    student_id = make_student_id(first_name, last_name, email)
    item = {
        "student_id":    {"S": student_id},
        "session_id":    {"S": session_id},
        "points":        {"N": "5"},
        "checked_in_at": {"S": now_iso()},
    }

    try:
        get_result = dynamodb.get_item(
            TableName="Student",
            Key={"student_id": {"S": student_id}}
        )
        if "Item" not in get_result:
            return {"error": "Student account does not exist"}
            
        dynamodb.put_item(
            TableName="Attendance",
            Item=item,
            ConditionExpression="attribute_not_exists(student_id) AND attribute_not_exists(session_id)",
        )

        dynamodb.update_item(
            TableName="Student",
            Key={"student_id": {"S": student_id}},
            UpdateExpression="ADD attendance_points :increment, bonus_points :increment, total_points :increment",
            ExpressionAttributeValues={
                ":increment": {"N": "5"}
            }
        )
        
        return response(200, {"message": "Check-in recorded", "student_id": student_id})
    except ClientError as e:
        if e.response.get("Error", {}).get("Code") == "ConditionalCheckFailedException":
            return response(200, {"message": "Already checked in", "student_id": student_id})
        return response(500, {"message": "Failed to record attendance"})
