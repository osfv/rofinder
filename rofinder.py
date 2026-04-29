import argparse
import json
import os
import sys

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from api import RobloxAPI
from exporter import RoFinderExporter
from ui import RoFinderUI
from version import APP_NAME, VERSION

console = Console()
error_console = Console(stderr=True)
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

API_DOMAIN_MAP = {
    "roproxy": "roproxy.com",
    "roblox": "roblox.com",
}


def positive_int(value):
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"{value!r} is not a valid integer") from exc

    if number < 1:
        raise argparse.ArgumentTypeError("limit must be a positive integer")
    return number


def parse_sections(args):
    if args.full:
        return set(FULL_SECTIONS)

    if args.sections:
        requested = set()
        unknown = []

        for token in args.sections.split(","):
            key = token.strip().lower()
            if not key:
                continue
            section = SECTION_ALIASES.get(key)
            if section:
                requested.add(section)
            else:
                unknown.append(key)

        if unknown:
            valid_sections = ", ".join(sorted(SECTION_ALIASES))
            unknown_sections = ", ".join(unknown)
            raise argparse.ArgumentTypeError(
                f"unknown section(s): {unknown_sections}. Available sections: {valid_sections}"
            )

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


def resolve_api_domain(api_choice):
    if api_choice:
        return API_DOMAIN_MAP.get(api_choice, "roproxy.com")
    env_domain = os.getenv("ROFINDER_API_DOMAIN")
    return env_domain or "roproxy.com"


def build_parser():
    parser = argparse.ArgumentParser(
        description=f"{APP_NAME} v{VERSION} - Remastered Roblox Intelligence"
    )
    parser.add_argument("user", help="Username or User ID")

    parser.add_argument(
        "--detailed", action="store_true", help="Show main profile + badges + groups"
    )
    parser.add_argument("--avatar", action="store_true", help="Show ONLY avatar information")
    parser.add_argument("--friends", action="store_true", help="Show ONLY friends list")
    parser.add_argument("--games", action="store_true", help="Show ONLY game favorites")
    parser.add_argument("--full", action="store_true", help="Fetch every available section")
    parser.add_argument(
        "--sections",
        help="Comma-separated sections (profile, stats, presence, avatar, assets, friends, favorites, badges, groups)",
    )

    parser.add_argument("--limit", type=positive_int, default=10, help="Limit list results")
    parser.add_argument("--save", help="Save output to file")
    parser.add_argument(
        "--format",
        choices=["json", "txt", "md"],
        default="txt",
        help="Format for saving file",
    )
    parser.add_argument("--json", action="store_true", help="Output raw JSON to console")
    parser.add_argument("--theme", choices=["neon", "mono"], default="neon", help="UI theme")
    parser.add_argument("--no-anim", action="store_true", help="Disable intro animations")
    parser.add_argument("--api", choices=["roproxy", "roblox"], help="API backend")
    return parser


def _progress_update(progress, task_id, description):
    if progress is not None and task_id is not None:
        progress.update(task_id, description=description)


def gather_intel(api, user_id, user_info, sections, limit, progress=None, task_id=None):
    data = {
        "profile": user_info,
        "stats": {},
        "status": {},
        "avatar_url": "N/A",
    }

    if "stats" in sections:
        _progress_update(progress, task_id, "Pulling network stats...")
        data["stats"] = {
            "friends": api.get_friends_count(user_id),
            "followers": api.get_followers_count(user_id),
            "following": api.get_following_count(user_id),
        }

    if "presence" in sections:
        _progress_update(progress, task_id, "Checking presence...")
        data["status"] = {
            "presence": api.get_presence(user_id),
            "premium": api.get_premium_status(user_id),
        }

    if "avatar" in sections:
        _progress_update(progress, task_id, "Rendering avatar...")
        data["avatar_url"] = api.get_avatar_thumbnail(user_id)

    if "assets" in sections:
        _progress_update(progress, task_id, "Scanning avatar assets...")
        data["assets"] = api.get_currently_wearing(user_id)

    if "friends" in sections:
        _progress_update(progress, task_id, f"Fetching friends (Limit: {limit})...")
        data["friends_list"] = api.get_friends_list(user_id, limit=limit)

    if "favorites" in sections:
        _progress_update(progress, task_id, f"Fetching favorites (Limit: {limit})...")
        data["favorites"] = api.get_favorites(user_id, limit=limit)

    if "badges" in sections:
        _progress_update(progress, task_id, f"Fetching badges (Limit: {limit})...")
        data["badges"] = api.get_badges(user_id, limit=limit)

    if "groups" in sections:
        _progress_update(progress, task_id, f"Fetching groups (Limit: {limit})...")
        data["groups"] = api.get_groups(user_id, limit=limit)

    return data


