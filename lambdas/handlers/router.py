from utils import http_method, raw_path, path_params, response, clean_path, get_json, strip_stage
from lambdas.handlers.getStudent import getStudent


# Lambda func to route to different backend endpoints
def route(event, context):
    method = http_method(event)
    path   = raw_path(event)
    stage  = (event.get("requestContext", {}).get("stage") or
              event.get("requestContext", {}).get("http", {}).get("stage"))
    
    clean = strip_stage(path, stage)
    segs  = [s for s in clean.strip("/").split("/") if s]

    try:
        if method == "GET" and segs[0] == "student":
            student_id = segs[1]
            # data = get_json(event)
            # student_id = data.get("student_id")
            if not student_id:
                return response(400, {"message": "student_id is required"})
            return getStudent(student_id)
        
        return response(404, {"message": f"No route for {method} {path}"})
    
    except ValueError as ve:
        return response(400, {"message": str(ve)})
    except Exception as e:
        return response(500, {"message": "Internal error", "detail": str(e)})
    