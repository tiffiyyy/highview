import boto3
import json
import uuid
import sys, os
import base64
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import response, now_iso
import qrcode # need to add this dependency?

dynamodb = boto3.client(
        'dynamodb',
        region_name='us-east-1',
        aws_access_key_id=os.getenv("key_id"),
        aws_secret_access_key=os.getenv("access_key"))

def createSession(event, context):
    """
    Create a new session in the Session table
    Expected event body: {
        "session_name": "string",
        "session_type": "string", 
        "session_date": "string"
    }
    """

    # Parse the request body
    if isinstance(event.get('body'), str):
        body = json.loads(event['body'])
    else:
        body = event.get('body', {})
    
    # Validate required fields
    required_fields = ['session_name', 'session_type', 'session_date']
    for field in required_fields:
        if field not in body:
            return response(400, {"error": f"Missing required field: {field}"})
    
    # Generate a unique session ID
    session_id = str(uuid.uuid4())

    url = f"<url-here>?session_id={session_id}"
    qr_img = qrcode.make(url)

    # encode this to base 64 and store in tbl
    with open(qr_img, "rb") as image_file:
        qr_encoded = base64.b64encode(image_file.read()).decode('utf-8')
    
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
        'qr_img': {'B': qr_encoded}
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