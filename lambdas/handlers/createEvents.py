import boto3
import json
import uuid
import sys, os
from io import BytesIO
import qrcode
import qrcode.image.svg as qsvg
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import response, now_iso

dynamodb = boto3.client(
        'dynamodb',
        region_name='us-east-1',
        aws_access_key_id=os.getenv("key_id"),
        aws_secret_access_key=os.getenv("access_key"))

def createSession(event, context):

    # Parse the request body
    if isinstance(event.get('body'), str):
        body = json.loads(event['body'])
    else:
        body = event.get('body', {})
    
    # Session name, type, date, mentor need to be required in html
    
    # Generate a unique session ID
    session_id = str(uuid.uuid4())

    url = f"http://localhost:5173/session_checkin.html?session_id={session_id}"

    qr_img = qrcode.make(url, image_factory=qsvg.SvgImage)
    buffer = BytesIO()
    qr_img.save(buffer)
    svg_xml = buffer.getvalue().decode("utf-8")
    # qr_encoded = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    # Create the session item for DynamoDB
    session_item = {
        'session_id': {'S': session_id},
        'session_name': {'S': body['session_name']},
        'session_type': {'S': body['session_type']},
        'session_date': {'S': body['session_date']},
        'session_description': {'S': body['session_description']},
        'session_location': {'S': body['session_location']},
        'session_time': {'S': body['session_time']},
        'created_at': {'S': now_iso()},
        'qr_img': {'S': svg_xml},
        'mentor_email': {'S': body['email']}
    }
    
    # Put the item in the Session table
    dynamodb.put_item(
        TableName='Session',
        Item=session_item
    )
    
    # Return success response with the created session
    return response(201, {
        "message": "Session created successfully",
        "session": {
            "session_id": session_id,
            "session_name": body['session_name'],
            "session_type": body['session_type'],
            "session_date": body['session_date'],
            "session_description": body['session_description'],
            "session_location": body['session_location'],
            "session_time": body['session_time'],
            "created_at": session_item['created_at']['S']
        }
    })

# if __name__ == "__main__":
#     test_event = {
#         "body": json.dumps({
#             "session_name": "Intro to AWS",
#             "session_type": "Workshop",
#             "session_date": "2025-11-01",
#             "session_description": "Hands-on AWS workshop for students",
#             "session_location": "Room 201",
#             "session_time": "10:00 AM",
#             "email": "mentor@example.com"
#         })
#     }
#     result = createSession(test_event, None)
