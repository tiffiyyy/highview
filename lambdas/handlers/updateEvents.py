import boto3
import json
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import response, now_iso

dynamodb = boto3.client(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id=os.getenv("key_id"),
    aws_secret_access_key=os.getenv("access_key"),
)


def updateSession(event, context):
    raw = event.get("body")
    body = json.loads(raw) if isinstance(raw, str) else (raw or {})

    session_id = (event.get("pathParameters") or {}).get("session_id")
    if not session_id:
        return response(400, {"message": "path parameter 'session_id' is required"})

    got = dynamodb.get_item(
        TableName="Session",
        Key={"session_id": {"S": session_id}},
    )
    if "Item" not in got:
        return response(404, {"message": "Session not found"})

    old_item = got["Item"]

    new_item = dict(old_item)

    # update fields
    fields = [
        "session_name",
        "session_type",
        "session_date",
        "session_description",
        "session_location",
        "session_time",
        "email",
    ]

    for f in fields:
        if f in body and body[f] is not None:
            if f == "email":
                new_item["mentor_email"] = {"S": str(body[f])}
            else:
                new_item[f] = {"S": str(body[f])}

    if "created_at" not in new_item:
        new_item["created_at"] = {"S": now_iso()}
    new_item["updated_at"] = {"S": now_iso()}

    new_item["session_id"] = {"S": session_id}

    dynamodb.put_item(TableName="Session", Item=new_item)

    return response(200, {
        "message": "Session updated successfully",
        "session": {
            "session_id": new_item["session_id"]["S"],
            "session_name": new_item.get("session_name", {}).get("S", ""),
            "session_type": new_item.get("session_type", {}).get("S", ""),
            "session_date": new_item.get("session_date", {}).get("S", ""),
            "session_description": new_item.get("session_description", {}).get("S", ""),
            "session_location": new_item.get("session_location", {}).get("S", ""),
            "session_time": new_item.get("session_time", {}).get("S", ""),
            "email": new_item.get("mentor_email", {}).get("S", ""),
            "created_at": new_item.get("created_at", {}).get("S", ""),
            "updated_at": new_item.get("updated_at", {}).get("S", ""),
        }
    })
