# -*- coding: utf-8 -*-
import json
import urllib
import requests

from .config import API_ROOT, OAUTH_URL


class MercadoLibre:

    def __init__(self, app_id, secret_key,
                 access_token=None, refresh_token=None):
        self.app_id = app_id
        self.secret_key = secret_key
        self.access_token = access_token
        self.refresh_token = refresh_token

    def _get(self, path):
        pass

    def _post(self, path, body=None, params=None):
        if params is None:
            params = {}
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

    def create_item(self, data):
        url = '{0}{1}'.format(API_ROOT, '/items')
        params = {'access_token': self.access_token}
        response = self._post(url, body=data, params=params)

        if not response.status_code == requests.codes.ok:
            response.raise_for_status()

        return response.json()
