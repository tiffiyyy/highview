from requests import Response
import boto3
import json
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import getStudentPoints, getStudentEventsAttended
dynamodb = boto3.client('dynamodb', region_name='us-east-1')
response = dynamodb.list_tables()
# Get table info for Students table
table_info = dynamodb.describe_table(TableName="Student")
# print(table_info)

# Teacher can search up student by name and get their information
def getStudent(event): #add back (event, student_id) later 
    # try:
        # student_id = event['student_id']
        # student_id = event['pathParameters'].get('student_id')

        response = dynamodb.get_item(
            TableName="Student",
            Key={
                'student_id': {'S': event["student_id"]} #change to just "student_id"
            }
        )

        # student_info = response["Item"]
        # print(student_info["company"]['S'])
        totalAttendancePoints = get_attendance_points(student_id)
        bonusPoints = get_bonus_points(student_id)
        totalPoints = totalAttendancePoints + bonusPoints

        missedSessions = get_number_of_missed_sessions(student_id)

        
        if 'Item' in response:
            student_data = response['Item']
            payload = {
                    "first": student_data["first"]['S'],
                    "last": student_data["last"]['S'],
                    "company": student_data["company"]['S'],
                    "email": student_data["email"]['S'],
                    "points": totalPoints,
                    "attendancePoints": totalAttendancePoints,
                    "bonusPoints": bonusPoints,
                    "missedSessions": missedSessions
                }
            return response(200, payload)
            # return {
            #     "statusCode": 200,
            #     "body": json.dumps({
            #         "first": student_data["first"]['S'],
            #         "last": student_data["last"]['S'],
            #         "company": student_data["company"]['S'],
            #         "email": student_data["email"]['S'],
            #         "points": totalPoints,
            #         "attendancePoints": totalAttendancePoints,
            #         "bonusPoints": bonusPoints,
            #         "missedSessions": missedSessions
            #     })
            # }
        
    # except Exception as e:
    #     return {
    #         "statusCode": 200,
    #         "body": json.dumps({"data": "your data"})
    #     }
        #return Response(500, {"error": str(e)})

print(getStudent({"student_id": "47502221-0d40-5bbb-b9dd-d40a316760dc"}))