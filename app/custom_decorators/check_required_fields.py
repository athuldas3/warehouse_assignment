from functools import wraps
from flask import request, jsonify


def check_required_fields(required_fields):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            # Check if the request has JSON data
            if request.is_json:
                # Check if all required fields are present in the request data
                if all(field in request.json for field in required_fields):
                    return view_func(*args, **kwargs)
                else:
                    # If any required field is missing, return a JSON response with an error message
                    error_message = f"Missing required fields: {', '.join(required_fields)}"
                    print("error_message", error_message)
                    return {"error": error_message}, 400
            else:
                # If the request doesn't contain JSON data, return an error response
                error_message = "Invalid JSON data in the request body"
                return {"error": error_message}, 400
        return wrapper
    return decorator
