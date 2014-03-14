# -*- coding: utf-8 -*-
import urllib
import requests

from .config import OAUTH_URL


class MercadoLibre:

    def __init__(self, app_id, secret_key,
                 access_token=None, refresh_token=None):
        self.app_id = app_id
        self.secret_key = secret_key
        self.access_token = access_token
        self.refresh_token = refresh_token

    def _get(self, path):
        pass

    def _post(self, path, body=None, params={}):
        url = self._build_url(path, params)
        return requests.post(url, body)

    def _put(self, path, body=None, params={}):
        pass

    def _delete(self, path, params={}):
        pass

    def _options(self, path, params={}):
        pass

    def _build_url(self, path, params={}):
        return '{0}?{1}'.format(path, urllib.urlencode(params))

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
