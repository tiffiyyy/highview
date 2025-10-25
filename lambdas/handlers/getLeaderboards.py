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

print(getTopStudents(10), end="\n\n\n")
print(getBottomStudents(10))