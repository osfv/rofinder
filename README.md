<div align="center">

# RoFinder v3

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&duration=2200&pause=900&color=00FFFF&center=true&vCenter=true&width=520&lines=Remastered+Roblox+OSINT+CLI;Fast+intel+%7C+Clean+reports" alt="Typing" />

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Roblox](https://img.shields.io/badge/Roblox-API-000000?style=for-the-badge&logo=roblox&logoColor=white)
![License](https://img.shields.io/github/license/osfv/rofinder?style=for-the-badge)
![Last Commit](https://img.shields.io/github/last-commit/osfv/rofinder?style=for-the-badge)

</div>

## What It Is

A fast, clean Roblox OSINT CLI with reliable API calls, a dashboard-style interface, and flexible exports.

## ⚡ Features

- Resilient API client (retries, pagination, caching)
- Neon dashboard UI with optional animations
- Sectioned intelligence: profile, presence, avatar, friends, favorites, badges, groups
- Export reports to JSON, TXT, or Markdown

## 🚀 Quick Start

```bash
git clone https://github.com/osfv/rofinder.git
cd rofinder
pip install -r requirements.txt
python rofinder.py roblox
```

## 🔍 Usage

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

## 🧩 Sections

Available for `--sections`:

- `profile`, `stats`, `presence`, `avatar`, `assets`, `friends`, `favorites`, `badges`, `groups`

## 📦 Exports

- `json` for structured data
- `txt` for readable reports
- `md` for shareable Markdown

## 📄 License

MIT © 2026 osfv
