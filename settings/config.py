# coding:utf-8

import os
from settings import development
from settings import production

# default config
config = development

def load_config(c):
    if c:
        # load config from arg
        if c == 'production':
            config = production
        elif c == 'development':
            config = development
        elif c == 'docker':
            pass
        else:
            config = development
    else:
        # load config from env
        envc = os.getenv('TORCONFIG', 'dev')
        if envc == 'production':
            config = production
        elif envc == 'development':
            config = development
        elif envc == 'docker':
            pass
        else:
            config = development
    return config
