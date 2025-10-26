import boto3
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import cors_headers, response, get_number_of_missed_sessions

dynamodb = boto3.client(
        'dynamodb',
        region_name='us-east-1',
        aws_access_key_id=os.getenv("key_id"),
        aws_secret_access_key=os.getenv("access_key"))


# Teacher can search up student by name and get their information
def handler(event, context):
    method = (event.get("requestContext", {}).get("http", {}).get("method")
              or event.get("httpMethod", "GET"))
    if method == "OPTIONS":
        return {"statusCode": 204, "headers": cors_headers(), "body": ""}
    
    input_name = (event.get("body") or {}).get("input_name")
    if not input_name:
        return response(400, {"message": "input_name is required"})
    
    resp = dynamodb.scan(TableName="Student")
    list_of_students = []
    segments = input_name.split(" ")

    for student in resp.get('Items', []):
        student_id = student['student_id']['S']
        missed_sessions = get_number_of_missed_sessions(student_id)
        first = student['first']['S']
        last = student['last']['S']
        has_second_segment = 1 if len(segments) > 1 else 0
        if  segments[0].lower() in first.lower() or segments[0].lower() in last.lower() or segments[has_second_segment].lower() in first.lower() or segments[has_second_segment].lower() in last.lower():
            list_of_students.append({
                "student_id": student_id,
                "first": first,
                "last": last,
                "company": student['company']['S'],
                "total_points": student['total_points']['N'],
                "attendance_points": student["attendance_points"]["N"],
                "bonus_points": student["bonus_points"]["N"],
                "missed_sessions": missed_sessions
            })
    return list_of_students
