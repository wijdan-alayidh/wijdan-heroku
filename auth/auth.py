import os

import json 
from flask import Flask, request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# Basic configuration attributes for AUTH0 
AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
ALGORITHMS = os.environ['ALGORITHMS']
API_AUDIENCE = os.environ['API_AUDIENCE']

'''
AuthError Exception : 
    - A standard way to communicate with auth failure.
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

'''
get_token_auth_header : 

    - This method responsable for getting request header 
    and return the token part of the header.
    
    - This method should raise AuthError in this situations:
        - if no header is present.
        - if no 'bearer' split in the Token
        - if the Token splits less than 2 
'''
def get_token_auth_header():

    # Get header from the request 
    auth = request.headers.get('Authorization', None)

    # check if the header is present in the request or rise Autherror
    if not auth:
        raise AuthError({
            "code": "authorization_header_missing",
            "description": "Authorization header is expected."
        }, 401)

    # check header parts
    parts = auth.split()

    # Check if the header not started with Bearer will raise Autherror
    if parts[0].lower() != 'bearer':
        raise AuthError ({
            "code": "invalid_header",
            "description": "Authorization header must start with 'Bearer'. "
        }, 401)

    ## The header must be 2 parts :
    ## - if the header have one part will raise Autherror
    elif len(parts) == 1:
        raise AuthError({
            "code": "invalid_header",
            "description": "Token not Found. "
        }, 401)

    ## - if the header have more than 2 parts will raise Autherror
    elif len(parts) > 2:
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must be barrer token. "
        }, 401)

    ## take payload part from header
    token = parts[1]
    return token

def check_permissions(permission, payload):

    if 'permissions' not in payload:
        
        raise AuthError({
            "code" : "invalid_claims",
            "description" : "Permissions not included in JWT."
        }, 400)

    if permission not in payload['permissions']:

        raise AuthError({
            "code" : "unauthorized",
            "description" : "Permission Not Found."
        }, 403)

    return True

def verify_decode_jwt(token):

    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:

        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:

        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)
        
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator