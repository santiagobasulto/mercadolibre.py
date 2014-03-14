# -*- coding: utf-8 -*-
import json
import unittest
import requests
from mock import patch

from mercadolibre import MercadoLibre


class TestMercadoLibreAuthentication(unittest.TestCase):
    def setUp(self):
        self.client = MercadoLibre(app_id='test', secret_key='test')

    def _fake_response(self, status=200, content=None):
        response = requests.Response()
        response.status_code = status
        if content is not None:
            if isinstance(content, dict):
                content = json.dumps(content)
            response._content = content
        return response

    def test_authenticate(self):
        content = {
            u'access_token': u'fake_access_token',
            u'token_type': u'bearer',
            u'expires_in': 21600,
            u'refresh_token': u'fake_code',
            u'scope': u'offline_access read write'
        }
        with patch.object(requests, 'post') as mocked_method:
            mocked_method.return_value = self._fake_response(content=content)
            self.client.authenticate(code='fake_code', redirect_uri='/')
        self.assertEqual(self.client.access_token, content['access_token'])

    def test_authenticate_code_already_used_or_expired(self):
        content = {
            u'status': 400,
            u'message': (u'Error validating grant. Your authorization code or '
                         u'refresh token may be expired or it was '
                         u'already used.'),
            u'cause': [],
            u'error': u'invalid_grant'
        }
        with patch.object(requests, 'post') as mocked_method:
            mocked_method.return_value = self._fake_response(
                status=400, content=content)
            self.assertRaises(
                requests.exceptions.HTTPError,
                self.client.authenticate,
                code='fake_code',
                redirect_uri='/'
            )
