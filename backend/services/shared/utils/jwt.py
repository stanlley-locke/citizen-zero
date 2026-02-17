from datetime import datetime, timedelta
import jwt

def decode_token(token, secret_key):
    try:
        return jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
