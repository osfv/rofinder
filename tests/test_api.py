import requests

import api as api_module


class FailingSession:
    headers = {}

    def request(self, method, url, **kwargs):
        raise requests.Timeout("slow upstream")


def test_request_records_last_error_for_network_failures():
    api = api_module.RobloxAPI()
    api.session = FailingSession()

    assert api._request("GET", "https://users.roproxy.com/v1/users/1") is None

    assert isinstance(api.last_error, api_module.RobloxAPIError)
    assert "GET https://users.roproxy.com/v1/users/1" in str(api.last_error)
    assert "slow upstream" in str(api.last_error)
