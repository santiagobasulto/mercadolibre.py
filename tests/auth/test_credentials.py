from unittest import TestCase

from mercadolibre.auth import Credentials

from ..fixtures import auth_fixtures


class TestCredentials(TestCase):

    def test_is_authenticated(self):
        """Should return True if app_id and app_secret is provided"""
        cred = Credentials(
            app_id=auth_fixtures.APP_ID,
            app_secret=auth_fixtures.APP_SECRET)

        self.assertTrue(cred.is_authenticated())

    def test_is_not_authenticated(self):
        """Should return True if app_id and app_secret is provided"""
        cred = Credentials(app_id=None, app_secret=None)

        self.assertFalse(cred.is_authenticated())

    def test_is_authorized(self):
        """Should return True if an access token is provided"""
        cred = Credentials(
            app_id=auth_fixtures.APP_ID,
            app_secret=auth_fixtures.APP_SECRET,
            access_token=auth_fixtures.ACCESS_TOKEN)

        self.assertTrue(cred.is_authenticated())
        self.assertTrue(cred.is_authorized())

    def test_is_not_authorized(self):
        """Should return False if an access token is NOT provided"""
        cred = Credentials(
            app_id=auth_fixtures.APP_ID,
            app_secret=auth_fixtures.APP_SECRET)

        self.assertTrue(cred.is_authenticated())
        self.assertFalse(cred.is_authorized())

    def test_is_refreshable(self):
        """Should return True if a refresh token is provided"""
        cred = Credentials(
            app_id=auth_fixtures.APP_ID,
            app_secret=auth_fixtures.APP_SECRET,
            access_token=auth_fixtures.ACCESS_TOKEN,
            refresh_token=auth_fixtures.REFRESH_TOKEN)

        self.assertTrue(cred.is_refreshable())

    def test_is_not_refreshable(self):
        """Should return False if a refresh token is NOT provided"""
        cred = Credentials(
            app_id=auth_fixtures.APP_ID,
            app_secret=auth_fixtures.APP_SECRET)

        self.assertFalse(cred.is_refreshable())