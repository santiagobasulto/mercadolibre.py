from mock import patch, MagicMock
from requests import Response

from mercadolibre import api

from mercadolibre.resources import *
from mercadolibre.resources import BaseResource

from .base import BaseAuthenticatedTestCase
from ..fixtures import item_fixtures


class ItemResourceLowLevelTestCase(BaseAuthenticatedTestCase):
    """Tests low level access and API to the Item Resource"""
    def test_get_an_item(self):
        item_id = "MLA503678087"

        with patch.object(BaseResource, '_get') as _mock:
            response = MagicMock(spec=Response, ok=True, status_code=200)
            response.json = MagicMock(
                return_value=item_fixtures.REAL_ITEM_FROM_MLA)
            _mock.return_value = response

            # Low level API access
            item = ItemResource.get(id=item_id, credentials=self.credentials)

        self.assertEqual(item.id, item_id)
        self.assertTrue(hasattr(item, 'permalink'))
        self.assertIsNotNone(item.permalink)

    def test_post_an_item(self):
        data = item_fixtures.BASIC_TEST_ITEM_FOR_CREATION_1

        with patch.object(BaseResource, '_post') as _mock:
            response = MagicMock(spec=Response, ok=True, status_code=201)
            response.json = MagicMock(
                return_value=item_fixtures.BASIC_TEST_ITEM_CREATED_1)
            _mock.return_value = response

            # Low level API access
            item = ItemResource.post(data=data, credentials=self.credentials)

        self.assertTrue(hasattr(item, 'id'))
        self.assertIsNotNone(item.id)

        self.assertTrue(hasattr(item, 'permalink'))
        self.assertIsNotNone(item.permalink)


class ItemResourceMidLevelTestCase(BaseAuthenticatedTestCase):
    def test_get_an_item(self):
        item_id = "MLA503678087"
        ItemResource.credentials = self.credentials

        with patch.object(BaseResource, '_get') as _mock:
            response = MagicMock(spec=Response, ok=True, status_code=200)
            response.json = MagicMock(
                return_value=item_fixtures.REAL_ITEM_FROM_MLA)
            _mock.return_value = response

            # Mid level API access
            item = ItemResource.get(id=item_id)

        self.assertEqual(item.id, item_id)
        self.assertTrue(hasattr(item, 'permalink'))
        self.assertIsNotNone(item.permalink)

    def test_post_an_item(self):
        data = item_fixtures.BASIC_TEST_ITEM_FOR_CREATION_1
        ItemResource.credentials = self.credentials

        with patch.object(BaseResource, '_post') as _mock:
            response = MagicMock(spec=Response, ok=True, status_code=201)
            response.json = MagicMock(
                return_value=item_fixtures.BASIC_TEST_ITEM_CREATED_1)
            _mock.return_value = response

            # Mid level API access
            item = ItemResource.post(data=data)

        self.assertTrue(hasattr(item, 'id'))
        self.assertIsNotNone(item.id)

        self.assertTrue(hasattr(item, 'permalink'))
        self.assertIsNotNone(item.permalink)


class ItemResourceHighLevelTestCase(BaseAuthenticatedTestCase):
    def setUp(self):
        super(ItemResourceHighLevelTestCase, self).setUp()
        self.client = api.login(self.credentials)

    def test_item_resource_is_present_on_api(self):
        """ItemResource should be accessible from the API"""
        self.assertEqual(self.client.items, ItemResource)

    def test_get_an_item(self):
        item_id = "MLA503678087"
        with patch.object(BaseResource, '_get') as _mock:
            response = MagicMock(spec=Response, ok=True, status_code=200)
            response.json = MagicMock(
                return_value=item_fixtures.REAL_ITEM_FROM_MLA)
            _mock.return_value = response

            # High level API access
            item = self.client.items.get(id=item_id)

        self.assertEqual(item.id, item_id)
        self.assertTrue(hasattr(item, 'permalink'))
        self.assertIsNotNone(item.permalink)

    def test_post_an_item(self):
        data = item_fixtures.BASIC_TEST_ITEM_FOR_CREATION_1

        with patch.object(BaseResource, '_post') as _mock:
            response = MagicMock(spec=Response, ok=True, status_code=201)
            response.json = MagicMock(
                return_value=item_fixtures.BASIC_TEST_ITEM_CREATED_1)
            _mock.return_value = response

            # High level API access
            item = self.client.items.post(data=data)

        # kwargs = _mock.call_args[1]
        # self.assertEqual(_mock.call_count, 1)
        # self.assertIsNotNone(
        #     kwargs.get('credentials'),
        #     "POST should have been called with credentials")

        self.assertTrue(hasattr(item, 'id'))
        self.assertIsNotNone(item.id)

        self.assertTrue(hasattr(item, 'permalink'))
        self.assertIsNotNone(item.permalink)


# class DescriptionResourceLowLevelTestCase(BaseAuthenticatedTestCase):
#     def test_add_description_to_item(self):
#         ItemDescriptionResource.post()