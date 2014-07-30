import os
from os.path import dirname as dn
import json

from mock import patch, MagicMock
from requests import Response

from mercadolibre import api

from mercadolibre.resources import *
from mercadolibre.resources import BaseResource
from mercadolibre.iterators import BaseMercadoLibreIterator

from .base import BaseAuthenticatedTestCase

_j = os.path.join


class SearchItemsTestCase(BaseAuthenticatedTestCase):
    def setUp(self):
        super(SearchItemsTestCase, self).setUp()
        self.client = api.login(self.credentials)

    def load_json_fixture(self, file_name):
        fixtures_path = _j(dn(dn(os.path.realpath(__file__))), 'fixtures')
        base_path = _j(_j(fixtures_path, 'search'), file_name)
        with open(base_path, 'r') as f:
            return json.loads(f.read())

    def test_search_by_query_string(self):
        """Should search by QS and return a Search object"""
        content = self.load_json_fixture("samsung_s3_search_result.json")

        with patch.object(BaseResource, '_get') as _mock:
            response = MagicMock(spec=Response, ok=True, status_code=200)
            response.json = MagicMock(return_value=content)
            _mock.return_value = response

            # High level API access
            iterator = self.client.mla.search(q="Samsung S3")

        args = _mock.call_args[1]
        self.assertTrue('params' in args)
        self.assertEqual(args['params'].get('q'), 'Samsung S3')

        self.assertTrue(isinstance(iterator, BaseMercadoLibreIterator))
        self.assertEqual(iterator.query, 'Samsung S3')
        self.assertTrue(isinstance(iterator.available_filters, list))
        self.assertTrue(len(iterator.available_filters) > 0)

        self.assertEqual(iterator.total_count, 1340)
        self.assertEqual(iterator.limit, None)
        self.assertEqual(iterator.prev_offset, 0)
        self.assertEqual(iterator.offset, 50)

        obj1 = next(iterator)
        self.assertTrue(isinstance(obj1, ItemResource))

        self.assertEqual(obj1.id, "MLA515410700")
        self.assertEqual(
            obj1.title,
            "Celular Samsung Libre Galaxy S3 I9300 Quadcore 1.4ghz 16gb")

        obj2 = next(iterator)
        self.assertTrue(isinstance(obj2, ItemResource))

        self.assertEqual(obj2.id, "MLA509003727")
        self.assertEqual(
            obj2.title,
            "Celular Libre Samsung Galaxy S3 I9300 Quadcore 1.4ghz Led 4")


spec = """
ml.mla.search(q="Jawbone Up24")  # Done
ml.mla.search(q="Jawbone Up24", category=ml.categories.get(id='MLA12345')) ?

# By Category
ml.mla.search(category_id='MLA12345')
ml.mla.search(category=ml.categories.get(id='MLA12345'))

# By Seller
ml.mla.search(nickname='SANBASULTO_04')
ml.mla.search(seller_id='MLA12345')
ml.mla.search(seller=ml.mla.users.get(id='MLA12345'))
"""
