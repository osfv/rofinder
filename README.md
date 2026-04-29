# RoFinder v3

<div align="center">
  <img src="assets/rofinder.png" alt="RoFinder logo" width="160" />

  <h3>Fast Roblox profile intelligence from your terminal.</h3>

  <p>
    RoFinder gathers public Roblox account data, displays it in a clean Rich-powered CLI,
    and exports repeatable reports for later review.
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+" />
    <img src="https://img.shields.io/badge/Roblox-API-000000?style=for-the-badge&logo=roblox&logoColor=white" alt="Roblox API" />
    <img src="https://img.shields.io/github/license/osfv/rofinder?style=for-the-badge" alt="License" />
  </p>
</div>

## What It Does

RoFinder is a Roblox OSINT CLI for quick, structured checks on a username or user ID. It resolves the account, pulls public profile data, and can expand into network stats, presence, avatar assets, friends, favorites, badges, and groups.

It is built for public-data lookups. It does not bypass privacy settings, scrape credentials, or access private account data.

## Features

- Resolve usernames or numeric Roblox user IDs.
- Collect profile, creation date, ban status, verified badge, and display name.
- Pull follower/friend/following counts, presence status, premium signal, and last-online data when available.
- Inspect avatar headshot and currently worn avatar assets.
- Fetch optional friends, favorite games, badges, and groups with result limits.
- Export reports as JSON, TXT, or Markdown.
- Use `roproxy` by default, or switch directly to Roblox API domains.
- Disable animations or switch to a mono theme for cleaner logs.

## Install

```bash
git clone https://github.com/osfv/rofinder.git
cd rofinder
python -m pip install -r requirements.txt
```

## Quick Start

```bash
python rofinder.py roblox
```

Run a full lookup:

```bash
python rofinder.py roblox --full
```

Save a structured report:

```bash
python rofinder.py roblox --full --save reports/roblox.json --format json
```

## Usage

```bash
# Default profile, stats, presence, and avatar overview
python rofinder.py roblox

# Full sweep across every available section
python rofinder.py roblox --full

# Choose exact sections
python rofinder.py roblox --sections profile,stats,presence,badges,groups

# Avatar-focused lookup
python rofinder.py roblox --avatar

# Friends or favorites only
python rofinder.py roblox --friends --limit 25
python rofinder.py roblox --games --limit 25

# Machine-readable JSON output
python rofinder.py roblox --full --json

# Save reports
python rofinder.py roblox --full --save report.txt --format txt
python rofinder.py roblox --full --save report.md --format md
python rofinder.py roblox --full --save report.json --format json

# Cleaner terminal output
python rofinder.py roblox --no-anim
python rofinder.py roblox --theme mono

# API backend
python rofinder.py roblox --api roproxy
python rofinder.py roblox --api roblox
```

## Sections

Use `--sections` with a comma-separated list:

| Section | What it adds |
| --- | --- |
| `profile` | Basic account identity and creation metadata |
| `stats` | Friends, followers, and following counts |
| `presence` | Online state, last location, and premium signal |
| `avatar` | Avatar headshot URL |
| `assets` | Currently worn avatar items |
| `friends` | Friends list, limited by `--limit` |
| `favorites` | Favorite games, also available as `games` |
| `badges` | Recent badges |
| `groups` | Group memberships and roles |

## Exports

RoFinder can write reports to parent folders that do not exist yet:

```bash
python rofinder.py roblox --full --save output/roblox-report.md --format md
```

Formats:

- `json`: structured output with metadata.
- `txt`: plain readable intelligence report.
- `md`: Markdown report for sharing or notes.

## API Backends

Default backend:

```bash
python rofinder.py roblox --api roproxy
```

Direct Roblox API backend:

```bash
python rofinder.py roblox --api roblox
```

You can also set `ROFINDER_API_DOMAIN` when you need a custom compatible domain.

## Development

```bash
python -m pip install -r requirements-dev.txt
pytest -q
ruff check .
ruff format --check .
```

## License

MIT © 2026 [osfv](https://github.com/osfv)
