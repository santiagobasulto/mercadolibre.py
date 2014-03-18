from unittest import TestCase

from betamax import Betamax
from mock import patch

from mercadolibre import api
from mercadolibre import http

with Betamax.configure() as config:
    config.cassette_library_dir = 'tests/fixtures/cassettes'


APP_ID = '554056882653189'
APP_SECRET = 'a8hWBhGCbgNXhMuHrZM8nmGXLRL6wpXc'
ACCESS_TOKEN = "APP_USR-554056882653189-031816-50da07536429acf9d44587d7a488fa1b__H_F__-82365164"


class UserResourceTestCase(TestCase):
    def setUp(self):
        self.session = http.get_session()

    def test_me(self):
        """Should return the proper UserResource with my information.
        """
        with Betamax(self.session) as vcr:
            with patch.object(http, 'get_session') as m:
                m.return_value = self.session
                vcr.use_cassette('users')
                ml = api.login(APP_ID, APP_SECRET, ACCESS_TOKEN)
                me = ml.me()
                self.assertEqual(str(me.id), '82365164')
                self.assertEqual(me.site_id, 'MLA')
