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
    position = getSpecificStudent(student_id)
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

def getSpecificStudent(student_id):
    # Get the student from the Student table
    response = dynamodb.get_item(TableName="Student", Key={"student_id": {"S": student_id}})
    
    if 'Item' not in response:
        return {"error": "Student not found"}
    
    student_data = response['Item']
    
    # Get all students and calculate their points
    all_students_response = dynamodb.scan(TableName="Student")
    students_with_points = []
    
    for student in all_students_response.get('Items', []):
        current_student_id = student['student_id']['S']
        total_points = get_student_total_points(current_student_id)
        
        student_info = {
            "student_id": current_student_id,
            "first": student['first']['S'],
            "last": student['last']['S'],
            "company": student['company']['S'],
            "email": student['email']['S'],
            "total_points": total_points
        }
        
        students_with_points.append(student_info)
    
    # Sort students by total points in descending order
    students_with_points.sort(key=lambda x: x['total_points'], reverse=True)
    
    # Find the position of the specific student
    position = None
    for i, student in enumerate(students_with_points):
        if student['student_id'] == student_id:
            position = i + 1  # 1-based ranking
            break
    
    if position is None:
        return 0
    return position
    
    # Get the student's total points
    student_total_points = get_student_total_points(student_id)
    
    return {
        "student_id": student_id,
        "first": student_data["first"]['S'],
        "last": student_data["last"]['S'],
        "company": student_data["company"]['S'],
        "email": student_data["email"]['S'],
        "total_points": student_total_points,
        "position": position,
        "total_students": len(students_with_points)
    }
# print(getStudent("47502221-0d40-5bbb-b9dd-d40a316760dc"))