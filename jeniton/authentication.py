import jwt,datetime
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from django.contrib.auth.models import User

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')
        if authorization_header:
            try:
                _, token = authorization_header.split()
                decoded_payload = jwt.decode(token, 'access_secret', algorithms=['HS256'])
                user_id = decoded_payload.get('user_id')
                user = User.objects.get(pk=user_id)
                return (user, None)
            except jwt.ExpiredSignatureError:
                raise exceptions.AuthenticationFailed('Token has expired')
            except jwt.InvalidTokenError:
                raise exceptions.AuthenticationFailed('Invalid token')
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed('User not found')
        raise exceptions.AuthenticationFailed('Authorization header missing')

def create_access_token(user_id):
    return jwt.encode(
        {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),  # 15 minutes for access token
            'iat': datetime.datetime.utcnow()
        },
        "access_secret", 
        algorithm='HS256'
    )

def create_refresh_token(user_id):
    return jwt.encode(
        {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),  # 7 days for refresh token
            'iat': datetime.datetime.utcnow()
        },
        "refresh_secret", 
        algorithm='HS256'
    )

def decode_access_token(token):
    try:
        payload = jwt.decode(token, 'access_secret', algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('Token has expired')
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed('Invalid token')
    except Exception as e:
        raise exceptions.AuthenticationFailed(str(e))
    
def decode_refresh_token(token):
    try:
        payload = jwt.decode(token,'refresh_secret', algorithms=['HS256'])
        return payload['user_id']
    except:
        return exceptions.AuthenticationFailed("Unauthenticated")
