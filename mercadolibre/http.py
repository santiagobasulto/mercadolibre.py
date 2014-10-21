import ssl

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

from . import config


def default_headers():
    return {
        'Accept': config.JSON_MIME_TYPE,
        'User-Agent': config.USER_AGENT,
        'Content-type': config.JSON_MIME_TYPE,
        'Accept-Charset': config.CHARACTER_SET,
    }


class Ssl3HttpAdapter(HTTPAdapter):
    """"Transport adapter that allows us to use SSLv3.
    Originally derived from requests docs, this allows us to overcome
    MercadoLibre limitations with a poorly implemented SSL Setup:

    https://www.ssllabs.com/ssltest/analyze.html?d=api.mercadolibre.com
    """
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_SSLv3)


class MercadoLibreSession(requests.Session):
    def __init__(self, credentials=None):
        super(MercadoLibreSession, self).__init__()

        self.headers.update(default_headers())
        self.base_url = config.API_ROOT
        self.credentials = credentials

    def request(self, *args, **kwargs):
        """
        :param suppress_access_token: Will avoid appending the access token
            to the request.
        :param args: Accepts the same arguments as `requests.Session.request`
        :param kwargs: Accepts the same arguments as `requests.Session.request`
        :return: Same as `requests.Session.request`
        """
        params = kwargs.get('params', {})

        if 'access_token' not in params and self.credentials:
            kwargs.setdefault('suppress_access_token', False)
            if not kwargs['suppress_access_token']:
                params.update({'access_token': self.credentials.access_token})
            del kwargs['suppress_access_token']
            kwargs['params'] = params

        self.mount(config.API_ROOT, Ssl3HttpAdapter())
        kwargs['verify'] = True
        response = super(MercadoLibreSession, self).request(*args, **kwargs)

        return response


def get_session(credentials):
    return MercadoLibreSession(credentials=credentials)
