from unittest import TestCase

from mercadolibre.auth import Credentials
from mercadolibre import api, MercadoLibre

from .fixtures import auth_fixtures


class APITestCase(TestCase):
    """Tests the main API of the client.
    The API should be accessed through mercadolibre.api.login()
    """
    def setUp(self):
        self.credentials = Credentials(
            app_id=auth_fixtures.APP_ID,
            app_secret=auth_fixtures.APP_SECRET)
        self.authenticated_credentials = Credentials(
            app_id=auth_fixtures.APP_ID,
            app_secret=auth_fixtures.APP_SECRET,
            access_token=auth_fixtures.ACCESS_TOKEN)

    def test_wrong_arguments_raise_exception(self):
        """Should raise an AttributeError if the wrong arguments are provided to login"""
        with self.assertRaises(AttributeError):
            api.login(auth_fixtures.APP_ID, auth_fixtures.APP_SECRET)

    def test_api_login_returns_the_correct_class_with_params(self):
        """Should return the correct API class when using parameters to login"""
        ml = api.login(
            app_id=auth_fixtures.APP_ID,
            app_secret=auth_fixtures.APP_SECRET)

        self.assertEqual(ml.__class__, MercadoLibre)
        self.assertEqual(ml.credentials.app_id, auth_fixtures.APP_ID)
        self.assertEqual(ml.credentials.app_secret, auth_fixtures.APP_SECRET)

    def test_api_login_returns_the_correct_class_with_creds(self):
        """Should return the correct API class when credentials are provided"""
        ml = api.login(self.credentials)

        self.assertEqual(ml.__class__, MercadoLibre)
        self.assertEqual(ml.credentials.app_id, auth_fixtures.APP_ID)
        self.assertEqual(ml.credentials.app_secret, auth_fixtures.APP_SECRET)

    def test_api_is_not_authenticated_without_access_token(self):
        """An api without an access_token should NOT be authenticated"""
        ml = api.login(
            app_id=auth_fixtures.APP_ID, app_secret=auth_fixtures.APP_SECRET)
        self.assertFalse(ml.is_authenticated)

    def test_api_is_authenticated_with_access_token(self):
        """An api with an access_token should be authenticated"""
        ml = api.login(
            app_id=auth_fixtures.APP_ID, app_secret=auth_fixtures.APP_SECRET,
            access_token=auth_fixtures.ACCESS_TOKEN)
        self.assertTrue(ml.is_authenticated)