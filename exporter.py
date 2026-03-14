import json
import os
from datetime import datetime

from version import APP_NAME, VERSION

class RoFinderExporter:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def export_json(self, data, filename):
        if not filename.endswith('.json'):
            filename += '.json'

        final_data = {
            "meta": {
                "generated_at": self.timestamp,
                "tool": f"{APP_NAME} v{VERSION}"
            },
            "data": data
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=4)
        return os.path.abspath(filename)

    def export_txt(self, data, filename):
        if not filename.endswith('.txt'):
            filename += '.txt'

        user = data.get('profile', {})
        stats = data.get('stats', {})

        lines = [
            "============================================",
            " ROFINDER INTELLIGENCE REPORT",
            f" Generated: {self.timestamp}",
            "============================================",
            "",
            "[ BASIC INFORMATION ]",
            f" Username:     {user.get('name')}",
            f" Display Name: {user.get('displayName')}",
            f" User ID:      {user.get('id')}",
            f" Created:      {user.get('created')}",
            f" Is Banned:    {user.get('isBanned')}",
            "",
            "[ STATISTICS ]",
            f" Friends:      {stats.get('friends')}",
            f" Followers:    {stats.get('followers')}",
            f" Following:    {stats.get('following')}",
            "",
            "[ AVATAR ]",
            f" Headshot URL: {data.get('avatar_url')}",
            ""
        ]

        if data.get('assets'):
            lines.append("[ CURRENTLY WEARING ]")
            for asset in data['assets']:
                asset_type = asset.get('assetType', {}).get('name', 'Asset')
                lines.append(f" - {asset.get('name')} ({asset_type})")
                lines.append(f"   Link: https://www.roblox.com/catalog/{asset.get('id')}")
            lines.append("")

        if data.get('favorites'):
            lines.append("[ FAVORITE GAMES ]")
            for game in data['favorites']:
                creator_name = game.get('creatorName') or game.get('creator', {}).get('name', 'Unknown')
                lines.append(f" - {game.get('name')} (By {creator_name})")
            lines.append("")

        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        return os.path.abspath(filename)
