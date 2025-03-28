# auth_helpers.py
import jwt
import datetime

SECRET_KEY = 'your_secret_key_here'

def generate_token(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token valid for 1 hour
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def validate_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['username']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
