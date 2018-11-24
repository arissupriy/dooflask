from app import app
from app.configs import BASE, Config
import os, datetime
from jwt import ExpiredSignature, InvalidTokenError, ExpiredSignatureError
import jwt

class CreateURL:
    def __init__(self, *args, **kwargs):
        print('-----------------\nGenerating URLs')
        for route in args:
            print('... {} generated'.format(route['url_prefix']))
            app.register_blueprint(route['func'], url_prefix=route['url_prefix'])
        
        print('{} URLs successfully created\n -----------------'.format(len(args)))    

def doo_render(location, filename, **context):
    import os, imp, sys
    import imp
    from flask import send_from_directory, render_template
    base_path = os.path.dirname(location)
    app.template_folder = os.path.join(base_path, 'templates')
    return render_template(filename, **context)

def encode_auth_token(data):
    try:
        payload = {
            'sub': data,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5, seconds=60)
        }

        token = jwt.encode(
             payload, app.secret_key, algorithm='HS256'
        )

        if type(token) == bytes:
            token = token.decode('utf-8')

        return {
            "token": token,
            "loggedIn": payload['iat'],
            "expired": payload['exp']
        }
    except Exception as e:
        return e

def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        token = auth_token.headers.get('AUTHORIZATION').split( )[1]
    except Exception as e:
        token = auth_token.headers.get('AUTHORIZATION')
    payload = jwt.decode(token, secret_key)
    return payload