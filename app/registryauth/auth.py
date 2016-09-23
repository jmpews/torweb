# coding:utf-8
import tornado.web
import asyncio
import tornado.httpclient
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

class DockerRegistryAuth:
    def __init__(self,private_key_path, scopes='::',service=SERVICE, account='', issuer=ISSUER, token_expires=300):
        self.account = account
        self.issuer = issuer
        self.scopes = scopes
        self.access = self.get_access_by_scopes(scopes)
        self.service = service
        self.private_key_path = private_key_path
        self.token_expires = token_expires

    @property
    def private_key(self):
        if getattr(self, '_private_key_content', None):
            return self._private_key_content

        with open(self.private_key_path, 'rb') as fp:
            setattr(self, '_private_key_content', fp.read())
            return self._private_key_content

    @property
    def public_key(self):
        private_key = load_pem_private_key(
                self.private_key,
                password=None,
                backend=default_backend()
        )
        _public_key = private_key.public_key()
        return _public_key


    def check_service(self, service):
        return self.service == service

    def get_token(self):
        now = int(time.time())
        claim = {
            'iss': self.issuer,
            'sub': self.account,
            'aud': self.service,
            'exp': now + self.token_expires,
            'nbf': now,
            'iat': now,
            'jti': base64.b64encode(os.urandom(1024)).decode(),
            'access': self.access
        }

        headers = {
            'kid': self.get_kid().decode()
        }
        # import pdb;pdb.set_trace()
        token = jwt.encode(claim, self.private_key.decode(), algorithm='RS256', headers=headers).decode()
        return {
            'token': token,
            'issued_at': now,
            'expires_in': now + self.token_expires
        }

    def get_kid(self):
        der_public_key = self.public_key.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)

        sha256 = hashlib.sha256(der_public_key)
        base32_payload = base64.b32encode(sha256.digest()[:30])  # 240bits / 8
        return b":".join(
            [base32_payload[i:i + 4] for i in range(0, 48, 4)]
        )

    def get_login_info(self, authorization):
        if not authorization:
            return None
        auth_info = authorization
        if authorization.startswith('Basic'):
            auth_info = authorization[5:]

        user_info = base64.b64decode(auth_info)
        self.username, self.password = user_info.split(':')
        return {
            'username': self.username,
            'password': self.password,
        }

    def get_access_by_scopes(self, scopes):
        print(scopes)
        scopes = [scopes,]
        access = list()
        if not scopes:
            return access
        for scope in scopes:
            type_, name, actions = scope.split(':')
            if actions == '':
                actions = []
            else:
                actions = actions.split(',')
            access.append({
                'type': type_,
                'name': name,
                'actions': actions
            })

        return access

    @staticmethod
    def unauthorized401(handler, access, message=None, code=None):
        detail = list()
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
                    "code": code or "UNAUTHORIZED",
                    "detail": detail,
                    "message": message or "access to the requested resource is not authorized"
                }
            ]
        }
        handler.set_status(401)
        handler.set_header('Content-Type', 'application/json; charset=utf-8')
        handler.set_header('Docker-Distribution-Api-Version', 'registry/2.0')
        handler.set_header('Www-Authenticate', 'Bearer realm="https://auth.docker.io/token",service="registry.docker.io",scope="repository:samalba/my-app:pull,push"')
        handler.write(json.dumps(data), 401)

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

        claim = {
            'iss': self.issuer,
            'sub': self.subject,
            'aud': self.service,
            'exp': now + self.token_expiration,
            'nbf': now,
            'iat': now,
            'jti': base64.b64encode(os.urandom(1024)).decode(),
            'access': self.get_access_by_scopes(self.scopes)
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


def unauthorized401(handler, access, message=None, code=None):
    detail = list()
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
                "code": code or "UNAUTHORIZED",
                "detail": detail,
                "message": message or "access to the requested resource is not authorized"
            }
        ]
    }
    handler.set_status(401)
    handler.set_header('Content-Type', 'application/json; charset=utf-8')
    handler.set_header('Docker-Distribution-Api-Version', 'registry/2.0')
    handler.set_header('Www-Authenticate',
                       'Bearer realm="https://auth.docker.io/token",service="registry.docker.io",scope="repository:samalba/my-app:pull,push"')
    handler.write(json.dumps(data), 401)

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
        return
