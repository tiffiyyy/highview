import boto3
import json
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_student_total_points, response, now_iso, get_attendance_points,get_bonus_points


dynamodb = boto3.client(
        'dynamodb',
        region_name='us-east-1')

def addAttendancePointsToStudent(student_id):
    """
    Add attendance_points attribute to a student record
    """

    students = dynamodb.scan(TableName="Student")
    for student in students['Items']:
        student_id = student['student_id']['S']
        attendance_points = get_attendance_points(student_id)
        update_response = dynamodb.update_item(
                    TableName="Student",
                    Key={"student_id": {"S": student_id}},
                    UpdateExpression="SET attendance_points = :val, updated_at = :timestamp",
                    ExpressionAttributeValues={
                        ":val": {"N": str(attendance_points)},
                        ":timestamp": {"S": now_iso()}
                    })
        bonus_points = get_bonus_points(student_id)
        update_response = dynamodb.update_item(
                    TableName="Student",
                    Key={"student_id": {"S": student_id}},
                    UpdateExpression="SET bonus_points = :val, updated_at = :timestamp",
                    ExpressionAttributeValues={
                        ":val": {"N": str(bonus_points)},
                        ":timestamp": {"S": now_iso()}
                    })
        total_points = get_student_total_points(student_id)
        update_response = dynamodb.update_item(
                    TableName="Student",
                    Key={"student_id": {"S": student_id}},
                    UpdateExpression="SET total_points = :val, updated_at = :timestamp",
                    ExpressionAttributeValues={
                        ":val": {"N": str(total_points)},
                        ":timestamp": {"S": now_iso()}
                    })

    return response(200, {
            "message": "Attendance points added to student successfully",
            "student_id": student_id,
            "attendance_points": attendance_points
        })

    
        #First check if student exists
        # get_response = dynamodb.get_item(
        #     TableName="Student",
        #     Key={"student_id": {"S": student_id}}
        # )
        
        # if 'Item' not in get_response:
        #     return response(404, {"error": "Student not found"})
        
        # Validate attendance_points is a number
        #try:
        #    attendance_points = float(attendance_points)
        #except (ValueError, TypeError):
        #    return response(400, {"error": "attendance_points must be a valid number"})

        # for student in students['Items']:
        #     attendance_points = student['attendance_points']['N']
        #     update_response = dynamodb.update_item(
        #         TableName="Student",
        #         Key={"student_id": {"S": student_id}},
        #         UpdateExpression="SET attendance_points = :val, updated_at = :timestamp",
        #         ExpressionAttributeValues={
        #             ":val": {"N": str(attendance_points)},
        #             ":timestamp": {"S": now_iso()}
        #         }
        # )
        
        # Update the student record with attendance_points
        
        
        




print(addAttendancePointsToStudent("47502221-0d40-5bbb-b9dd-d40a316760dc"))

# print("\nTesting bulk update of all students:")
# print(addAttendancePointsToAllStudents())