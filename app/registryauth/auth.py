# coding:utf-8
import tornado.web
import asyncio
import tornado.httpclient
from tornado.web import HTTPError
from custor.handlers.basehandler import BaseRequestHandler
from custor.utils import json_result, get_cleaned_query_data, ColorPrint
from custor.logger import logger

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, load_pem_private_key
import jwt
import json
import hashlib
import os
import base64

import time

SERVICE = 'token-service'
ISSUER = 'registry-token-issuer'

# /v2/_catalog的授权
SCOPE_CATALOG = {"type":"registry","name":"catalog","actions":["*"]}
TOKEN_EXPIRATION = 300

# 生成token所需要的key
class Key(object):
    private_key = None

    def __new__(cls, *args, **kwargs):
        cls.private_key = ''
        # In Python 3.3 and later, if you're overriding both __new__ and __init__, you need to avoid passing any extra arguments to the object methods you're overriding.
        # If you only override one of those methods, it's allowed to pass extra arguments to the other one (since that usually happens without your help).
        # 疑问? 不是通过new调用init了?
        return super(Key, cls).__new__(Key)

    def __init__(self, private_key_path='./private_key.pem'):
        fp = open(private_key_path, 'rb')
        self.private_key = fp.read()

    def generate_public_key(self):
        private_key = load_pem_private_key(
                self.private_key,
                password=None,
                backend=default_backend()
        )
        return private_key.public_key()

    @classmethod
    def init_private_key(cls, private_key_path='./private_key.pem'):
        fp = open(private_key_path)
        cls.private_key = fp.read()

    @classmethod
    def gen_public_key(cls):
        if cls.private_key is None:
            logger.debug('must init_private_key.')
            return None
        private_key = load_pem_private_key(
                cls.private_key,
                password=None,
                backend=default_backend()
        )
        return private_key.public_key()

# 生成key
key = Key(private_key_path='./private_key.pem')


class DockerToken():
    def __init__(self, service, scopes, subject=''):
        self.issuer = ISSUER
        self.service = service
        self.scopes = scopes
        self.subject = subject
        self.token_expiration = TOKEN_EXPIRATION

    # 获取key
    def get_kid(self, public_key):
        der_public_key = public_key.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)

        sha256 = hashlib.sha256(der_public_key)
        base32_payload = base64.b32encode(sha256.digest()[:30])  # 240bits / 8
        return b":".join(
            [base32_payload[i:i + 4] for i in range(0, 48, 4)]
        )

    def get_access_by_scopes(self, scopes):
        access = list()
        access.append(SCOPE_CATALOG)
        if not scopes:
            return access
        scopes = [scopes, ]
        for scope in scopes:
            _type, name, actions = scope.split(':')
            if actions == '':
                actions = []
            else:
                actions = actions.split(',')
            access.append({
                'type': _type,
                'name': name,
                'actions': actions
            })
        return access

    def get_token(self, key):
        now = int(time.time())
        access = self.get_access_by_scopes(self.scopes)
        print(access)
        claim = {
            'iss': self.issuer,
            'sub': self.subject,
            'aud': self.service,
            'exp': now + self.token_expiration,
            'nbf': now,
            'iat': now,
            'jti': base64.b64encode(os.urandom(1024)).decode(),
            'access': access
        }

        headers = {
            'kid': self.get_kid(key.generate_public_key()).decode()
        }

        token = jwt.encode(claim, key.private_key.decode(), algorithm='RS256', headers=headers).decode()
        return {
            'token': token,
            'issued_at': now,
            'expires_in': now + self.token_expiration
        }


def get_login_info(authorization):
    if not authorization:
        return None
    auth_info = authorization
    if authorization.startswith('Basic'):
        auth_info = authorization[5:]

    user_info = base64.b64decode(auth_info).decode()
    username, password = user_info.split(':')
    # return {
    #     'username': username,
    #     'password': password,
    # }
    return username, password


def get_access_by_scopes(scopes):
    access = list()
    if not scopes:
        return access
    scopes = [scopes,]
    for scope in scopes:
        type_, name, actions = scope.split(':')
        access.append({
            'type': type_,
            'name': name,
            'actions': actions.split(',')
        })

    return access

def unauthorized401(handler, scope, message=None, code=None):
    detail = list()
    access = get_access_by_scopes(scope)
    for scope in access:
        for action in scope['actions']:
            detail.append({
                "Action": action,
                "Name": scope['name'],
                "Type": scope['type']
            })
    data = {
        "errors": [
            {
                "code": code or "jmpews-error-code",
                "detail": detail,
                "message": message or "access to the requested resource is not authorized"
            }
        ]
    }
    handler.set_status(401)
    handler.set_header('Content-Type', 'application/json; charset=utf-8')
    handler.set_header('Docker-Distribution-Api-Version', 'registry/2.0')
    handler.set_header('Www-Authenticate','Bearer realm="https://127.0.0.1:9000/registryauth/auth",service="token-service",scope="{0}"'.format(scope))
    handler.write(json.dumps(data))

class RegistryAuthHandler(BaseRequestHandler):
    """
    授权
    1. 未登录用户授权的 Push和Pull
    account = ''
    2. 登陆

    """
    def get(self, *args, **kwargs):
        service = get_cleaned_query_data(self, ['service'])['service']
        Authorization = self.request.headers.get('Authorization', None)
        if Authorization:
            username, password = get_login_info(Authorization)
            # 验证用户名和密码
            print('Authorization:', username, password)

        query_data = get_cleaned_query_data(self, ['scope', 'account', 'client_id'], blank=True)
        scopes = query_data['scope']
        account = query_data['account']
        client_id = query_data['client_id']

        if not account:
            account = ''

        token = DockerToken(
            service=SERVICE,
            scopes=scopes,
            subject=account
        )
        res = token.get_token(key=key)
        self.write(json.dumps({'token': res['token']}))
        # unauthorized401(self, scopes)
        # HTTPError(404)
        return

class RegistryHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        import requests
        token = DockerToken(
            service=SERVICE,
            scopes=None,
            subject=''
        )
        res = token.get_token(key=key)
        s = requests.Session()
        # print(res['token'])
        s.headers.update({'Authorization': 'Bearer ' + res['token']})
        resp = s.get('http://127.0.0.1:5000/v2/_catalog')
        print(resp.json())
        self.write(resp.text)


def get_catalog():
    import requests
    token = DockerToken(
        service=SERVICE,
        scopes=None,
        subject=''
    )
    res = token.get_token(key=key)
    s = requests.Session()
    # print(res['token'])
    s.headers.update({'Authorization': 'Bearer ' + res['token']})
    resp = s.get('http://127.0.0.1:5000/v2/_catalog')
    r = resp.json()
    return r['repositories']


