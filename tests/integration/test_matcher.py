import mock

from unittest import TestCase
from . import mercadolibre_query_matcher


class RequestMocked(mock.MagicMock):
    pass


class MercadoLibreMatcherTestCase(TestCase):
    def test_equal_access_token_without_other_params(self):
        """Should return true if equal access tokens are passed and there are no other params"""
        r1 = RequestMocked()
        r1.query = [('access_token', 'APP_USR-XXX-YYY')]
        r2 = RequestMocked()
        r2.query = [('access_token', 'APP_USR-XXX-YYY')]

        self.assertTrue(mercadolibre_query_matcher(r1, r2))

    def test_different_access_token_without_other_params(self):
        """Should return true if different access tokens are the only queries"""
        r1 = RequestMocked()
        r1.query = [('access_token', 'APP_USR-XXX-YYY')]
        r2 = RequestMocked()
        r2.query = [('access_token', 'APP_USR-XXX-UUU')]

        self.assertTrue(mercadolibre_query_matcher(r1, r2))

    def test_equal_access_token_with_equal_other_params(self):
        """Should return true if equal access tokens are passed and there are other params equals"""
        r1 = RequestMocked()
        r1.query = [('access_token', 'APP_USR-XXX-YYY'), ('q', 'iPhone')]
        r2 = RequestMocked()
        r2.query = [('access_token', 'APP_USR-XXX-YYY'), ('q', 'iPhone')]

        self.assertTrue(mercadolibre_query_matcher(r1, r2))

    def test_different_access_token_with_equal_other_params(self):
        """Should return true if different access tokens are passed and there are other params equals"""
        r1 = RequestMocked()
        r1.query = [('access_token', 'APP_USR-XXX-YYY'), ('q', 'iPhone')]
        r2 = RequestMocked()
        r2.query = [('access_token', 'APP_USR-XXX-UUU'), ('q', 'iPhone')]

        self.assertTrue(mercadolibre_query_matcher(r1, r2))

    def test_equal_access_token_with_different_other_params(self):
        """Should return false if equal access tokens are passed but the other params are different"""
        r1 = RequestMocked()
        r1.query = [('access_token', 'APP_USR-XXX-YYY'), ('q', 'iPhone')]
        r2 = RequestMocked()
        r2.query = [('access_token', 'APP_USR-XXX-YYY'), ('q', 'iPad')]

        self.assertFalse(mercadolibre_query_matcher(r1, r2))

    def test_differetn_access_token_with_different_other_params(self):
        """Should return false if different access tokens are passed but the other params are different"""
        r1 = RequestMocked()
        r1.query = [('access_token', 'APP_USR-XXX-YYY'), ('q', 'iPhone')]
        r2 = RequestMocked()
        r2.query = [('access_token', 'APP_USR-XXX-UUU'), ('q', 'iPad')]

        self.assertFalse(mercadolibre_query_matcher(r1, r2))