# -*- coding: utf-8 -*-
from . import __version__


API_ROOT = 'https://api.mercadolibre.com'
AUTH_URL = 'https://auth.mercadolibre.com/authorization'
OAUTH_URL = '{0}{1}'.format(API_ROOT, '/oauth/token')
USER_AGENT = 'mercadolibre.py-v{version}'.format(version=__version__)
JSON_MIME_TYPE = 'application/json'
CHARACTER_SET = 'utf-8'
