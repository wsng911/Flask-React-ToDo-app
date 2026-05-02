from functools import wraps
from flask import request, g, jsonify
import jwt
from datetime import datetime, timedelta
from index import app

TWO_WEEKS = 1209600


def generate_token(user, expiration=TWO_WEEKS):
    payload = {
        'id': user.id,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(seconds=expiration)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token


def verify_token(token):
    try:
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return data
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if token:
            string_token = token.encode('ascii', 'ignore')
            user = verify_token(string_token)
            if user:
                g.current_user = user
                return f(*args, **kwargs)

        return jsonify(message="Authentication is required to access this resource"), 401

    return decorated
