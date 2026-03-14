from datetime import datetime
import time

import dateutil.parser
from rich import box
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text

from version import AUTHOR

console = Console()

class RoFinderUI:
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
        return Panel(
            Align.center(banner_text),
            subtitle=f"[dim]By {AUTHOR}[/dim]",
            border_style=border_style
        )

    def boot_sequence(self):
        steps = [
            ("Warming neon core", 0.22),
            ("Syncing Roblox endpoints", 0.22),
            ("Mapping presence grid", 0.22),
            ("Locking target channel", 0.22),
        ]

        with Progress(
            SpinnerColumn(style="bold cyan"),
            TextColumn("[bold magenta]{task.description}"),
            BarColumn(bar_width=18, style="cyan"),
            TextColumn("[dim]{task.percentage:>3.0f}%"),
            transient=True,
            console=console
        ) as progress:
            for description, duration in steps:
                task = progress.add_task(description, total=100)
                for _ in range(10):
                    progress.advance(task, 10)
                    time.sleep(duration / 10)

    def play_intro(self):
        frames = [
            self._banner_panel("bold cyan", "cyan"),
            self._banner_panel("bold magenta", "magenta"),
            self._banner_panel("bold bright_cyan", "bright_cyan"),
        ]

        with Live(frames[0], refresh_per_second=12, console=console, transient=True) as live:
            for i in range(18):
                live.update(frames[i % len(frames)])
                time.sleep(0.06)

    def print_banner(self):
        console.print(self._banner_panel("bold cyan", "cyan"))

    def create_mini_header(self, user_data):
        verified = "☑️" if user_data.get('hasVerifiedBadge') else ""
        return Panel(
            f"[bold white]Target:[/bold white] [yellow]@{user_data.get('name')}[/yellow] {verified} [dim]({user_data.get('id')})[/dim]",
            border_style="cyan",
            expand=False
        )

    def create_user_panel(self, user_data, friends, followers, following, thumbnail, presence_data, is_premium):
        created_at = dateutil.parser.parse(user_data['created'])
        now = datetime.now(created_at.tzinfo)
        age = (now - created_at).days

        status_text, status_color = "Offline", "red"
        last_online = "Unknown"

        if presence_data:
            ptype = presence_data.get('userPresenceType', 0)
            if ptype == 1: status_text, status_color = "Online", "green"
            elif ptype == 2: status_text, status_color = "Playing", "orange1"
            elif ptype == 3: status_text, status_color = "Studio", "blue"

            if presence_data.get('lastOnline'):
                dt = dateutil.parser.parse(presence_data['lastOnline'])
                last_online = dt.strftime('%Y-%m-%d %H:%M')

        verified = " ☑️ " if user_data.get('hasVerifiedBadge') else ""
        premium = " 💎 [black on white] PREM [/black on white]" if is_premium else ""

        grid = Table.grid(expand=True)
        grid.add_column()
        grid.add_column(justify="right")

        t1 = Table(show_header=False, box=None, padding=(0, 2))
        t1.add_row("[bold yellow]Name:", f"{user_data.get('name')} {verified}{premium}")
        t1.add_row("[bold yellow]Display:", user_data.get('displayName'))
        t1.add_row("[bold yellow]ID:", str(user_data.get('id')))
        t1.add_row("[bold yellow]Status:", f"[{status_color}]● {status_text}[/{status_color}]")
        t1.add_row("[bold yellow]Seen:", last_online)
        t1.add_row("[bold yellow]Age:", f"{age} days")

        t2 = Table(show_header=True, box=box.SIMPLE_HEAD)
        t2.add_column("Stat", style="magenta")
        t2.add_column("Val", justify="right")
        t2.add_row("Friends", str(friends))
        t2.add_row("Followers", str(followers))
        t2.add_row("Following", str(following))

        grid.add_row(t1, t2)
        return Panel(grid, title=f"[bold cyan]User: {user_data.get('name')}[/bold cyan]", border_style="cyan")

    def create_friends_table(self, friends_list):
        table = Table(title=f"Friends List ({len(friends_list)})", expand=True, box=box.ROUNDED, border_style="cyan")
        table.add_column("User ID", style="dim")
        table.add_column("Username", style="bold white")
        table.add_column("Display Name", style="yellow")
        table.add_column("Status", style="green")

        for f in friends_list:
            is_online = f.get('isOnline', False)
            status = "● Online" if is_online else "[dim]Offline[/dim]"
            table.add_row(str(f['id']), f['name'], f['displayName'], status)

        return table

    def create_wearing_table(self, assets):
        table = Table(title="Avatar Assets (Wearing)", expand=True, box=box.ROUNDED, border_style="blue")
        table.add_column("Type", style="dim")
        table.add_column("Item Name", style="bold white")
        table.add_column("ID", style="cyan")

        for asset in assets:
            table.add_row(asset.get('assetType', {}).get('name', 'Asset'), asset['name'], str(asset['id']))
        return table

    def create_favorites_table(self, games):
        table = Table(title="Favorite Games", expand=True, box=box.ROUNDED, border_style="green")
        table.add_column("Game Name", style="bold white")
        table.add_column("Creator", style="yellow")

        for game in games:
            creator_name = game.get('creator', {}).get('name', 'Unknown')
            table.add_row(game.get('name', 'Unknown'), creator_name)
        return table

    def create_badges_table(self, badges):
        table = Table(title="Recent Badges", expand=True, box=box.ROUNDED, border_style="magenta")
        table.add_column("ID", style="dim", width=12)
        table.add_column("Badge Name", style="bold white")
        for badge in badges:
            table.add_row(str(badge['id']), badge['name'])
        return table

    def create_groups_table(self, groups):
        table = Table(title="Top Groups", expand=True, box=box.ROUNDED, border_style="yellow")
        table.add_column("Group", style="bold white")
        table.add_column("Rank", style="dim")
        for group in groups[:5]:
            table.add_row(group['group']['name'], group['role']['name'])
        return table
