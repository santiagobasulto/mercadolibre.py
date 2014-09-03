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


class BaseSearchTestCase(BaseAuthenticatedTestCase):
    def setUp(self):
        super(BaseSearchTestCase, self).setUp()
        self.client = api.login(self.credentials)

    def load_json_fixture(self, file_name):
        fixtures_path = _j(dn(dn(os.path.realpath(__file__))), 'fixtures')
        base_path = _j(_j(fixtures_path, 'search'), file_name)
        with open(base_path, 'r') as f:
            return json.loads(f.read())


class SearchItemsTestCase(BaseSearchTestCase):
    def test_search_by_query_string(self):
        """Should search by QS and return an iterator"""
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

    def test_search_by_query_string_and_category_with_id(self):
        """Should search by QS and category and return an iterator"""
        content = self.load_json_fixture(
            "samsung_qs_and_category_search_result.json")

        with patch.object(BaseResource, '_get') as _mock:
            response = MagicMock(spec=Response, ok=True, status_code=200)
            response.json = MagicMock(return_value=content)
            _mock.return_value = response

            # High level API access
            iterator = self.client.mla.search(
                q="Samsung", category_id="MLA12272")

        args = _mock.call_args[1]
        self.assertTrue('params' in args)
        self.assertEqual(args['params'].get('q'), 'Samsung')
        self.assertEqual(args['params'].get('category'), 'MLA12272')

        self.assertTrue(isinstance(iterator, BaseMercadoLibreIterator))
        self.assertEqual(iterator.query, 'Samsung')
        self.assertTrue(isinstance(iterator.available_filters, list))
        self.assertTrue(len(iterator.available_filters) > 0)

        self.assertEqual(iterator.total_count, 1)
        self.assertEqual(iterator.limit, None)
        self.assertEqual(iterator.prev_offset, 0)
        self.assertEqual(iterator.offset, 50)

        obj1 = next(iterator)
        self.assertTrue(isinstance(obj1, ItemResource))

        self.assertEqual(obj1.id, "MLA512445905")
        self.assertEqual(
            obj1.title,
            "Samsung Gear Fit Para S4 S5 Note Ritmo Cardiaco")

    def test_search_by_seller_nickname(self):
        """Should search by seller nickname and return an iterator"""
        content = self.load_json_fixture(
            "seller_by_nickname_laplata_notebooks.json")

        with patch.object(BaseResource, '_get') as _mock:
            response = MagicMock(spec=Response, ok=True, status_code=200)
            response.json = MagicMock(return_value=content)
            _mock.return_value = response

            # High level API access
            iterator = self.client.mla.search(nickname="LAPLATA-NOTEBOOKS")

        args = _mock.call_args[1]
        self.assertTrue('params' in args)

        self.assertEqual(args['params'].get('nickname'), 'LAPLATA-NOTEBOOKS')

        self.assertTrue(isinstance(iterator, BaseMercadoLibreIterator))
        self.assertIsNone(iterator.query)
        self.assertTrue(isinstance(iterator.seller, dict))
        self.assertTrue(isinstance(iterator.available_filters, list))
        self.assertTrue(len(iterator.available_filters) > 0)

        self.assertEqual(iterator.total_count, 70)
        self.assertEqual(iterator.limit, None)
        self.assertEqual(iterator.prev_offset, 0)
        self.assertEqual(iterator.offset, 50)

        obj1 = next(iterator)
        self.assertTrue(isinstance(obj1, ItemResource))

        self.assertEqual(obj1.id, "MLA508081074")
        self.assertEqual(
            obj1.title,
            "Notebook Sony Vaio I3 6gb 750gb Tecl. Iluminado Fact. A O B")

    def test_search_by_seller_id(self):
        """Should search by seller ID and return an iterator"""
        content = self.load_json_fixture(
            "seller_by_nickname_laplata_notebooks.json")

        with patch.object(BaseResource, '_get') as _mock:
            response = MagicMock(spec=Response, ok=True, status_code=200)
            response.json = MagicMock(return_value=content)
            _mock.return_value = response

            # High level API access
            iterator = self.client.mla.search(seller_id="38726013")

        args = _mock.call_args[1]
        self.assertTrue('params' in args)

        self.assertEqual(args['params'].get('seller_id'), '38726013')

        self.assertTrue(isinstance(iterator, BaseMercadoLibreIterator))
        self.assertIsNone(iterator.query)
        self.assertTrue(isinstance(iterator.seller, dict))
        self.assertTrue(isinstance(iterator.available_filters, list))
        self.assertTrue(len(iterator.available_filters) > 0)

        self.assertEqual(iterator.total_count, 70)
        self.assertEqual(iterator.limit, None)
        self.assertEqual(iterator.prev_offset, 0)
        self.assertEqual(iterator.offset, 50)

        obj1 = next(iterator)
        self.assertTrue(isinstance(obj1, ItemResource))

        self.assertEqual(obj1.id, "MLA508081074")
        self.assertEqual(
            obj1.title,
            "Notebook Sony Vaio I3 6gb 750gb Tecl. Iluminado Fact. A O B")


spec = """
ml.mla.search(q="Jawbone Up24")  # Done

# By Category
ml.mla.search(category_id='MLA12345')  # Done
ml.mla.search(category=ml.categories.get(id='MLA12345'))  # Won't fix

# By Seller
ml.mla.search(nickname='SANBASULTO_04')  # Done
ml.mla.search(seller_id='MLA12345')  # Done
ml.mla.search(seller=ml.mla.users.get(id='MLA12345'))  # Won't fix
"""
