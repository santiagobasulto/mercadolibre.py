from unittest import TestCase

from mercadolibre.auth import Credentials

from ..fixtures import auth_fixtures


class BaseAuthenticatedTestCase(TestCase):
    def setUp(self):
        self.credentials = Credentials(
            app_id=auth_fixtures.APP_ID, app_secret=auth_fixtures.APP_SECRET,
            access_token=auth_fixtures.ACCESS_TOKEN)
        self.maxDiff = None
