from mercadolibre import api
from mercadolibre.resources import UserResource

from . import vcr_conf, BaseVCRIntegrationTestCase, requires_access_token


class UserResourceTestCase(BaseVCRIntegrationTestCase):
    @vcr_conf.use_cassette('users.yaml')
    @requires_access_token
    def test_user_me_with_resource(self):
        """Should return the data from the user using the mid-level api
        """
        user = UserResource.get("me", credentials=self.credentials)
        self.assertEqual(user.id, 165949089)
        self.assertEqual(user.nickname, 'TT681357')
        self.assertEqual(user.email, 'test_user_50000654@testuser.com')

    @vcr_conf.use_cassette('users.yaml')
    @requires_access_token
    def test_user_me_with_api(self):
        """Should return the data from the user using the high-level api
        """
        client = api.login(
            app_id=self.app_id, app_secret=self.app_secret,
            access_token=self.access_token)
        user = client.me()

        self.assertEqual(user.id, 165949089)
        self.assertEqual(user.nickname, 'TT681357')
        self.assertEqual(user.email, 'test_user_50000654@testuser.com')

    @vcr_conf.use_cassette('users.yaml')
    @requires_access_token
    def test_create_mla_test_user(self):
        """Should create a test user and return its data
        """
        client = api.login(
            app_id=self.app_id, app_secret=self.app_secret,
            access_token=self.access_token)
        user = client.test_user.post({'site_id': 'MLA'})

        self.assertIsNotNone(user.id)
        self.assertIsNotNone(user.nickname)
        self.assertIsNotNone(user.email)