def gather_intel_with_progress(api, user_id, user_info, sections, limit, show_progress=True):
    if not show_progress:
        return gather_intel(api, user_id, user_info, sections, limit)

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold magenta]Gathering intel..."),
        transient=True,
    ) as progress:
        task_id = progress.add_task("", total=None)
        return gather_intel(api, user_id, user_info, sections, limit, progress, task_id)


def render_results(ui, data, sections):
    should_render_overview = any(
        section in sections for section in {"stats", "presence", "avatar", "assets"}
    )

    if should_render_overview:
        ui.render_overview(
            data["profile"],
            data.get("stats", {}),
            data.get("status", {}).get("presence"),
            data.get("status", {}).get("premium", False),
            data.get("avatar_url"),
            data.get("assets", []),
        )
    else:
        console.print(ui.create_mini_header(data["profile"]))

    if data.get("assets"):
        ui.animate_section_header("Avatar Assets")
        ui.print_wearing_table(data["assets"])

    if data.get("friends_list"):
        ui.animate_section_header("Friends")
        ui.print_friends_table(data["friends_list"])

    if "favorites" in sections:
        ui.animate_section_header("Favorites")
        favorites = data.get("favorites", [])
        if favorites:
            ui.print_favorites_table(favorites)
        else:
            console.print(
                Panel(
                    "[dim yellow]No favorite games found or inventory is private.[/dim yellow]",
                    border_style="yellow",
                )
            )

    if data.get("badges"):
        ui.animate_section_header("Badges")
        ui.print_badges_table(data["badges"])

    if data.get("groups"):
        ui.animate_section_header("Groups")
        ui.print_groups_table(data["groups"])


def save_report(data, filename, file_format):
    lower_filename = filename.lower()
    if file_format == "json" or lower_filename.endswith(".json"):
        return exporter.export_json(data, filename)
    if file_format == "md" or lower_filename.endswith(".md"):
        return exporter.export_md(data, filename)
    return exporter.export_txt(data, filename)


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        sections = parse_sections(args)
    except argparse.ArgumentTypeError as exc:
        parser.error(str(exc))

    api = RobloxAPI(api_domain=resolve_api_domain(args.api))
    ui = RoFinderUI(theme=args.theme, animate=not args.no_anim and not args.json)

    if not args.json and not args.no_anim:
        ui.boot_sequence()
        ui.play_intro()
        ui.print_banner()
    elif not args.json:
        ui.print_banner()

    user_id, user_info = api.resolve_user(args.user)
    if not user_id:
        error = f"User '{args.user}' not found."
        if api.last_error:
            error = f"Could not resolve user '{args.user}'. {api.last_error}"
        error_console.print(f"[bold red]Error:[/bold red] {error}")
        return 1

    data = gather_intel_with_progress(
        api,
        user_id,
        user_info,
        sections,
        args.limit,
        show_progress=not args.json,
    )

    if args.json:
        print(json.dumps(data, indent=4))
    else:
        render_results(ui, data, sections)

    if args.save:
        with console.status("[bold yellow]Saving report..."):
            saved_path = save_report(data, args.save, args.format)
        console.print(f"\n[bold green]Report saved:[/bold green] {saved_path}")

    if not args.json:
        ui.outro(f"{APP_NAME} v{VERSION}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
