import boto3
import json
import uuid
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import response, now_iso

dynamodb = boto3.client('dynamodb', region_name='us-east-1')

def deleteSession(session_type, session_id):
    try:
        # First check if the session exists
        get_response = dynamodb.get_item(
            TableName="Session",
            Key={
                'session_id': {'S': session_id},
                'session_type': {'S': session_type}
            }
        )
        
        if 'Item' not in get_response:
            return response(404, {"error": "Session not found with the provided keys"})
        
        # If session exists, proceed with deletion
        delete_response = dynamodb.delete_item(
            TableName="Session",
            Key={
                'session_id': {'S': session_id},
                'session_type': {'S': session_type}
            }
        )
        return response(200, {"message": "Session deleted successfully"})
        
    except dynamodb.exceptions.ResourceNotFoundException:
        return response(404, {"error": "Session table not found"})
    except Exception as e:
        return response(500, {"error": f"Failed to delete session: {str(e)}"})

print(deleteSession("PD","a53c1837-29e9-4a96-b955-f4e2fc14fbc3"))