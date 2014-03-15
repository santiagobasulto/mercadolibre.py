from . import http
from . import config
from .resources import *
from .exceptions import UnauthorizedException


try:
    import urllib
    encode_function = urllib.urlencode
except AttributeError:
    from urllib import parse
    encode_function = parse.urlencode


class MercadoLibre(object):
    """
    High level API.
    """
    def __init__(self, app_id, app_secret,
                 access_token=None, refresh_token=None):
        self.session = http.get_session()

        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = access_token
        self.refresh_token = refresh_token

        self.site = SiteMLA
        self.items = Item

    def build_authorization_url(self, redirect_url):
        params = {
            "client_id": self.app_id,
            "response_type": "code",
            "redirect_uri": redirect_url,
        }
        return "{0}?{1}".format(config.AUTH_URL, encode_function(params))

    def authenticate(self, code, redirect_uri):
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.app_id,
            'client_secret': self.app_secret,
            'code': code,
            'redirect_uri': redirect_uri
        }

        response = self.session.post(config.OAUTH_URL, params=params)

        if not response.ok:
            response.raise_for_status()

        content = response.json()
        self.access_token = content['access_token']
        if 'refresh_token' in content:
            self.refresh_token = content['refresh_token']

        return (content.get('access_token'), content.get('refresh_token'))

    def create_item(self, data, params=None):
        if not self.access_token:
            raise UnauthorizedException(
                "Need an access token to perform this operation")
        return Item.post(
            data=data, params=None, access_token=self.access_token)


def login(app_id, app_secret, access_token=None, refresh_token=None):
    """Abstraction that creates an authorized API object and returns it."""
    return MercadoLibre(
        app_id, app_secret,
        access_token=access_token,
        refresh_token=refresh_token)
