# -*- coding: utf-8 -*-
import json
import requests

from .resources import *
from .config import API_ROOT, OAUTH_URL

try:
    import urllib
    encode_function = urllib.urlencode
except AttributeError:
    from urllib import parse
    encode_function = parse.urlencode


class MercadoLibre:

    def __init__(self, app_id, secret_key,
                 access_token=None, refresh_token=None):
        self.app_id = app_id
        self.secret_key = secret_key
        self.access_token = access_token
        self.refresh_token = refresh_token

    def _get(self, path):
        pass

    def _post(self, path, body=None, params=None, privileged=True):
        if params is None:
            params = {}

        if privileged and not 'access_token' in params:
            params.update({'access_token': self.access_token})

        headers = {
            'Accept': 'application/json',
            'User-Agent': '',
            'Content-type': 'application/json'
        }
        url = self._build_url(path, params)

        if body is not None:
            body = json.dumps(body)
        return requests.post(url, body, headers=headers)

    def _put(self, path, body=None, params=None):
        pass

    def _delete(self, path, params=None):
        pass

    def _options(self, path, params=None):
        pass

    def _build_url(self, path, params=None):
        if params is None:
            params = {}

        return '{}/{}?{}'.format(
            API_ROOT, path, encode_function(params))

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

    def create_item(self, data, params=None):
        if not params:
            params = {}

        path = 'items'
        response = self._post(path, body=data, params=params)

        if not response.status_code == requests.codes.ok:
            response.raise_for_status()
        import ipdb; ipdb.set_trace()

        return Item(api=self, data=response.json())

    def validate_item(self, data, params=None):
        if not params:
            params = {}

        path = 'items/validate'
        response = self._post(path, body=data, params=params)

        if not response.status_code == requests.codes.ok:
            response.raise_for_status()

        return response

    def upload_picture(self, picture_io=None):
        pass
