import os
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from version import APP_NAME, VERSION, AUTHOR

DEFAULT_TIMEOUT = 12
DEFAULT_RETRIES = 3
CACHE_TTL_SECONDS = 60
API_DOMAIN = os.getenv("ROFINDER_API_DOMAIN", "roproxy.com")


def _build_retry():
    try:
        return Retry(
            total=DEFAULT_RETRIES,
            connect=DEFAULT_RETRIES,
            read=DEFAULT_RETRIES,
            status=DEFAULT_RETRIES,
            backoff_factor=0.4,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=("GET", "POST"),
            respect_retry_after_header=True,
        )
    except TypeError:
        return Retry(
            total=DEFAULT_RETRIES,
            connect=DEFAULT_RETRIES,
            read=DEFAULT_RETRIES,
            status=DEFAULT_RETRIES,
            backoff_factor=0.4,
            status_forcelist=(429, 500, 502, 503, 504),
            method_whitelist=("GET", "POST"),
            respect_retry_after_header=True,
        )


class RobloxAPI:
    def __init__(self, timeout=DEFAULT_TIMEOUT, api_domain=API_DOMAIN):
        self.timeout = timeout
        self.api_domain = api_domain
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": f"{APP_NAME}/{VERSION} ({AUTHOR})",
            "Accept": "application/json"
        })

        retry = _build_retry()
        adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=10)
        self.session.mount("https://", adapter)

        self._cache = {}

    def _url(self, service, path):
        return f"https://{service}.{self.api_domain}{path}"

    def _cache_get(self, key):
        entry = self._cache.get(key)
        if not entry:
            return None
        value, expires_at = entry
        if time.time() > expires_at:
            self._cache.pop(key, None)
            return None
        return value

    def _cache_set(self, key, value, ttl=CACHE_TTL_SECONDS):
        self._cache[key] = (value, time.time() + ttl)

    def _request(self, method, url, **kwargs):
        try:
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            if response.headers.get("content-type", "").startswith("application/json"):
                return response.json()
            return None
        except requests.RequestException:
            return None

    def _paginate(self, base_url, limit):
        results = []
        cursor = None
        page_size = min(max(limit, 1), 100)

        while len(results) < limit:
            cursor_param = f"&cursor={cursor}" if cursor else ""
            url = f"{base_url}&limit={page_size}{cursor_param}"
            data = self._request("GET", url)
            if not data:
                break
            results.extend(data.get('data', []))
            cursor = data.get('nextPageCursor')
            if not cursor:
                break

        return results[:limit]

    def resolve_user(self, user_input):
        if user_input.isdigit():
            user_id = int(user_input)
        else:
            user_id = self.get_id_by_username(user_input)

        if not user_id:
            return None, None

        user_info = self.get_user_info(user_id)
        if not user_info:
            return None, None

        return user_id, user_info

    def get_id_by_username(self, username):
        payload = {"usernames": [username], "excludeBannedUsers": False}
        data = self._request("POST", self._url("users", "/v1/usernames/users"), json=payload)
        results = data.get('data', []) if data else []
        return results[0].get('id') if results else None

    def get_user_info(self, user_id):
        cache_key = f"user:{user_id}"
        cached = self._cache_get(cache_key)
        if cached:
            return cached

        data = self._request("GET", self._url("users", f"/v1/users/{user_id}"))
        if data:
            self._cache_set(cache_key, data)
        return data

    def get_premium_status(self, user_id):
        data = self._request("GET", self._url("premium", f"/v1/users/{user_id}/premium-features"))
        if not data:
            return False
        return data.get('subscriptionProductModel', {}).get('renewalPeriod') is not None

    def get_presence(self, user_id):
        payload = {"userIds": [user_id]}
        data = self._request("POST", self._url("presence", "/v1/presence/users"), json=payload)
        presences = data.get('userPresences', []) if data else []
        return presences[0] if presences else None

    def get_friends_count(self, user_id):
        data = self._request("GET", self._url("friends", f"/v1/users/{user_id}/friends/count"))
        return data.get('count', 0) if data else 0

    def get_followers_count(self, user_id):
        data = self._request("GET", self._url("friends", f"/v1/users/{user_id}/followers/count"))
        return data.get('count', 0) if data else 0

    def get_following_count(self, user_id):
        data = self._request("GET", self._url("friends", f"/v1/users/{user_id}/following/count"))
        return data.get('count', 0) if data else 0

    def get_friends_list(self, user_id, limit=50):
        base_url = self._url("friends", f"/v1/users/{user_id}/friends?sortOrder=Asc")
        return self._paginate(base_url, limit)

    def get_badges(self, user_id, limit=10):
        base_url = self._url("badges", f"/v1/users/{user_id}/badges?sortOrder=Desc")
        return self._paginate(base_url, limit)

    def get_groups(self, user_id, limit=10):
        data = self._request("GET", self._url("groups", f"/v1/users/{user_id}/groups/roles"))
        groups = data.get('data', []) if data else []
        return groups[:limit]

    def get_avatar_thumbnail(self, user_id, size="720x720"):
        cache_key = f"thumb:{user_id}:{size}"
        cached = self._cache_get(cache_key)
        if cached:
            return cached

        path = f"/v1/users/avatar-headshot?userIds={user_id}&size={size}&format=Png&isCircular=false"
        data = self._request("GET", self._url("thumbnails", path))
        records = data.get('data', []) if data else []
        image_url = records[0].get('imageUrl') if records else "N/A"
        if image_url:
            self._cache_set(cache_key, image_url)
        return image_url

    def get_currently_wearing(self, user_id):
        data = self._request("GET", self._url("avatar", f"/v1/users/{user_id}/avatar"))
        return data.get('assets', []) if data else []

    def get_favorites(self, user_id, limit=50):
        base_url = self._url("games", f"/v2/users/{user_id}/favorite/games?sortOrder=Desc")
        return self._paginate(base_url, limit)
