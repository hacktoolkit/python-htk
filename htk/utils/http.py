# Third Party (PyPI) Imports
from requests.auth import AuthBase


class HTTPBearerAuth(AuthBase):
    """Bearer Authorization

    Usage: `requests.post(url, auth=HTTPBearerAuth(...))`
    """

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = "Bearer {}".format(self.token)
        return r
