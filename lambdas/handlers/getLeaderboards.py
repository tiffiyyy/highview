import boto3
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_student_total_points


dynamodb = boto3.client(
        'dynamodb',
        region_name='us-east-1',
        aws_access_key_id=os.getenv("key_id"),
        aws_secret_access_key=os.getenv("access_key"))


def handler(event, context):
    # Scan the Student table to get all students
    response = dynamodb.scan(TableName="Student")
    
    students_with_points = []
    
    # Calculate total points for each student
    for student in response.get('Items', []):
        student_id = student['student_id']['S']
        # total_points = get_student_total_points(student_id)
        
        student_data = {
            "student_id": student_id,
            "first": student['first']['S'],
            "last": student['last']['S'],
            "company": student['company']['S'],
            "total_points": student['total_points']['N']
        }
        
        students_with_points.append(student_data)
    
    # Sort students by total points in descending order
    students_with_points.sort(key=lambda x: x['total_points'], reverse=True)
    
    return students_with_points
