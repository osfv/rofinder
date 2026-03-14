import argparse
import sys

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from api import RobloxAPI
from exporter import RoFinderExporter
from ui import RoFinderUI
from version import APP_NAME, VERSION

console = Console()
api = RobloxAPI()
ui = RoFinderUI()
exporter = RoFinderExporter()

APP_TITLE = f"{APP_NAME} v{VERSION} - Modular Roblox Intelligence"


def main():
    parser = argparse.ArgumentParser(description=APP_TITLE)
    parser.add_argument("user", help="Username or User ID")

    # Modes
    parser.add_argument("--detailed", action="store_true", help="Show main profile + badges + groups")
    parser.add_argument("--avatar", action="store_true", help="Show ONLY avatar information")
    parser.add_argument("--friends", action="store_true", help="Show ONLY friends list")
    parser.add_argument("--games", action="store_true", help="Show ONLY game favorites/history")

    # Options
    parser.add_argument("--limit", type=int, default=10, help="Limit results for lists (default: 10)")
    parser.add_argument("--save", help="Save output to file")
    parser.add_argument("--format", choices=['json', 'txt'], default='txt', help="Format for saving file")
    parser.add_argument("--json", action="store_true", help="Output raw JSON to console (for devs)")

    args = parser.parse_args()

    # If no specific mode is selected, default to Basic Summary (or detailed if flag present)
    is_specific_mode = args.avatar or args.friends or args.games

    if not args.json:
        ui.boot_sequence()
        ui.play_intro()
        ui.print_banner()

    user_input = args.user
    user_id = None

    # --- 1. Resolve User ---
    with Progress(SpinnerColumn(), TextColumn("[bold cyan]Targeting user..."), transient=True) as progress:
        progress.add_task("", total=None)
        if user_input.isdigit():
            user_id = int(user_input)
        else:
            user_id = api.get_id_by_username(user_input)

    if not user_id:
        console.print(f"[bold red]❌ Error:[/bold red] User '{user_input}' not found.")
        sys.exit(1)

    # Fetch Basic Info (Always needed for header/verification)
    user_info = api.get_user_info(user_id)
    if not user_info:
        console.print("[bold red]❌ Error:[/bold red] API Connection failed.")
        sys.exit(1)

    # --- 2. Data Fetching Strategy ---

    full_data = {
        "profile": user_info,
        "stats": {},
        "status": {},
        "avatar_url": "N/A"
    }

    with Progress(SpinnerColumn(), TextColumn("[bold magenta]Fetching intelligence..."), transient=True) as progress:
        task = progress.add_task("", total=None)

        # A. Default / Detailed Mode
        if not is_specific_mode:
            friends_count = api.get_friends_count(user_id)
            followers = api.get_followers_count(user_id)
            following = api.get_following_count(user_id)
            presence = api.get_presence(user_id)
            premium = api.get_premium_status(user_id)
            avatar = api.get_avatar_thumbnail(user_id)

            full_data["stats"] = {"friends": friends_count, "followers": followers, "following": following}
            full_data["status"] = {"presence": presence, "premium": premium}
            full_data["avatar_url"] = avatar

            # Output for JSON users
            if args.json:
                import json
                print(json.dumps(full_data, indent=4))
            else:
                # Display Main Panel
                console.print(ui.create_user_panel(user_info, friends_count, followers, following, avatar, presence, premium))

                if args.detailed:
                    progress.update(task, description="Fetching extended data...")
                    badges = api.get_badges(user_id)
                    groups = api.get_groups(user_id)
                    full_data["badges"] = badges
                    full_data["groups"] = groups

                    if badges: console.print(ui.create_badges_table(badges))
                    if groups: console.print(ui.create_groups_table(groups))

        # B. Specific Modes (can be combined)
        else:
            if not args.json:
                console.print(ui.create_mini_header(user_info))

            if args.avatar:
                progress.update(task, description="Scanning avatar assets...")
                assets = api.get_currently_wearing(user_id)
                thumb = api.get_avatar_thumbnail(user_id)
                full_data["assets"] = assets
                full_data["avatar_url"] = thumb
                if not args.json:
                    console.print(ui.create_wearing_table(assets))
                    console.print(f"[dim]Avatar Headshot: {thumb}[/dim]\n")

            if args.friends:
                progress.update(task, description=f"Fetching friends (Limit: {args.limit})...")
                friends_list = api.get_friends_list(user_id, limit=args.limit)
                full_data["friends_list"] = friends_list
                if not args.json:
                    console.print(ui.create_friends_table(friends_list))
                    print("")

            if args.games:
                progress.update(task, description=f"Fetching favorites (Limit: {args.limit})...")
                favorites = api.get_favorites(user_id, limit=args.limit)
                full_data["favorites"] = favorites
                if not args.json:
                    if favorites:
                        console.print(ui.create_favorites_table(favorites))
                    else:
                        console.print(Panel("[dim yellow]No favorite games found. User inventory might be private.[/dim yellow]", border_style="yellow"))
                    print("")

            if args.json:
                import json
                print(json.dumps(full_data, indent=4))

    # --- 3. Export Logic ---
    if args.save:
        filename = args.save
        saved_path = ""
        with console.status("[bold yellow]Saving report..."):
            if args.format == 'json' or filename.endswith('.json'):
                saved_path = exporter.export_json(full_data, filename)
            else:
                saved_path = exporter.export_txt(full_data, filename)

        console.print(f"\n[bold green]✅ Report saved:[/bold green] {saved_path}")

    if not args.json:
        console.print(f"[dim]{APP_NAME} v{VERSION}[/dim]", justify="center")

if __name__ == "__main__":
    main()
