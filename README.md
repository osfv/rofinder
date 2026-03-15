# RoFinder v3

A fast, clean Roblox OSINT CLI with reliable API calls, a dashboard-style interface, and flexible exports.

## Features

- Resilient API client (retries, pagination, caching)
- Neon dashboard UI with optional animations
- Sectioned intelligence: profile, presence, avatar, friends, favorites, badges, groups
- Export reports to JSON, TXT, or Markdown

## Requirements

- Python 3.8+

## Quick Start

```bash
git clone https://github.com/osfv/rofinder.git
cd rofinder
pip install -r requirements.txt
python rofinder.py roblox
```

## Usage

```bash
# Full sweep
python rofinder.py roblox --full

# Custom sections
python rofinder.py roblox --sections profile,stats,presence,badges,groups

# Avatar only
python rofinder.py roblox --avatar

# Save reports
python rofinder.py roblox --full --save report.json --format json
python rofinder.py roblox --full --save report.md --format md

# UI options
python rofinder.py roblox --no-anim
python rofinder.py roblox --theme mono
```

## Sections

Available for `--sections`:

- `profile`, `stats`, `presence`, `avatar`, `assets`, `friends`, `favorites`, `badges`, `groups`

## Exports

- `json` for structured data
- `txt` for readable reports
- `md` for shareable Markdown

## API

RoFinder uses the `roproxy.com` domain by default. To switch back to official Roblox APIs:

```bash
# Windows (PowerShell)
$env:ROFINDER_API_DOMAIN="roblox.com"
python rofinder.py roblox
```

## License

MIT © 2026 osfv
