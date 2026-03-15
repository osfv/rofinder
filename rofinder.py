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
exporter = RoFinderExporter()

DEFAULT_SECTIONS = {"profile", "stats", "presence", "avatar"}
FULL_SECTIONS = {
    "profile",
    "stats",
    "presence",
    "avatar",
    "assets",
    "friends",
    "favorites",
    "badges",
    "groups",
}

SECTION_ALIASES = {
    "games": "favorites",
    "favorites": "favorites",
    "friends": "friends",
    "avatar": "avatar",
    "assets": "assets",
    "badges": "badges",
    "groups": "groups",
    "profile": "profile",
    "stats": "stats",
    "presence": "presence",
}


def parse_sections(args):
    if args.full:
        return set(FULL_SECTIONS)

    if args.sections:
        requested = set()
        for token in args.sections.split(','):
            key = token.strip().lower()
            if not key:
                continue
            if key in SECTION_ALIASES:
                requested.add(SECTION_ALIASES[key])
        return requested or set(DEFAULT_SECTIONS)

    if args.avatar or args.friends or args.games:
        requested = set()
        if args.avatar:
            requested.update({"avatar", "assets"})
        if args.friends:
            requested.add("friends")
        if args.games:
            requested.add("favorites")
        return requested

    if args.detailed:
        return set(DEFAULT_SECTIONS) | {"badges", "groups"}

    return set(DEFAULT_SECTIONS)


def main():
    parser = argparse.ArgumentParser(description=f"{APP_NAME} v{VERSION} - Remastered Roblox Intelligence")
    parser.add_argument("user", help="Username or User ID")

    # Modes
    parser.add_argument("--detailed", action="store_true", help="Show main profile + badges + groups")
    parser.add_argument("--avatar", action="store_true", help="Show ONLY avatar information")
    parser.add_argument("--friends", action="store_true", help="Show ONLY friends list")
    parser.add_argument("--games", action="store_true", help="Show ONLY game favorites")
    parser.add_argument("--full", action="store_true", help="Fetch every available section")
    parser.add_argument("--sections", help="Comma-separated sections (profile, stats, presence, avatar, assets, friends, favorites, badges, groups)")

    # Options
    parser.add_argument("--limit", type=int, default=10, help="Limit results for lists (default: 10)")
    parser.add_argument("--save", help="Save output to file")
    parser.add_argument("--format", choices=['json', 'txt', 'md'], default='txt', help="Format for saving file")
    parser.add_argument("--json", action="store_true", help="Output raw JSON to console (for devs)")
    parser.add_argument("--theme", choices=["neon", "mono"], default="neon", help="UI theme")
    parser.add_argument("--no-anim", action="store_true", help="Disable intro animations")

    args = parser.parse_args()
    sections = parse_sections(args)

    ui = RoFinderUI(theme=args.theme)

    if not args.json and not args.no_anim:
        ui.boot_sequence()
        ui.play_intro()
        ui.print_banner()
    elif not args.json:
        ui.print_banner()

    user_id, user_info = api.resolve_user(args.user)

    if not user_id:
        console.print(f"[bold red]Error:[/bold red] User '{args.user}' not found.")
        sys.exit(1)

    full_data = {
        "profile": user_info,
        "stats": {},
        "status": {},
        "avatar_url": "N/A",
    }

    with Progress(SpinnerColumn(), TextColumn("[bold magenta]Gathering intel..."), transient=True) as progress:
        task = progress.add_task("", total=None)

        if "stats" in sections:
            progress.update(task, description="Pulling network stats...")
            full_data["stats"] = {
                "friends": api.get_friends_count(user_id),
                "followers": api.get_followers_count(user_id),
                "following": api.get_following_count(user_id),
            }

        if "presence" in sections:
            progress.update(task, description="Checking presence...")
            presence = api.get_presence(user_id)
            premium = api.get_premium_status(user_id)
            full_data["status"] = {"presence": presence, "premium": premium}

        if "avatar" in sections:
            progress.update(task, description="Rendering avatar...")
            full_data["avatar_url"] = api.get_avatar_thumbnail(user_id)

        if "assets" in sections:
            progress.update(task, description="Scanning avatar assets...")
            full_data["assets"] = api.get_currently_wearing(user_id)

        if "friends" in sections:
            progress.update(task, description=f"Fetching friends (Limit: {args.limit})...")
            full_data["friends_list"] = api.get_friends_list(user_id, limit=args.limit)

        if "favorites" in sections:
            progress.update(task, description=f"Fetching favorites (Limit: {args.limit})...")
            full_data["favorites"] = api.get_favorites(user_id, limit=args.limit)

        if "badges" in sections:
            progress.update(task, description="Fetching badges...")
            full_data["badges"] = api.get_badges(user_id, limit=args.limit)

        if "groups" in sections:
            progress.update(task, description="Fetching groups...")
            full_data["groups"] = api.get_groups(user_id, limit=args.limit)

    if args.json:
        import json
        print(json.dumps(full_data, indent=4))
    else:
        should_render_overview = any(section in sections for section in {"stats", "presence", "avatar", "assets"})

        if should_render_overview:
            ui.render_overview(
                user_info,
                full_data.get("stats", {}),
                full_data.get("status", {}).get("presence"),
                full_data.get("status", {}).get("premium", False),
                full_data.get("avatar_url"),
                full_data.get("assets", []),
            )
        else:
            console.print(ui.create_mini_header(user_info))

        if full_data.get("assets"):
            console.print(ui.section_header("Avatar Assets"))
            console.print(ui.create_wearing_table(full_data["assets"]))

        if full_data.get("friends_list"):
            console.print(ui.section_header("Friends"))
            console.print(ui.create_friends_table(full_data["friends_list"]))

        if "favorites" in sections:
            console.print(ui.section_header("Favorites"))
            favorites = full_data.get("favorites", [])
            if favorites:
                console.print(ui.create_favorites_table(favorites))
            else:
                console.print(Panel("[dim yellow]No favorite games found or inventory is private.[/dim yellow]", border_style="yellow"))

        if full_data.get("badges"):
            console.print(ui.section_header("Badges"))
            console.print(ui.create_badges_table(full_data["badges"]))

        if full_data.get("groups"):
            console.print(ui.section_header("Groups"))
            console.print(ui.create_groups_table(full_data["groups"]))

    if args.save:
        filename = args.save
        with console.status("[bold yellow]Saving report..."):
            if args.format == 'json' or filename.endswith('.json'):
                saved_path = exporter.export_json(full_data, filename)
            elif args.format == 'md' or filename.endswith('.md'):
                saved_path = exporter.export_md(full_data, filename)
            else:
                saved_path = exporter.export_txt(full_data, filename)

        console.print(f"\n[bold green]Report saved:[/bold green] {saved_path}")

    if not args.json:
        console.print(f"[dim]{APP_NAME} v{VERSION}[/dim]", justify="center")


if __name__ == "__main__":
    main()
