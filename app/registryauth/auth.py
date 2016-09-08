# coding:utf-8
import tornado.web
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

class DockerRegistryAuth:
    def __init__(self, account, scopes, service, issuer, private_key_path, token_expires=300):
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
        scopes = [scopes,]
        access = list()
        if not scopes:
            return access
        for scope in scopes:
            type_, name, actions = scope.split(':')
            access.append({
                'type': type_,
                'name': name,
                'actions': actions.split(',')
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

class RegistryAuthHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        query_data = get_cleaned_query_data(self, ['scope', 'service'])
        account, client_id, Authorization = get_cleaned_query_data(self, ['account', 'client_id','Authorization'], blank=True)
        if not account:
            account = ''
        if not Authorization:
            Authorization = ''
        print(query_data)
        registry_auth = DockerRegistryAuth(account=account,
                                           scopes=query_data['scope'],
                                           service=SERVICE,
                                           issuer=ISSUER,
                                           private_key_path='./private_key.pem'
                                           )
        if not registry_auth.check_service(query_data['service']):
            return DockerRegistryAuth.unauthorized401(self, 'service not be allowed.')
        res = registry_auth.get_token()
        self.write(json.dumps({'token': res['token']}))
        return

        user = registry_auth.get_login_info(self.request.headers.get('Authorization'))
        if user:
            if not(user['username'] == 'test' and user['password'] == 'test'):
                return DockerRegistryAuth.unauthorizted401(self, 'incorrect username or password')
            res = registry_auth.get_token()
            self.write(json.dumps({'token': res['token']}))
