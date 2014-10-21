from . import http
from . import config
from mercadolibre.auth import Credentials
from .resources import *


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
    def __init__(self, credentials):
        self.session = http.get_session(credentials)

        self.credentials = credentials

        self.mla = MLASiteResource
        self.mla.credentials = credentials

        self.items = ItemResource
        self.items.credentials = credentials

        self.categories = CategoryResource
        self.categories.credentials = credentials

        self.test_user = TestUser
        self.test_user.credentials = credentials

    def me(self):
        return UserResource.get("me", credentials=self.credentials)

    @property
    def is_authenticated(self):
        return self.credentials.is_authenticated()

    @property
    def is_authorized(self):
        return self.credentials.is_authorized()

    def build_authorization_url(self, redirect_url):
        params = {
            "client_id": self.credentials.app_id,
            "response_type": "code",
            "redirect_uri": redirect_url,
        }
        return "{0}?{1}".format(config.AUTH_URL, encode_function(params))

    def refresh_access_token(self, refresh_token):
        params = {
            'grant_type': 'refresh_token',
            'client_id': self.credentials.app_id,
            'client_secret': self.credentials.app_secret,
            'refresh_token': refresh_token
        }

        response = self.session.post(
            config.OAUTH_URL, params=params, suppress_access_token=True)

        if not response.ok:
            response.raise_for_status()
        content = response.json()
        self.access_token = content.get('access_token')
        self.refresh_token = content.get('refresh_token')
        return (self.access_token, self.refresh_token)

    def authenticate(self, code, redirect_uri):
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.credentials.app_id,
            'client_secret': self.credentials.app_secret,
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


def login(credentials=None, app_id=None, app_secret=None,
          access_token=None, refresh_token=None):
    """Abstraction that creates an authorized API object and returns it."""

    if credentials is None:
        if not all([app_id, app_secret]):
            raise AttributeError(
                "App ID and App Secret are required. Check Docs.")
        credentials = Credentials(
            app_id=app_id, app_secret=app_secret,
            access_token=access_token, refresh_token=refresh_token)
    elif not isinstance(credentials, Credentials):
        # I'm killing Duck Typing. Sorry.
        raise AttributeError(
            "credentials must be a subclass of mercadolibre.auth.Credentials."
            " Check the docs.")

    return MercadoLibre(credentials)
