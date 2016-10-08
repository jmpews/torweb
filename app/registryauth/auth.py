# coding:utf-8
from custor.handlers.basehandler import BaseRequestHandler
from custor.utils import json_result, get_cleaned_query_data, ColorPrint, get_cleaned_json_data
from custor.logger import logger

from settings.config import config
from app.registryauth.utils import get_access_by_scope, get_login_info, DockerToken, Key, unauthorized401, get_auth_user, check_scopes_with_user, get_info_from_event

import json

from db.mysql_model.user import User
from db.mysql_model.registry import RegistryImage

# 生成key
key = Key(private_key_path=config.private_key_path)
DockerToken.load_key(key)

class RegistryAuthHandler(BaseRequestHandler):
    """
    授权
    1. 未登录用户授权的 Push和Pull
    account = ''
    2. 登陆

    """
    def get(self, *args, **kwargs):
        service = get_cleaned_query_data(self, ['service'])['service']
        scopes = get_cleaned_query_data(self, ['scope'], blank=True)['scope']
        user = get_auth_user(self)
        if not check_scopes_with_user(scopes, user):
            unauthorized401(self, get_cleaned_query_data(self, ['scope'], blank=True)['scope'])
            return

        query_data = get_cleaned_query_data(self, ['scope', 'account', 'client_id'], blank=True)
        account = query_data['account']
        client_id = query_data['client_id']

        if not account:
            account = ''

        token = DockerToken(
            service=config.SERVICE,
            scopes=scopes,
            subject=account
        )
        res = token.get_token()
        self.write(json.dumps({'token': res['token']}))
        # unauthorized401(self, scopes)
        # HTTPError(404)
        return

class RegistryHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
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
        print(resp.json())
        self.write(resp.text)


class RegistryEventHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        events = get_info_from_event(self)
        for event in events:
            if event['action'] == 'push':
                repository = event['repository']
                tag = event['tag']
                if not tag:
                    continue
                user = User.get_by_username(event['username'])
                RegistryImage.create(user=user, action='push', repository=repository, tag=tag)
                logger.debug('Image: {0}:{1} Push.'.format(repository, tag))
        self.write('ok')
