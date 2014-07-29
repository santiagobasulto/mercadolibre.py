from unittest import TestCase

from mock import patch, MagicMock
from requests import Response

from mercadolibre import api
from mercadolibre import http
from mercadolibre.resources import BaseResource

from .base import BaseAuthenticatedTestCase
from ..fixtures import user_fixtures


class UserResourceTestCase(BaseAuthenticatedTestCase):
    def test_me(self):
        """Should return the proper UserResource with my information.
        """
        client = api.login(self.credentials)
        with patch.object(BaseResource, '_get') as _mock:
            response = MagicMock(spec=Response, ok=True, status_code=201)
            response.json = MagicMock(
                return_value=user_fixtures.BASE_USER)
            _mock.return_value = response
            me = client.me()

        self.assertEqual(str(me.id), '82365164')
        self.assertEqual(me.site_id, 'MLA')
