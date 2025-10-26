import boto3
import json
import uuid
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import response, now_iso

dynamodb = boto3.client(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id=os.getenv("key_id"),
    aws_secret_access_key=os.getenv("access_key"))

def getSessions(event, context):
    """
    Retrieve all sessions from the Session table
    """
    try:
        # Scan the entire Session table to get all sessions
        scan_response = dynamodb.scan(
            TableName='Session'
        )
        
        # Extract sessions from the response
        sessions = []
        for item in scan_response.get('Items', []):
            session = {
                'session_id': item.get('session_id', {}).get('S', ''),
                'created_at': item.get('created_at', {}).get('S', ''),
                'mentor_email': item.get('mentor_email', {}).get('S', ''),
                'qr_img': item.get('qr_img', {}).get('S', ''),
                'session_date': item.get('session_date', {}).get('S', ''),
                'session_description': item.get('session_description', {}).get('S', ''),
                'session_location': item.get('session_location', {}).get('S', ''),
                'session_name': item.get('session_name', {}).get('S', ''),
                'session_time': item.get('session_time', {}).get('S', ''),
                'session_type': item.get('session_type', {}).get('S', ''),
                #'updated_at': item.get('updated_at', {}).get('S', '')
            }
            sessions.append(session)
        
        # Return success response with all sessions
        return response(200, {
            "message": "Sessions retrieved successfully",
            "sessions": sessions,
            "count": len(sessions)
        })
        
    except Exception as e:
        # Return error response
        return response(500, {
            "message": "Error retrieving sessions",
            "error": str(e)
        })

if __name__ == "__main__":
    # Test the function
    test_event = {}
    result = getSessions()
    print(json.dumps(result, indent=2))