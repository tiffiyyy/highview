from utils import http_method, raw_path, path_params, response
from lambdas.handlers.getStudent import getStudent
from lambdas.handlers.createEvents import createSession
from lambdas.handlers.deleteEvents import deleteSession


# Lambda func to route to different backend endpoints
def route(event, context):
    method = http_method(event)
    path = raw_path(event)
    params = path_params(event)

    try:
        # Student endpoints
        if path.startswith("/student/") and method == "GET" and "student_id" in params:
            return getStudent(params["student_id"])  
        # Session creation endpoints
        elif path == "/sessions" and method == "POST":
            return createSession(event)
        # Session deletion endpoints
        elif path == "/sessions" and method == "DELETE" and "session_type" and "session_id" in params:
            return deleteSession(params["session_id"], params["session_type"])

        return response(404, {"message": f"No route for {method} {path}"})
    
    except ValueError as ve:
        return response(400, {"message": str(ve)})
    except Exception as e:
        return response(500, {"message": "Internal error", "detail": str(e)})
    