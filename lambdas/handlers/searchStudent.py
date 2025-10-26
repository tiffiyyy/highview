import boto3
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

dynamodb = boto3.client(
        'dynamodb',
        region_name='us-east-1',
        aws_access_key_id=os.getenv("key_id"),
        aws_secret_access_key=os.getenv("access_key"))


# Teacher can search up student by name and get their information
def handler(event, context):
    input_name = (event.get("body") or {}).get("input_name")
    if not input_name:
        return response(400, {"message": "input_name is required"})
    
    response = dynamodb.scan(TableName="Student")
    list_of_students = []
    segments = input_name.split(" ")

    for student in response.get('Items', []):
        student_id = student['student_id']['S']
        first = student['first']['S']
        last = student['last']['S']
        has_second_segment = 1 if len(segments) > 1 else 0
        if  segments[0].lower() in first.lower() or segments[0].lower() in last.lower() or segments[has_second_segment].lower() in first.lower() or segments[has_second_segment].lower() in last.lower():
            list_of_students.append({
                "student_id": student_id,
                "first": first,
                "last": last,
                "company": student['company']['S'],
                "total_points": student['total_points']['N']
            })
    return list_of_students

