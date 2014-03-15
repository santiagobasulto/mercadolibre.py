# -*- coding: utf-8 -*-
import json
import requests
import unittest

from mercadolibre import MercadoLibre


class MercadoLibreBaseTestCase(unittest.TestCase):
    def setUp(self):
        self.client = MercadoLibre(app_id='test', app_secret='test')

    def _fake_response(self, status=200, content=None):
        response = requests.Response()
        response.status_code = status
        if content is not None:
            if isinstance(content, dict):
                content = json.dumps(content)
            response._content = content
        return response
