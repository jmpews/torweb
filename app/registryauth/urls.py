# conding:utf-8

from app.registryauth.auth import (
    RegistryAuthHandler,
)

urlprefix = r'/registryauth'

urlpattern = (
    (r'/registryauth/auth', RegistryAuthHandler),
)
