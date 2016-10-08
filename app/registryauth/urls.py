# conding:utf-8

from app.registryauth.auth import (
    RegistryAuthHandler,
    RegistryHandler,
    RegistryEventHandler
)

urlprefix = r'/registryauth'

urlpattern = (
    (r'/registryauth/event', RegistryEventHandler),
    (r'/registryauth/auth', RegistryAuthHandler),
    (r'/registryauth', RegistryHandler),
)
