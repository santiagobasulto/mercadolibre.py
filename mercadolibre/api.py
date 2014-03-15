import requests

from .resources import *
from .exceptions import UnauthorizedException
from .config import API_ROOT, OAUTH_URL


class MercadoLibre(object):
    """
    High level API.
    """
    def __init__(self, app_id, secret_key,
                 access_token=None, refresh_token=None):
        self.app_id = app_id
        self.secret_key = secret_key
        self.access_token = access_token
        self.refresh_token = refresh_token

        self.site = SiteMLA
        self.items = Item

    def authenticate(self, code, redirect_uri):
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.app_id,
            'client_secret': self.secret_key,
            'code': code,
            'redirect_uri': redirect_uri
        }
        response = self._post(OAUTH_URL, params=params)

        if not response.status_code == requests.codes.ok:
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


def login(app_id, app_secret, access_token, refresh_token=None):
    """Abstraction that creates an authorized API object and returns it."""
    return MercadoLibre(
        app_id, app_secret,
        access_token=access_token,
        refresh_token=refresh_token)
