import boto3
from botocore.exceptions import ClientError
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_attendance_points, get_total_attendance_points, get_bonus_points, get_number_of_missed_sessions, response, get_student_total_points

dynamodb = boto3.client(
        'dynamodb',
        region_name='us-east-1',
        aws_access_key_id=os.getenv("key_id"),
        aws_secret_access_key=os.getenv("access_key"))


# Teacher can search up student by name and get their information
def handler(event, context):
    student_id = (event.get("pathParameters") or {}).get("student_id")
    if not student_id:
        return response(400, {"message": "student_id is required"})
    
    try:
        resp = dynamodb.get_item(
            TableName="Student",
            Key={
                'student_id': {'S': student_id}
            }
        )
    except ClientError:
        return response(500, {"message": "DynamoDB error"})
    
    student_data = resp.get("Item")
    if not student_data:
        return response(404, {"message": "Student not found", "student_id": student_id})

    totalAttendancePoints = get_attendance_points(student_id)
    bonusPoints = get_bonus_points(student_id)
    totalPoints = totalAttendancePoints + bonusPoints
    # position = getSpecificStudent(student_id)
    position = 0
    missedSessions = get_number_of_missed_sessions(student_id)

    payload = {
            "first": student_data["first"]['S'],
            "last": student_data["last"]['S'],
            "company": student_data["company"]['S'],
            "email": student_data["email"]['S'],
            "points": totalPoints,
            "position": position,
            "attendancePoints": totalAttendancePoints,
            "bonusPoints": bonusPoints,
            "missedSessions": missedSessions
        }
    return response(200, payload)

# print(getStudent("47502221-0d40-5bbb-b9dd-d40a316760dc"))