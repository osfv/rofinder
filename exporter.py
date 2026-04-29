import json
import os
from datetime import datetime
from pathlib import Path

from version import APP_NAME, VERSION, AUTHOR


class RoFinderExporter:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _normalize_filename(self, filename, ext):
        path = Path(filename)
        if path.suffix.lower() != ext:
            path = Path(f"{path}{ext}")
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def _write_lines(self, filename, lines):
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return os.path.abspath(filename)

    def _profile_stats_status(self, data):
        return data.get("profile", {}), data.get("stats", {}), data.get("status", {})

    def _friend_name(self, friend):
        username = friend.get("name", "Unknown")
        display_name = friend.get("displayName")
        if display_name and display_name != username:
            return f"{display_name} (@{username})"
        return username

    def _creator_name(self, game):
        return game.get("creatorName") or game.get("creator", {}).get("name", "Unknown")

    def _asset_type(self, asset):
        return asset.get("assetType", {}).get("name", "Asset")

    def _base_txt_lines(self, data):
        profile, stats, status = self._profile_stats_status(data)
        return [
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

    def _base_md_lines(self, data):
        profile, stats, status = self._profile_stats_status(data)
        return [
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

    def _append_section(self, lines, title, rows, formatter):
        if not rows:
            return

        lines.append(title)
        for row in rows:
            formatted = formatter(row)
            if isinstance(formatted, list):
                lines.extend(formatted)
            else:
                lines.append(formatted)
        lines.append("")

    def _txt_asset_lines(self, asset):
        return [
            f" - {asset.get('name')} ({self._asset_type(asset)})",
            f"   Link: https://www.roblox.com/catalog/{asset.get('id')}",
        ]

    def _md_asset_line(self, asset):
        return f"- {asset.get('name')} ({self._asset_type(asset)})"

    def _txt_friend_line(self, friend):
        return f" - {self._friend_name(friend)} ({friend.get('id')})"

    def _md_friend_line(self, friend):
        return f"- {self._friend_name(friend)} ({friend.get('id')})"

    def _txt_favorite_line(self, game):
        return f" - {game.get('name')} (By {self._creator_name(game)})"

    def _md_favorite_line(self, game):
        return f"- {game.get('name')} (By {self._creator_name(game)})"

    def _txt_badge_line(self, badge):
        return f" - {badge.get('name')} ({badge.get('id')})"

    def _md_badge_line(self, badge):
        return f"- {badge.get('name')} ({badge.get('id')})"

    def _txt_group_line(self, group):
        group_name = group.get("group", {}).get("name", "Unknown")
        role_name = group.get("role", {}).get("name", "Member")
        return f" - {group_name} ({role_name})"

    def _md_group_line(self, group):
        group_name = group.get("group", {}).get("name", "Unknown")
        role_name = group.get("role", {}).get("name", "Member")
        return f"- {group_name} ({role_name})"

    def export_json(self, data, filename):
        filename = self._normalize_filename(filename, ".json")

        final_data = {
            "meta": {
                "generated_at": self.timestamp,
                "tool": APP_NAME,
                "version": VERSION,
                "author": AUTHOR,
            },
            "data": data,
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=4)
        return os.path.abspath(filename)

    def export_txt(self, data, filename):
        filename = self._normalize_filename(filename, ".txt")
        lines = self._base_txt_lines(data)

        self._append_section(
            lines, "[ CURRENTLY WEARING ]", data.get("assets"), self._txt_asset_lines
        )
        self._append_section(lines, "[ FRIENDS ]", data.get("friends_list"), self._txt_friend_line)
        self._append_section(
            lines, "[ FAVORITE GAMES ]", data.get("favorites"), self._txt_favorite_line
        )
        self._append_section(lines, "[ BADGES ]", data.get("badges"), self._txt_badge_line)
        self._append_section(lines, "[ GROUPS ]", data.get("groups"), self._txt_group_line)

        return self._write_lines(filename, lines)

    def export_md(self, data, filename):
        filename = self._normalize_filename(filename, ".md")
        lines = self._base_md_lines(data)

        self._append_section(lines, "## Currently Wearing", data.get("assets"), self._md_asset_line)
        self._append_section(lines, "## Friends", data.get("friends_list"), self._md_friend_line)
        self._append_section(
            lines, "## Favorite Games", data.get("favorites"), self._md_favorite_line
        )
        self._append_section(lines, "## Badges", data.get("badges"), self._md_badge_line)
        self._append_section(lines, "## Groups", data.get("groups"), self._md_group_line)

        return self._write_lines(filename, lines)
