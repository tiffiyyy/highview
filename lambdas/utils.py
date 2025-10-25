import json
import datetime
# Reduce info from api calls to necessary attributes

def get_attendance_points(student_id):
    pass

# get total possible attendance points
def get_total_attendance_points(session_id): # num_session_types * 5
    pass

def get_bonus_points(student_id):
    pass

def get_number_of_missed_sessions(student_id):
    pass

def http_method(event):
    return (event.get("requestContext", {}).get("http", {}).get("method")
            or event.get("httpMethod", "GET"))

def raw_path(event):
    return event.get("rawPath") or event.get("path") or "/"

def path_params(event):
    return event.get("pathParameters") or {}

# def query_params(event):
#     return event.get("queryStringParameters") or {}

def cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type,Authorization",
        "Access-Control-Allow-Methods": "GET,POST,DELETE,OPTIONS",
    }

def response(status, body):
    return {
        "statusCode": status,
        "headers": { **cors_headers(), "Content-Type": "application/json" },
        "body": json.dumps(body),
    }

# need to add date column to attendance/bonus points?
def now_iso():
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat() 