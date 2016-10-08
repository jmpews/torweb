#coding:utf-8

from custor.handlers.basehandler import BaseRequestHandler
from custor.utils import json_result, get_cleaned_query_data, ColorPrint

from db.mysql_model.user import User

from custor.logger import logger

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, load_pem_private_key
import jwt
import json
import hashlib
import os
import base64
import time

from settings.config import config

# /v2/_catalog的授权
SCOPE_CATALOG = {"type":"registry","name":"catalog","actions":["*"]}

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
    def init_private_key(cls, private_key_path):
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

class DockerToken():
    key = None

    @classmethod
    def load_key(cls, key):
        cls.key = key

    def __init__(self, service, scopes, subject=''):
        if(not DockerToken.key):
            raise Exception('must load private key before')

        self.issuer = config.ISSUER
        self.service = service
        self.scopes = scopes
        self.subject = subject
        self.token_expiration = config.TOKEN_EXPIRATION

    # 获取key
    def get_kid(self, public_key):
        der_public_key = public_key.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)

        sha256 = hashlib.sha256(der_public_key)
        base32_payload = base64.b32encode(sha256.digest()[:30])  # 240bits / 8
        return b":".join(
            [base32_payload[i:i + 4] for i in range(0, 48, 4)]
        )

    def get_token(self):
        now = int(time.time())
        access = get_access_by_scope(self.scopes)
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
            'kid': self.get_kid(DockerToken.key.generate_public_key()).decode()
        }

        token = jwt.encode(claim, DockerToken.key.private_key.decode(), algorithm='RS256', headers=headers).decode()
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


def get_access_by_scope(scopes):
    access = list()
    # access.append(SCOPE_CATALOG)
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

def get_auth_user(handler):
    Authorization = handler.request.headers.get('Authorization', None)
    if Authorization:
        username, password = get_login_info(Authorization)
        # 验证用户名和密码
        print('Authorization:', username, password)
        u = User.auth(username, password)
        if u:
            return u
    return None

def check_scopes_with_user(scopes, user):
    access = get_access_by_scope(scopes)
    for scope in access:
        if scope['name'] == 'catalog':
            continue
        if 'pull' in scope['actions']:
            if user:
                pass
            else:
                return False
    return True

def unauthorized401(handler, scope, message=None, code=None):
    access = []
    _type, name, actions = scope.split(':')
    if actions == '':
        actions = []
    else:
        actions = actions.split(',')
    for action in actions:
        access.append({
            'Type': _type,
            'Name': name,
            'Action': action
        })
    data = {
        "errors": [
            {
                "code": code or "UNAUTHORIZED",
                "detail": access,
                "message": message or "access to the requested resource is not authorized. @knownsec"
            }
        ]
    }
    handler.set_status(401)
    handler.set_header('Content-Type', 'application/json; charset=utf-8')
    handler.set_header('Docker-Distribution-Api-Version', 'registry/2.0')
    handler.set_header('Www-Authenticate','Bearer realm="http://10.0.246.79:9000/registryauth/auth",service="token-service",scope="{0}",error="insufficient_scope"'.format(scope))
    print(data)
    handler.write(json.dumps(data))

def get_catalog():
    import requests
    token = DockerToken(
        service=config.SERVICE,
        scopes="registry:catalog:*",
        subject=''
    )
    res = token.get_token()
    s = requests.Session()
    # print(res['token'])
    s.headers.update({'Authorization': 'Bearer ' + res['token']})
    resp = s.get('http://127.0.0.1:5000/v2/_catalog')
    r = resp.json()
    return r['repositories']

def get_info_from_event(handler):
    result = []
    events = json.loads(handler.request.body.decode())['events']
    for event in events:
        action = event['action']
        target = event['target']
        repository = target.get('repository', '')
        tag = target.get('tag', None)
        actor = event['actor']
        username = actor.get('name', '')
        result.append({
            'action': action,
            'repository': repository,
            'tag': tag,
            'username': username
        })
    return result
