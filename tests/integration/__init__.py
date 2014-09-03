import os
from unittest import TestCase
from copy import deepcopy
from functools import wraps

import vcr
import pytest

from mercadolibre.auth import Credentials

ML_APP_ID = "XXX"
ML_APP_SECRET = "YYY"

__all__ = ['BaseVCRIntegrationTestCase', 'vcr_conf', 'requires_access_token']


@pytest.mark.integration
class BaseVCRIntegrationTestCase(TestCase):
    def setUp(self):
        self.app_id = ML_APP_ID
        self.app_secret = ML_APP_SECRET
        self.access_token = (getattr(self, 'access_token', None) or
                             os.environ.get('ML_TESTING_ACCESS_TOKEN'))
        self.credentials = Credentials(
            app_id=ML_APP_ID, app_secret=ML_APP_SECRET,
            access_token=self.access_token
        )


def requires_access_token(method):
    @wraps(method)
    def inner(self, *args, **kwargs):
        if not self.access_token:
            raise Exception(
                "You must provide a testing access token to run integration "
                "test cases.\n"
                "Try this: "
                "$ ML_TESTING_ACCESS_TOKEN=XXX py.test tests/integration")
        return method(self, *args, **kwargs)
    return inner


def mercadolibre_query_matcher(new_req, prev_req):
    """
    Matches 2 requests to MercadoLibre API. Will avoid matching the
    access_token param (if any).
    """
    def filter_query(request):
        return [q for q in deepcopy(request.query) if q[0] != 'access_token']
    return filter_query(new_req) == filter_query(prev_req)

vcr_conf = vcr.VCR(
    record_mode=os.environ.get('ML_TESTS_RECORD_MODE', 'once'),
    cassette_library_dir='tests/fixtures/cassettes/',
    match_on=[
        'method',
        'scheme',
        'host',
        'port',
        'path'
    ]
)

vcr_conf.register_matcher(
    'mercadolibre_query_matcher', mercadolibre_query_matcher)
vcr_conf.match_on += ['mercadolibre_query_matcher']