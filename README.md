<div align="center">

```
██████╗  ██████╗ ███████╗██╗███╗   ██╗██████╗ ███████╗██████╗
██╔══██╗██╔═══██╗██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
██████╔╝██║   ██║█████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝
██╔══██╗██║   ██║██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
██║  ██║╚██████╔╝██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║
╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                          V3
```

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=15&duration=2200&pause=900&color=00FFFF&center=true&vCenter=true&width=520&lines=Remastered+Roblox+OSINT+CLI;Fast+intel+%7C+Clean+reports+%7C+Zero+fluff" alt="Typing SVG" />

<br/>

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0d0d0d)](https://python.org)
[![Roblox API](https://img.shields.io/badge/Roblox-API-00FFFF?style=for-the-badge&logo=roblox&logoColor=white&labelColor=0d0d0d)](https://roblox.com)
[![Last Commit](https://img.shields.io/github/last-commit/osfv/rofinder?style=for-the-badge&labelColor=0d0d0d&color=00ff99)](https://github.com/osfv/rofinder/commits/main)

**[Install](#-quick-start) · [Usage](#-usage) · [Sections](#-sections) · [Exports](#-exports)**

</div>

---

## What is RoFinder?

RoFinder is a Roblox OSINT CLI. Point it at a username and get back a full intelligence report. Profile, presence, avatar assets, friends, badges, groups.

No login. No cookies. 100% read-only.

---

## ✦ Features

| | |
|---|---|
| **Resilient API client** | Auto-retry, pagination, response caching, dual backend support (`roblox` / `roproxy`) |
| **Sectioned intel** | Run only what you need: profile, presence, avatar, assets, friends, favorites, badges, groups |
| **Flexible exports** | Dump reports to `.json`, `.txt`, or `.md` |

---

## ⚡ Quick Start

```bash
git clone https://github.com/osfv/rofinder.git
cd rofinder
pip install -r requirements.txt
python rofinder.py roblox
```

> Requires Python 3.8+

---

## 🔍 Usage

```bash
# Full sweep — all sections
python rofinder.py <username> --full

# Pick specific sections
python rofinder.py <username> --sections profile,stats,presence,badges,groups

# Avatar assets only
python rofinder.py <username> --avatar

# Export a report
python rofinder.py <username> --full --save report.json --format json
python rofinder.py <username> --full --save report.md   --format md
python rofinder.py <username> --full --save report.txt  --format txt

# UI tweaks
python rofinder.py <username> --no-anim     # disable animations
python rofinder.py <username> --theme mono  # monochrome terminal theme

# Switch API backend
python rofinder.py <username> --api roproxy  # default
python rofinder.py <username> --api roblox   # direct
```

---

## 🧩 Sections

Use any combination with `--sections`:

```
profile · stats · presence · avatar · assets · friends · favorites · badges · groups
```

---

## 📦 Exports

| Flag | Output |
|---|---|
| `--format json` | Structured data, ready for scripts or further processing |
| `--format txt` | Clean, human-readable report for sharing |
| `--format md` | Markdown — paste straight into docs or Discord |

---

## 🔗 API Backend

RoFinder defaults to **roproxy** to avoid rate limits. Switch to the official API with `--api roblox`.

```bash
python rofinder.py <username> --api roblox
```

---

## 📄 License

MIT © 2026 [osfv](https://github.com/osfv)
