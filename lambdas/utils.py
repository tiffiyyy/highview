import json
import datetime
import boto3
import uuid
import os
# Reduce info from api calls to necessary attributes

dynamodb = boto3.client(
        'dynamodb',
        region_name='us-east-1',
        aws_access_key_id=os.getenv("key_id"),
        aws_secret_access_key=os.getenv("access_key"))

def get_attendance_points(student_id):
    # Query attendance records for the student
    response = dynamodb.query(
        TableName="Attendance",
        KeyConditionExpression="student_id = :student_id",
        ExpressionAttributeValues={
            ":student_id": {"S": student_id}
        }
    )
    
    total_points = 0
    for record in response.get('Items', []):
        total_points += float(record['points']['N'])
    
    return total_points


# get total possible attendance points
def get_total_attendance_points(session_id): # num_session_types * 5
        # Scan the entire Session table to get all sessions
        response = dynamodb.scan(
            TableName="Session"
        )
        
        # Count the number of sessions
        session_count = len(response.get('Items', []))
        
        # Each session is worth 5 points
        total_possible_points = session_count * 5
        
        return total_possible_points


def get_bonus_points(student_id):
    response = dynamodb.query(
        TableName="BonusPoints",
        KeyConditionExpression="student_id = :student_id",
        ExpressionAttributeValues={
            ":student_id": {"S": student_id}
        }
    )
    
    total_bonus_points = 0
    for record in response.get('Items', []):
        total_bonus_points += float(record['points']['N'])
    
    return total_bonus_points
# print(get_bonus_points("47502221-0d40-5bbb-b9dd-d40a316760dc"))

def get_student_total_points(student_id):
    return get_attendance_points(student_id) + get_bonus_points(student_id)

def get_number_of_missed_sessions(student_id):
    response = dynamodb.query(
        TableName="Attendance",
        KeyConditionExpression="student_id = :student_id",
        ExpressionAttributeValues={
            ":student_id": {"S": student_id}
        }
    )
    missed_sessions = 0
    for record in response.get('Items', []):
        if record['points']['N'] == "2.5" or record['points']['N'] == "0":
            missed_sessions += 1
    return missed_sessions
    

def http_method(event):
    return (event.get("requestContext", {}).get("http", {}).get("method")
            or event.get("httpMethod", "GET"))

def raw_path(event):
    return event.get("rawPath") or event.get("path") or "/"

def path_params(event):
    return event.get("pathParameters") or {}

# def query_params(event):
#     return event.get("queryStringParameters") or {}

def normalize_email(email):
    return (email or "").strip().lower()

def make_student_id(first, last, email):
    # First|Last|normalized_email
    key = f"{(first or '').strip()}|{(last or '').strip()}|{normalize_email(email)}"
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, key))

def cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "GET,POST,DELETE,OPTIONS",
    }

def response(status, body):
    return {
        "statusCode": status,
        "headers": { **cors_headers(), "Content-Type": "application/json" },
        "body": json.dumps(body),
    }

def get_json(event):
    body = event.get("body")
    if not body:
        return {}
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON")

# need to add date column to attendance/bonus points?
def now_iso():
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat() 