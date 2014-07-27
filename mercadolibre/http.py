import requests

from . import config


def default_headers():
    return {
        'Accept': config.JSON_MIME_TYPE,
        'User-Agent': config.USER_AGENT,
        'Content-type': config.JSON_MIME_TYPE,
        'Accept-Charset': config.CHARACTER_SET,
    }


class MercadoLibreSession(requests.Session):
    def __init__(self, credentials=None):
        super(MercadoLibreSession, self).__init__()

        self.headers.update(default_headers())
        self.base_url = config.API_ROOT
        self.credentials = credentials

    def request(self, *args, **kwargs):
        params = kwargs.get('params', {})
        if 'access_token' not in params and self.credentials:
            params.update({'access_token': self.credentials.access_token})
            kwargs['params'] = params

        return super(MercadoLibreSession, self).request(*args, **kwargs)


def get_session(credentials):
    return MercadoLibreSession(credentials=credentials)