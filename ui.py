import itertools
import random
from datetime import datetime
import time

import dateutil.parser
from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
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

BANNER_LINES = [
    r" ____       _____ _           _           ",
    r"|  _ \ ___ |  ___(_)_ __   __| | ___ _ __ ",
    r"| |_) / _ \| |_  | | '_ \ / _` |/ _ \ '__|",
    r"|  _ < (_) |  _| | | | | | (_| |  __/ |   ",
    r"|_| \_\___/|_|   |_|_| |_|\__,_|\___|_|   ",
]

GLYPHS = "░▒▓█▀▄▌▐╔╗╚╝═║"


class RoFinderUI:
    def __init__(self, theme="neon", animate=True):
        self.theme = THEMES.get(theme, THEMES["neon"])
        self.animate = animate

    # ── internal helpers ──────────────────────────────────────────────

    def _banner_text(self):
        return "\n".join(BANNER_LINES)

    def _banner_panel(self, text_style, border_style):
        banner_text = Text(self._banner_text(), style=text_style)
        subtitle = f"[dim]By {AUTHOR}[/dim]"
        return Panel(Align.center(banner_text), subtitle=subtitle, border_style=border_style)

    def _scramble_line(self, target, progress):
        """Return a partially-revealed version of *target*.

        *progress* is a float 0→1.  Characters up to the progress
        point are revealed; the rest are random glyphs.
        """
        reveal = int(len(target) * progress)
        revealed = target[:reveal]
        noise = "".join(random.choice(GLYPHS) for _ in range(len(target) - reveal))
        return revealed + noise

    def boot_sequence(self):
        steps = [
            "Initialising core",
            "Syncing endpoints",
            "Mapping presence grid",
            "Locking channel",
        ]

        if not self.animate:
            return

        dots = itertools.cycle(["·  ", "·· ", "···"])

        with Live(console=console, refresh_per_second=20, transient=True) as live:
            completed = []
            for i, step in enumerate(steps):
                for tick in range(8):
                    lines = Text()
                    for done in completed:
                        lines.append(f"  ✓ {done}\n", style=f"bold {self.theme['success']}")
                    lines.append(f"  {next(dots)} {step}", style=f"{self.theme['muted']}")
                    live.update(lines)
                    time.sleep(0.04)
                completed.append(step)

            lines = Text()
            for done in completed:
                lines.append(f"  ✓ {done}\n", style=f"bold {self.theme['success']}")
            live.update(lines)
            time.sleep(0.15)

    def play_intro(self):
        if not self.animate:
            return

        with Live(console=console, refresh_per_second=30, transient=True) as live:
            revealed = []
            for line in BANNER_LINES:
                for step in range(6):
                    progress = (step + 1) / 6
                    current = self._scramble_line(line, progress)
                    display = Text()
                    for prev in revealed:
                        display.append(prev + "\n", style=f"bold {self.theme['primary']}")
                    display.append(current, style=f"bold {self.theme['accent']}")
                    panel = Panel(
                        Align.center(display),
                        border_style=self.theme["primary"],
                        subtitle=f"[dim]By {AUTHOR}[/dim]",
                    )
                    live.update(panel)
                    time.sleep(0.018)
                revealed.append(line)

            for color in [self.theme["accent"], self.theme["primary"]]:
                full = Text("\n".join(BANNER_LINES), style=f"bold {color}")
                panel = Panel(
                    Align.center(full),
                    border_style=color,
                    subtitle=f"[dim]By {AUTHOR}[/dim]",
                )
                live.update(panel)
                time.sleep(0.12)

    def print_banner(self):
        console.print(self._banner_panel(f"bold {self.theme['primary']}", self.theme["panel"]))

    def section_header(self, title):
        return Panel(
            Align.center(Text(title.upper(), style=f"bold {self.theme['accent']}")),
            border_style=self.theme["accent"],
            padding=(0, 2),
        )

    def animate_section_header(self, title):
        if not self.animate:
            console.print(self.section_header(title))
            return

        target = title.upper()
        with Live(console=console, refresh_per_second=24, transient=True) as live:
            for step in range(8):
                progress = (step + 1) / 8
                decoded = self._scramble_line(target, progress)
                panel = Panel(
                    Align.center(Text(decoded, style=f"bold {self.theme['accent']}")),
                    border_style=self.theme["muted"],
                    padding=(0, 2),
                )
                live.update(panel)
                time.sleep(0.025)

        console.print(self.section_header(title))

    def _print_table_animated(self, table_builder, rows, delay=0.035):
        if not self.animate or not rows:
            console.print(table_builder(rows))
            return

        with Live(console=console, refresh_per_second=24, transient=True) as live:
            for i in range(1, len(rows) + 1):
                live.update(table_builder(rows[:i]))
                time.sleep(delay)

        console.print(table_builder(rows))

    def create_mini_header(self, user_data):
        verified = "VERIFIED" if user_data.get("hasVerifiedBadge") else ""
        verified_text = (
            f" [bold {self.theme['info']}]{verified}[/bold {self.theme['info']}]"
            if verified
            else ""
        )
        return Panel(
            f"[bold white]Target:[/bold white] [yellow]@{user_data.get('name')}[/yellow]{verified_text} [dim]({user_data.get('id')})[/dim]",
            border_style=self.theme["panel"],
            expand=False,
        )

    def _profile_panel(self, user_data):
        created_at = dateutil.parser.parse(user_data["created"])
        now = datetime.now(created_at.tzinfo)
        age_days = (now - created_at).days

        table = Table.grid(padding=(0, 1))
        table.add_row("Username", f"@{user_data.get('name')}")
        table.add_row("Display", user_data.get("displayName"))
        table.add_row("User ID", str(user_data.get("id")))
        table.add_row("Created", user_data.get("created"))
        table.add_row("Account Age", f"{age_days} days")
        table.add_row("Banned", str(user_data.get("isBanned")))

        return Panel(table, title="Profile", border_style=self.theme["panel"], box=box.ROUNDED)

    def _stats_panel(self, stats):
        table = Table(show_header=True, box=box.SIMPLE_HEAD)
        table.add_column("Stat", style=self.theme["accent"])
        table.add_column("Value", justify="right")
        table.add_row("Friends", str(stats.get("friends", 0)))
        table.add_row("Followers", str(stats.get("followers", 0)))
        table.add_row("Following", str(stats.get("following", 0)))
        return Panel(table, title="Network", border_style=self.theme["panel"], box=box.ROUNDED)

    def _presence_panel(self, presence_data, is_premium):
        status_text, status_color = "Offline", self.theme["danger"]
        last_online = "Unknown"

        if presence_data:
            ptype = presence_data.get("userPresenceType", 0)
            if ptype == 1:
                status_text, status_color = "Online", self.theme["success"]
            elif ptype == 2:
                status_text, status_color = "Playing", self.theme["warning"]
            elif ptype == 3:
                status_text, status_color = "Studio", self.theme["info"]

            if presence_data.get("lastOnline"):
                dt = dateutil.parser.parse(presence_data["lastOnline"])
                last_online = dt.strftime("%Y-%m-%d %H:%M")

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

    def _build_friends_table(self, rows):
        table = Table(
            title=f"Friends ({len(rows)})",
            expand=True,
            box=box.ROUNDED,
            border_style=self.theme["primary"],
        )
        table.add_column("User ID", style=self.theme["muted"])
        table.add_column("Username", style="bold")
        table.add_column("Display Name", style=self.theme["info"])
        table.add_column("Status", style=self.theme["success"])
        for friend in rows:
            status = "Online" if friend.get("isOnline") else "Offline"
            table.add_row(
                str(friend.get("id")),
                friend.get("name"),
                friend.get("displayName"),
                status,
            )
        return table

    def _build_wearing_table(self, rows):
        table = Table(
            title="Avatar Assets",
            expand=True,
            box=box.ROUNDED,
            border_style=self.theme["accent"],
        )
        table.add_column("Type", style=self.theme["muted"])
        table.add_column("Item Name", style="bold")
        table.add_column("ID", style=self.theme["info"])
        for asset in rows:
            asset_type = asset.get("assetType", {}).get("name", "Asset")
            table.add_row(asset_type, asset.get("name", "Unknown"), str(asset.get("id")))
        return table

    def _build_favorites_table(self, rows):
        table = Table(
            title="Favorite Games",
            expand=True,
            box=box.ROUNDED,
            border_style=self.theme["success"],
        )
        table.add_column("Game Name", style="bold")
        table.add_column("Creator", style=self.theme["info"])
        for game in rows:
            creator_name = game.get("creator", {}).get("name", "Unknown")
            table.add_row(game.get("name", "Unknown"), creator_name)
        return table

    def _build_badges_table(self, rows):
        table = Table(
            title="Recent Badges",
            expand=True,
            box=box.ROUNDED,
            border_style=self.theme["accent"],
        )
        table.add_column("ID", style=self.theme["muted"], width=12)
        table.add_column("Badge Name", style="bold")
        for badge in rows:
            table.add_row(str(badge.get("id")), badge.get("name", "Unknown"))
        return table

    def _build_groups_table(self, rows):
        table = Table(
            title="Top Groups",
            expand=True,
            box=box.ROUNDED,
            border_style=self.theme["warning"],
        )
        table.add_column("Group", style="bold")
        table.add_column("Rank", style=self.theme["muted"])
        for group in rows:
            table.add_row(
                group.get("group", {}).get("name", "Unknown"),
                group.get("role", {}).get("name", "Member"),
            )
        return table

    def print_friends_table(self, friends_list):
        self._print_table_animated(self._build_friends_table, friends_list)

    def print_wearing_table(self, assets):
        self._print_table_animated(self._build_wearing_table, assets)

    def print_favorites_table(self, games):
        self._print_table_animated(self._build_favorites_table, games)

    def print_badges_table(self, badges):
        self._print_table_animated(self._build_badges_table, badges)

    def print_groups_table(self, groups):
        self._print_table_animated(self._build_groups_table, groups)

    def create_friends_table(self, friends_list):
        return self._build_friends_table(friends_list)

    def create_wearing_table(self, assets):
        return self._build_wearing_table(assets)

    def create_favorites_table(self, games):
        return self._build_favorites_table(games)

    def create_badges_table(self, badges):
        return self._build_badges_table(badges)

    def create_groups_table(self, groups):
        return self._build_groups_table(groups)

    def outro(self, version_line):
        if not self.animate:
            console.print(f"[dim]{version_line}[/dim]", justify="center")
            return

        bar_width = min(console.width - 4, 48)

        with Live(console=console, refresh_per_second=20, transient=True) as live:
            for i in range(bar_width + 1):
                bar = f"[{self.theme['primary']}]{'━' * i}[/{self.theme['primary']}][{self.theme['muted']}]{'─' * (bar_width - i)}[/{self.theme['muted']}]"
                live.update(Align.center(Text.from_markup(bar)))
                time.sleep(0.008)
            time.sleep(0.1)

        console.print(f"[dim]{version_line}[/dim]", justify="center")
