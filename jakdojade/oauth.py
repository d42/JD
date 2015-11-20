import logging
import requests
from oauthlib.oauth1 import Client

from .decorators import cached_request
from .utils import url_set_params

logger = logging.getLogger()


class OauthRequests:
    def __init__(self, secret_key, client_key, defaults=None):
        self.defaults = {
            "devId": "c55b00b5-dead-beef-cafe-babefac3b001",
            "user-agent": "Samsung - 4.4.2 - API 19 - 1024x600 Android 4.4.2",
            "locale": "en"
        }

        if defaults:
            self.defaults.update(defaults)
        self.secret_key = secret_key
        self.client_key = client_key
        self.oauth = Client(client_key, client_secret=secret_key)

    @cached_request
    def __call__(self, url, params=None):
        params = params or {}
        url = url_set_params(url, params)
        url, headers, _ = self.oauth.sign(url)
        headers.update(self.defaults)
        req = requests.get(url, headers=headers)

        if req.status_code != 200:
            logging.error("code %d: %s", req.status_code, req.text)
        return req
