import requests

from . import config


def default_headers():
    return {
        'Accept': config.JSON_MIME_TYPE,
        'User-Agent': config.USER_AGENT,
        'Content-type': config.JSON_MIME_TYPE
    }


class MercadoLibreSession(requests.Session):
    def request(self, *args, **kwargs):
        kwargs.setdefault('headers', default_headers())
        return super(MercadoLibreSession, self).request(*args, **kwargs)


def get_session():
    return MercadoLibreSession()