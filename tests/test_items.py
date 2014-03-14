# -*- coding: utf-8 -*-
import requests
from mock import patch

from . import MercadoLibreBaseTestCase


class TestMercadoLibreItems(MercadoLibreBaseTestCase):

    def test_create_item(self):
        content = {
            u'id': u'MLA872398279',
            u'title': 'test item'
        }
        with patch.object(requests, 'post') as mocked_method:
            mocked_method.return_value = self._fake_response(content=content)
            item = self.client.create_item(data={'title': 'test  item'})
        self.assertTrue(isinstance(item, dict))
        self.assertEqual(item['title'], u'test item')

    def test_create_item_invalid_body(self):
        content = {
            u'cause': [
                {u'code': u'item.attributes.missing_required',
                 u'message': u'error message'}
            ],
            u'error': u'validation_error',
            u'message': u'Validation error',
            u'status': 400
        }
        with patch.object(requests, 'post') as mocked_method:
            mocked_method.return_value = self._fake_response(
                status=400, content=content)
            self.assertRaises(
                requests.exceptions.HTTPError,
                self.client.create_item,
                data={u'title': 'test item'}
            )
