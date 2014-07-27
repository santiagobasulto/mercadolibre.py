class Credentials(object):
    """Credentials used by mercadolibre.py to authenticate itself.
    The credential can represent both "authentication" and "authorization".

    Authentication requires a valid `app_id` and a valid `app_secret` and
    tells MercadoLibre "who" the client is.
    Authentication answers "who you are".

    Authorization requires a valid `access_token` (and optionally a
    `refresh_token`). That tells MercadoLibre if the client is "authorized"
    to perform certain action.
    Authentication answers "are you allowed to perform certain action".
    """
    def __init__(
            self, app_id, app_secret, access_token=None, refresh_token=None):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = access_token
        self.refresh_token = refresh_token

    def is_authenticated(self):
        return bool(self.app_id) and bool(self.app_secret)

    def is_authorized(self):
        return self.access_token is not None

    def is_refreshable(self):
        return self.refresh_token is not None

    # def is_active(self):
    #     return self.is_authenticated() and self._is_access_token_valid()