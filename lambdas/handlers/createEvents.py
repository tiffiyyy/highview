import boto3
import json
import uuid
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import response, now_iso

dynamodb = boto3.client('dynamodb', region_name='us-east-1')

def createSession(event):
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
    
    # Create the session item for DynamoDB
    session_item = {
        'session_id': {'S': session_id},
        'session_name': {'S': body['session_name']},
        'session_type': {'S': body['session_type']},
        'session_date': {'S': body['session_date']},
        'created_at': {'S': now_iso()}
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
            "created_at": session_item['created_at']['S']
        }
    })
        

print(createSession({"body": json.dumps({
    "session_name": "Test Session",
    "session_type": "PD",
    "session_date": "12/15/2024"
})}))