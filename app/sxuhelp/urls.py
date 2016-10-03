# conding:utf-8

from app.registryauth.auth import (
    RegistryAuthHandler,
    RegistryHandler
)

urlprefix = r'/registryauth'

urlpattern = (
    (r'/registryauth/auth', RegistryAuthHandler),
    (r'/registryauth', RegistryHandler),
)
