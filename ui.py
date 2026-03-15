from datetime import datetime
import time

import dateutil.parser
from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text

from version import AUTHOR

console = Console()

THEMES = {
    "neon": {
        "primary": "cyan",
        "accent": "magenta",
        "muted": "bright_black",
        "success": "green",
        "warning": "yellow",
        "danger": "red",
        "info": "bright_cyan",
        "panel": "cyan",
    },
    "mono": {
        "primary": "white",
        "accent": "bright_white",
        "muted": "bright_black",
        "success": "white",
        "warning": "white",
        "danger": "white",
        "info": "white",
        "panel": "white",
    },
}


class RoFinderUI:
    def __init__(self, theme="neon"):
        self.theme = THEMES.get(theme, THEMES["neon"])

    def _banner_text(self):
        return r"""
 ____       _____ _           _           
|  _ \ ___ |  ___(_)_ __   __| | ___ _ __ 
| |_) / _ \| |_  | | '_ \ / _` |/ _ \ '__|
|  _ < (_) |  _| | | | | | (_| |  __/ |   
|_| \_\___/|_|   |_|_| |_|\__,_|\___|_|   
        """

    def _banner_panel(self, text_style, border_style):
        banner_text = Text(self._banner_text(), style=text_style)
        subtitle = f"[dim]By {AUTHOR}[/dim]"
        return Panel(Align.center(banner_text), subtitle=subtitle, border_style=border_style)

    def boot_sequence(self):
        steps = [
            ("Warming neon core", 0.22),
            ("Syncing Roblox endpoints", 0.22),
            ("Mapping presence grid", 0.22),
            ("Locking target channel", 0.22),
        ]

        with Progress(
            SpinnerColumn(style=f"bold {self.theme['primary']}"),
            TextColumn("[bold]{task.description}"),
            BarColumn(bar_width=18, style=self.theme["primary"]),
            TextColumn("[dim]{task.percentage:>3.0f}%"),
            transient=True,
            console=console,
        ) as progress:
            for description, duration in steps:
                task = progress.add_task(description, total=100)
                for _ in range(10):
                    progress.advance(task, 10)
                    time.sleep(duration / 10)

    def play_intro(self):
        frames = [
            self._banner_panel(f"bold {self.theme['primary']}", self.theme["primary"]),
            self._banner_panel(f"bold {self.theme['accent']}", self.theme["accent"]),
            self._banner_panel(f"bold {self.theme['info']}", self.theme["info"]),
        ]

        with Live(frames[0], refresh_per_second=12, console=console, transient=True) as live:
            for i in range(18):
                live.update(frames[i % len(frames)])
                time.sleep(0.06)

    def print_banner(self):
        console.print(self._banner_panel(f"bold {self.theme['primary']}", self.theme["panel"]))

    def section_header(self, title):
        return Panel(
            Align.center(Text(title.upper(), style=f"bold {self.theme['accent']}")),
            border_style=self.theme["accent"],
            padding=(0, 2),
        )

    def create_mini_header(self, user_data):
        verified = "VERIFIED" if user_data.get('hasVerifiedBadge') else ""
        verified_text = f" [bold {self.theme['info']}]{verified}[/bold {self.theme['info']}]" if verified else ""
        return Panel(
            f"[bold white]Target:[/bold white] [yellow]@{user_data.get('name')}[/yellow]{verified_text} [dim]({user_data.get('id')})[/dim]",
            border_style=self.theme["panel"],
            expand=False,
        )

    def _profile_panel(self, user_data):
        created_at = dateutil.parser.parse(user_data['created'])
        now = datetime.now(created_at.tzinfo)
        age_days = (now - created_at).days

        table = Table.grid(padding=(0, 1))
        table.add_row("Username", f"@{user_data.get('name')}")
        table.add_row("Display", user_data.get('displayName'))
        table.add_row("User ID", str(user_data.get('id')))
        table.add_row("Created", user_data.get('created'))
        table.add_row("Account Age", f"{age_days} days")
        table.add_row("Banned", str(user_data.get('isBanned')))

        return Panel(table, title="Profile", border_style=self.theme["panel"], box=box.ROUNDED)

    def _stats_panel(self, stats):
        table = Table(show_header=True, box=box.SIMPLE_HEAD)
        table.add_column("Stat", style=self.theme["accent"])
        table.add_column("Value", justify="right")
        table.add_row("Friends", str(stats.get('friends', 0)))
        table.add_row("Followers", str(stats.get('followers', 0)))
        table.add_row("Following", str(stats.get('following', 0)))
        return Panel(table, title="Network", border_style=self.theme["panel"], box=box.ROUNDED)

    def _presence_panel(self, presence_data, is_premium):
        status_text, status_color = "Offline", self.theme["danger"]
        last_online = "Unknown"

        if presence_data:
            ptype = presence_data.get('userPresenceType', 0)
            if ptype == 1:
                status_text, status_color = "Online", self.theme["success"]
            elif ptype == 2:
                status_text, status_color = "Playing", self.theme["warning"]
            elif ptype == 3:
                status_text, status_color = "Studio", self.theme["info"]

            if presence_data.get('lastOnline'):
                dt = dateutil.parser.parse(presence_data['lastOnline'])
                last_online = dt.strftime('%Y-%m-%d %H:%M')

        premium_text = "Yes" if is_premium else "No"

        table = Table.grid(padding=(0, 1))
        table.add_row("Status", f"[{status_color}]● {status_text}[/{status_color}]")
        table.add_row("Last Online", last_online)
        table.add_row("Premium", premium_text)

        return Panel(table, title="Presence", border_style=self.theme["panel"], box=box.ROUNDED)

    def _avatar_panel(self, avatar_url, assets):
        asset_count = len(assets) if assets else 0
        table = Table.grid(padding=(0, 1))
        table.add_row("Headshot", avatar_url or "N/A")
        table.add_row("Assets", str(asset_count))
        return Panel(table, title="Avatar", border_style=self.theme["panel"], box=box.ROUNDED)

    def render_overview(self, user_data, stats, presence_data, is_premium, avatar_url, assets):
        panels = [
            self._profile_panel(user_data),
            self._stats_panel(stats),
            self._presence_panel(presence_data, is_premium),
            self._avatar_panel(avatar_url, assets),
        ]
        console.print(Columns(panels, expand=True, equal=True))

    def create_friends_table(self, friends_list):
        table = Table(title=f"Friends ({len(friends_list)})", expand=True, box=box.ROUNDED, border_style=self.theme["primary"])
        table.add_column("User ID", style=self.theme["muted"])
        table.add_column("Username", style="bold")
        table.add_column("Display Name", style=self.theme["info"])
        table.add_column("Status", style=self.theme["success"])

        for friend in friends_list:
            status = "Online" if friend.get('isOnline') else "Offline"
            table.add_row(str(friend.get('id')), friend.get('name'), friend.get('displayName'), status)

        return table

    def create_wearing_table(self, assets):
        table = Table(title="Avatar Assets", expand=True, box=box.ROUNDED, border_style=self.theme["accent"])
        table.add_column("Type", style=self.theme["muted"])
        table.add_column("Item Name", style="bold")
        table.add_column("ID", style=self.theme["info"])

        for asset in assets:
            asset_type = asset.get('assetType', {}).get('name', 'Asset')
            table.add_row(asset_type, asset.get('name', 'Unknown'), str(asset.get('id')))
        return table

    def create_favorites_table(self, games):
        table = Table(title="Favorite Games", expand=True, box=box.ROUNDED, border_style=self.theme["success"])
        table.add_column("Game Name", style="bold")
        table.add_column("Creator", style=self.theme["info"])

        for game in games:
            creator_name = game.get('creator', {}).get('name', 'Unknown')
            table.add_row(game.get('name', 'Unknown'), creator_name)
        return table

    def create_badges_table(self, badges):
        table = Table(title="Recent Badges", expand=True, box=box.ROUNDED, border_style=self.theme["accent"])
        table.add_column("ID", style=self.theme["muted"], width=12)
        table.add_column("Badge Name", style="bold")
        for badge in badges:
            table.add_row(str(badge.get('id')), badge.get('name', 'Unknown'))
        return table

    def create_groups_table(self, groups):
        table = Table(title="Top Groups", expand=True, box=box.ROUNDED, border_style=self.theme["warning"])
        table.add_column("Group", style="bold")
        table.add_column("Rank", style=self.theme["muted"])
        for group in groups:
            table.add_row(group.get('group', {}).get('name', 'Unknown'), group.get('role', {}).get('name', 'Member'))
        return table
