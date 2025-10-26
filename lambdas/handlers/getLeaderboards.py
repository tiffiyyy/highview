from requests import Response
import boto3
import json
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_student_total_points
# from utils import get_attendance_points, get_total_attendance_points, get_bonus_points, get_number_of_missed_sessions

dynamodb = boto3.client('dynamodb', region_name='us-east-1')
response = dynamodb.list_tables()
# Get table info for Students table
table_info = dynamodb.describe_table(TableName="Student")

def getTopStudents(num_students):
    # Scan the Student table to get all students
    response = dynamodb.scan(TableName="Student")
    
    students_with_points = []
    
    # Calculate total points for each student
    for student in response.get('Items', []):
        student_id = student['student_id']['S']
        total_points = get_student_total_points(student_id)
        
        student_data = {
            "student_id": student_id,
            "first": student['first']['S'],
            "last": student['last']['S'],
            "company": student['company']['S'],
            "email": student['email']['S'],
            "total_points": total_points
        }
        
        students_with_points.append(student_data)
    
    # Sort students by total points in descending order
    students_with_points.sort(key=lambda x: x['total_points'], reverse=True)
    
    # Return top 50 students
    return students_with_points[:num_students]


def getBottomStudents(num_students):
    # Scan the Student table to get all students
    response = dynamodb.scan(TableName="Student")
    
    students_with_points = []
    
    # Calculate total points for each student
    for student in response.get('Items', []):
        student_id = student['student_id']['S']
        total_points = get_student_total_points(student_id)
        
        student_data = {
            "student_id": student_id,
            "first": student['first']['S'],
            "last": student['last']['S'],
            "company": student['company']['S'],
            "email": student['email']['S'],
            "total_points": total_points
        }
        
        students_with_points.append(student_data)
    
    # Sort students by total points in descending order
    students_with_points.sort(key=lambda x: x['total_points'], reverse=True)
    
    # Return bottom students (last num_students from the sorted list)
    return students_with_points[-num_students:]

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
        return {"error": "Student not found in leaderboard"}
    
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

print(getSpecificStudent("3117d8e7-9f80-5178-bd10-33a42b6c2842")) #Frodo
print(getTopStudents(10), end="\n\n\n")
print(getBottomStudents(10))