from flask import request, jsonify, current_app
from functools import wraps

def require_api_key(f):
    """
    Dekorator, der sicherstellt, dass die Anfrage einen gültigen API-Schlüssel enthält.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = current_app.config['API_KEY']

        request_api_key = request.headers.get('X-API-KEY')
        
        if request_api_key and request_api_key == api_key:
            return f(*args, **kwargs)
        else:
            return jsonify({"error": "Unauthorized"}), 401
    return decorated_function
