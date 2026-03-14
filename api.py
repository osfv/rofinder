import requests
from version import APP_NAME, VERSION, AUTHOR

class RobloxAPI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": f"{APP_NAME}/{VERSION} ({AUTHOR})",
            "Accept": "application/json"
        })

    def get_id_by_username(self, username):
        url = "https://users.roblox.com/v1/usernames/users"
        payload = {"usernames": [username], "excludeBannedUsers": False}
        try:
            resp = self.session.post(url, json=payload)
            data = resp.json().get('data', [])
            return data[0]['id'] if data else None
        except: return None

    def get_user_info(self, user_id):
        try: return self.session.get(f"https://users.roblox.com/v1/users/{user_id}").json()
        except: return None

    def get_premium_status(self, user_id):
        try:
            resp = self.session.get(f"https://premium.roblox.com/v1/users/{user_id}/premium-features")
            return resp.json().get('subscriptionProductModel', {}).get('renewalPeriod') is not None
        except: return False

    def get_presence(self, user_id):
        try:
            resp = self.session.post("https://presence.roblox.com/v1/presence/users", json={"userIds": [user_id]})
            data = resp.json().get('userPresences', [])
            return data[0] if data else None
        except: return None

    def get_friends_count(self, user_id):
        try: return self.session.get(f"https://friends.roblox.com/v1/users/{user_id}/friends/count").json().get('count', 0)
        except: return 0

    def get_friends_list(self, user_id, limit=50):
        try:
            url = f"https://friends.roblox.com/v1/users/{user_id}/friends"
            resp = self.session.get(url)
            data = resp.json().get('data', [])
            return data[:limit]
        except: return []

    def get_followers_count(self, user_id):
        try: return self.session.get(f"https://friends.roblox.com/v1/users/{user_id}/followers/count").json().get('count', 0)
        except: return 0

    def get_following_count(self, user_id):
        try: return self.session.get(f"https://friends.roblox.com/v1/users/{user_id}/following/count").json().get('count', 0)
        except: return 0

    def get_badges(self, user_id, limit=5):
        try:
            return self.session.get(f"https://badges.roblox.com/v1/users/{user_id}/badges?limit={limit}&sortOrder=Desc").json().get('data', [])
        except: return []

    def get_groups(self, user_id):
        try: return self.session.get(f"https://groups.roblox.com/v1/users/{user_id}/groups/roles").json().get('data', [])
        except: return []

    def get_avatar_thumbnail(self, user_id):
        try:
            data = self.session.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=420x420&format=Png&isCircular=false").json().get('data', [])
            return data[0].get('imageUrl') if data else "N/A"
        except: return "N/A"

    def get_currently_wearing(self, user_id):
        try:
            resp = self.session.get(f"https://avatar.roblox.com/v1/users/{user_id}/avatar")
            return resp.json().get('assets', [])
        except: return []

    def get_favorites(self, user_id, limit=50):
        try:
            url = f"https://games.roblox.com/v2/users/{user_id}/favorite/games?limit={limit}&sortOrder=Desc"
            resp = self.session.get(url)
            return resp.json().get('data', [])
        except: return []
