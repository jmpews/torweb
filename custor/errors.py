# coding: utf-8

"""
Custom Exception
"""


class BaseException(Exception):
    def deal_with(self):
        pass


class RequestMissArgumentError(BaseException):
    """
    Miss Request
    """
    def __init__(self, msg='Args Miss.', code=233):
        self.msg = msg
        self.code = code
        super(RequestMissArgumentError, self).__init__(code, msg)

    def __str__(self):
        return self.msg


class PageNotFoundError(BaseException):
    """
    Page not found
    """
    def __init__(self, redirect_url='/static/404.html', code=233):
        self.redirect_url = redirect_url
        self.code = code
        super(PageNotFoundError, self).__init__(code, redirect_url)

    def __str__(self):
        return 'page not found.'
