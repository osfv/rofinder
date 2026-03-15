import json
import os
from datetime import datetime

from version import APP_NAME, VERSION, AUTHOR


class RoFinderExporter:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _normalize_filename(self, filename, ext):
        if not filename.endswith(ext):
            return f"{filename}{ext}"
        return filename

    def export_json(self, data, filename):
        filename = self._normalize_filename(filename, '.json')

        final_data = {
            "meta": {
                "generated_at": self.timestamp,
                "tool": APP_NAME,
                "version": VERSION,
                "author": AUTHOR,
            },
            "data": data,
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=4)
        return os.path.abspath(filename)

    def export_txt(self, data, filename):
        filename = self._normalize_filename(filename, '.txt')

        profile = data.get('profile', {})
        stats = data.get('stats', {})
        status = data.get('status', {})

        lines = [
            "============================================",
            f" {APP_NAME.upper()} INTELLIGENCE REPORT",
            f" Generated: {self.timestamp}",
            "============================================",
            "",
            "[ BASIC INFORMATION ]",
            f" Username:     {profile.get('name')}",
            f" Display Name: {profile.get('displayName')}",
            f" User ID:      {profile.get('id')}",
            f" Created:      {profile.get('created')}",
            f" Is Banned:    {profile.get('isBanned')}",
            "",
            "[ STATISTICS ]",
            f" Friends:      {stats.get('friends')}",
            f" Followers:    {stats.get('followers')}",
            f" Following:    {stats.get('following')}",
            "",
            "[ PRESENCE ]",
            f" Status:       {status.get('presence', {}).get('userPresenceType')}",
            f" Premium:      {status.get('premium')}",
            "",
            "[ AVATAR ]",
            f" Headshot URL: {data.get('avatar_url')}",
            "",
        ]

        assets = data.get('assets') or []
        if assets:
            lines.append("[ CURRENTLY WEARING ]")
            for asset in assets:
                asset_type = asset.get('assetType', {}).get('name', 'Asset')
                lines.append(f" - {asset.get('name')} ({asset_type})")
                lines.append(f"   Link: https://www.roblox.com/catalog/{asset.get('id')}")
            lines.append("")

        favorites = data.get('favorites') or []
        if favorites:
            lines.append("[ FAVORITE GAMES ]")
            for game in favorites:
                creator_name = game.get('creatorName') or game.get('creator', {}).get('name', 'Unknown')
                lines.append(f" - {game.get('name')} (By {creator_name})")
            lines.append("")

        badges = data.get('badges') or []
        if badges:
            lines.append("[ BADGES ]")
            for badge in badges:
                lines.append(f" - {badge.get('name')} ({badge.get('id')})")
            lines.append("")

        groups = data.get('groups') or []
        if groups:
            lines.append("[ GROUPS ]")
            for group in groups:
                group_name = group.get('group', {}).get('name', 'Unknown')
                role_name = group.get('role', {}).get('name', 'Member')
                lines.append(f" - {group_name} ({role_name})")
            lines.append("")

        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        return os.path.abspath(filename)

    def export_md(self, data, filename):
        filename = self._normalize_filename(filename, '.md')

        profile = data.get('profile', {})
        stats = data.get('stats', {})
        status = data.get('status', {})

        lines = [
            f"# {APP_NAME} Intelligence Report",
            "",
            f"- Generated: {self.timestamp}",
            f"- Version: {VERSION}",
            "",
            "## Basic Information",
            f"- Username: {profile.get('name')}",
            f"- Display Name: {profile.get('displayName')}",
            f"- User ID: {profile.get('id')}",
            f"- Created: {profile.get('created')}",
            f"- Is Banned: {profile.get('isBanned')}",
            "",
            "## Statistics",
            f"- Friends: {stats.get('friends')}",
            f"- Followers: {stats.get('followers')}",
            f"- Following: {stats.get('following')}",
            "",
            "## Presence",
            f"- Status Code: {status.get('presence', {}).get('userPresenceType')}",
            f"- Premium: {status.get('premium')}",
            "",
            "## Avatar",
            f"- Headshot URL: {data.get('avatar_url')}",
            "",
        ]

        assets = data.get('assets') or []
        if assets:
            lines.append("## Currently Wearing")
            for asset in assets:
                asset_type = asset.get('assetType', {}).get('name', 'Asset')
                lines.append(f"- {asset.get('name')} ({asset_type})")
            lines.append("")

        favorites = data.get('favorites') or []
        if favorites:
            lines.append("## Favorite Games")
            for game in favorites:
                creator_name = game.get('creatorName') or game.get('creator', {}).get('name', 'Unknown')
                lines.append(f"- {game.get('name')} (By {creator_name})")
            lines.append("")

        badges = data.get('badges') or []
        if badges:
            lines.append("## Badges")
            for badge in badges:
                lines.append(f"- {badge.get('name')} ({badge.get('id')})")
            lines.append("")

        groups = data.get('groups') or []
        if groups:
            lines.append("## Groups")
            for group in groups:
                group_name = group.get('group', {}).get('name', 'Unknown')
                role_name = group.get('role', {}).get('name', 'Member')
                lines.append(f"- {group_name} ({role_name})")
            lines.append("")

        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        return os.path.abspath(filename)
