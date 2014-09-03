from mercadolibre import api
from mercadolibre.iterators import BaseMercadoLibreIterator

from . import vcr_conf, BaseVCRIntegrationTestCase, requires_access_token
from .data import TEST_ITEM_1


class ItemPostTestCase(BaseVCRIntegrationTestCase):
    @vcr_conf.use_cassette('items.yaml')
    @requires_access_token
    def test_user_creates_and_get_item(self):
        client = api.login(
            app_id=self.app_id, app_secret=self.app_secret,
            access_token=self.access_token)
        post_item = client.items.post(data=TEST_ITEM_1)
        self.assertIsNotNone(
            post_item.id, "The created item doesn't have an id")
        self.assertIsNotNone(
            post_item.permalink, "The created item doesn't have an permalink")
        self.assertEqual(
            len(post_item.pictures), 1, "The created item doesn't pictures")

        get_item = client.items.get(id=post_item.id)
        self.assertEqual(get_item.id, post_item.id)
        self.assertEqual(get_item.permalink, post_item.permalink)
        self.assertEqual(get_item.category_id, post_item.category_id)

    @vcr_conf.use_cassette('items_search.yaml')
    def test_search_on_mla_site(self):
        client = api.login(
            app_id=self.app_id, app_secret=self.app_secret)
        q = 'Samsung S3'
        result_iterator = client.mla.search(q=q)

        self.assertTrue(isinstance(result_iterator, BaseMercadoLibreIterator))
        self.assertEqual(result_iterator.query, q)
        self.assertTrue(isinstance(result_iterator.available_filters, list))
        self.assertTrue(len(result_iterator.available_filters) > 0)

        self.assertTrue(result_iterator.total_count > 0)
        self.assertEqual(result_iterator.limit, None)
        self.assertEqual(result_iterator.prev_offset, 0)
        self.assertEqual(result_iterator.offset, 50)

        # Should get the next page. This might take a while
        for _ in range(51):
            item = next(result_iterator)
            self.assertIsNotNone(item.id)
            self.assertIsNotNone(item.permalink)
            self.assertIsNotNone(item.category_id)