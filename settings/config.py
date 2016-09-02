# encoding: utf-8

import os
# config = None

def load_config(c):
    # global config

    from settings import development
    from settings import production

    if c:
        if c == 'production':
            config = development
        elif c == 'docker':
            pass
        else:
            config = production
    else:
        # load config from env
        envc = os.getenv('config', 'dev')
        if envc == 'production':
            config = production
        elif envc == 'docker':
            pass
        else:
            config = development
    return config
