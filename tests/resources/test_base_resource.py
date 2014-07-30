from mock import patch, MagicMock
from requests import Response

from mercadolibre.resources import BaseResource, SearchableResourceMixin

from .base import BaseAuthenticatedTestCase
from ..fixtures import dummy_fixtures


class DummyResource(SearchableResourceMixin, BaseResource):
    RESOURCE_NAME = 'dummy'

    @classmethod
    def get_iterator_for_collection(cls):
        from mercadolibre.iterators import BaseMercadoLibreIterator
        return BaseMercadoLibreIterator


class TestBaseResourceInitialization(BaseAuthenticatedTestCase):

    def test_build_object_from_response_content(self):
        """Should have instance attributes and preserved original response"""
        obj = DummyResource.build_object_from_dict(
            {'a': 1, 'b': 2},
            credentials=self.credentials)

        # The content of the response is preserved
        self.assertEqual(obj._data, {'a': 1, 'b': 2})

        # Data is set as instance attributes
        self.assertEqual(obj.a, 1)
        self.assertEqual(obj.b, 2)

        # Credentials are preserved
        self.assertEqual(obj.credentials, self.credentials)

    def test_collection_endpoint(self):
        self.assertEqual(
            DummyResource.get_collection_resource_endpoint('search'),
            "https://api.mercadolibre.com/{0}/search".format(
                DummyResource.RESOURCE_NAME)
        )

    def test_collection_iterator_without_pagination(self):
        data = dummy_fixtures.DUMMY_COLLECTION_FROM_MLA_SEARCH

        with patch.object(BaseResource, '_get') as _mock:
            response = MagicMock(spec=Response, ok=True, status_code=200)
            response.json = MagicMock(return_value=data)
            _mock.return_value = response

            it = DummyResource.search(credentials=self.credentials)
            self.assertEqual(_mock.call_count, 1)

        obj1 = next(it)
        self.assertEqual(obj1.id, "MLA502003454")

        obj2 = next(it)
        self.assertEqual(obj2.id, "MLA504842874")

        obj3 = next(it)
        self.assertEqual(obj3.id, "MLA497525770")

        with self.assertRaises(StopIteration):
            next(it)

    def test_collection_iterator_with_pagination(self):
        page_1 = dummy_fixtures.DUMMY_COLLECTION_FROM_MLA_SEARCH_PAGE_1
        page_2 = dummy_fixtures.DUMMY_COLLECTION_FROM_MLA_SEARCH_PAGE_2

        with patch.object(BaseResource, '_get') as _mock:
            response = MagicMock(spec=Response, ok=True, status_code=200)
            response.json = MagicMock(return_value=page_1)
            _mock.return_value = response

            it = DummyResource.search(credentials=self.credentials)
            self.assertEqual(_mock.call_count, 1)

        obj1 = next(it)
        self.assertEqual(obj1.id, "MLA502003454")

        obj2 = next(it)
        self.assertEqual(obj2.id, "MLA504842874")

        obj3 = next(it)
        self.assertEqual(obj3.id, "MLA497525770")

        with patch.object(BaseResource, '_get') as _mock:
            response = MagicMock(spec=Response, ok=True, status_code=200)
            response.json = MagicMock(return_value=page_2)
            _mock.return_value = response

            obj4 = next(it)
            self.assertEqual(obj4.id, "MLA499776777")

            # Called to get the fourth result
            self.assertEqual(_mock.call_count, 1)

            self.assertTrue('params' in _mock.call_args[1])
            self.assertTrue('offset' in _mock.call_args[1]['params'])
            self.assertEqual(_mock.call_args[1]['params']['offset'], 3)

            obj5 = next(it)
            self.assertEqual(obj5.id, "MLA503203012")

        with self.assertRaises(StopIteration):
            next(it)

    def test_collection_iterator_with_pagination_and_offset(self):
        page_2 = dummy_fixtures.DUMMY_COLLECTION_FROM_MLA_SEARCH_PAGE_2

        with patch.object(BaseResource, '_get') as _mock:
            response = MagicMock(spec=Response, ok=True, status_code=200)
            response.json = MagicMock(return_value=page_2)
            _mock.return_value = response

            it = DummyResource.search(offset=3, credentials=self.credentials)
            self.assertEqual(_mock.call_count, 1)

        obj1 = next(it)
        self.assertEqual(obj1.id, "MLA499776777")

        obj2 = next(it)
        self.assertEqual(obj2.id, "MLA503203012")

        with patch.object(BaseResource, '_get') as _mock:
            response = MagicMock(spec=Response, ok=True, status_code=200)
            response.json = MagicMock(return_value=page_2)
            _mock.return_value = response
            with self.assertRaises(StopIteration):
                next(it)
            self.assertEqual(_mock.call_count, 0)
