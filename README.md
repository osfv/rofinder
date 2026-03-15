<div align="center">

# RoFinder v3

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=00ffff,ff00ff&height=180&section=header&text=RoFinder%20v3.0&fontSize=42&fontColor=fff&animation=fadeIn&fontAlignY=32&desc=Remastered%20Roblox%20OSINT%20%26%20Intelligence%20Suite&descAlignY=51&descAlign=50"/>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=2800&pause=900&color=00FFFF&center=true&vCenter=true&multiline=true&repeat=true&width=640&height=100&lines=Neon+Intel+Dashboard+%7C+Rapid+Signal+Scan;Export+Reports+to+JSON+%2F+TXT+%2F+MD;Built+by+osfv" alt="Typing SVG" />
</p>

<p align="center">
  <a href="https://github.com/osfv/rofinder/releases">
    <img src="https://img.shields.io/github/downloads/osfv/rofinder/total?style=for-the-badge&logo=github&color=7C3AED&labelColor=1e1e2e&logoColor=white" alt="Downloads"/>
  </a>
  <a href="https://github.com/osfv/rofinder/stargazers">
    <img src="https://img.shields.io/github/stars/osfv/rofinder?style=for-the-badge&logo=starship&color=FF6B6B&labelColor=1e1e2e&logoColor=white" alt="Stars"/>
  </a>
  <a href="https://github.com/osfv/rofinder/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/osfv/rofinder?style=for-the-badge&color=95E1D3&labelColor=1e1e2e" alt="License"/>
  </a>
  <a href="https://github.com/osfv/rofinder/commits/main">
    <img src="https://img.shields.io/github/last-commit/osfv/rofinder?style=for-the-badge&color=F8A5C2&labelColor=1e1e2e" alt="Last Commit"/>
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=1e1e2e" alt="Python"/>
  <img src="https://img.shields.io/badge/Roblox-API-000000?style=for-the-badge&logo=roblox&logoColor=white&labelColor=1e1e2e" alt="Roblox API"/>
  <img src="https://img.shields.io/badge/Status-Operational-00C851?style=for-the-badge&logoColor=white&labelColor=1e1e2e" alt="Status"/>
</p>

<p align="center">
  <a href="#installation"><kbd> <br> Installation <br> </kbd></a>&ensp;&ensp;
  <a href="#usage"><kbd> <br> Usage <br> </kbd></a>&ensp;&ensp;
  <a href="#features"><kbd> <br> Features <br> </kbd></a>&ensp;&ensp;
  <a href="#exporting"><kbd> <br> Exporting <br> </kbd></a>
</p>

</div>

<br>

## About RoFinder v3

RoFinder v3 is a full rebuild of the original CLI into a faster, cleaner intelligence suite for Roblox OSINT work. The API client now includes retries, pagination, and lightweight caching for better reliability, while the UI shifts to a neon dashboard layout with animated boot and section headers.

Exports are available in JSON, TXT, and Markdown to cover developer workflows and shareable reports.

<br>

## Features

- Resilient API client (retries, pagination, caching)
- Remastered neon dashboard layout with animated intro
- Sectioned intelligence: profile, presence, avatar, friends, favorites, badges, groups
- Export reports to JSON, TXT, or Markdown
- Backwards-compatible flags for v2 users

<br>

## Installation

<div align="center">

### 1. Clone the Repository
```bash
git clone https://github.com/osfv/rofinder.git
cd rofinder
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run RoFinder
```bash
python rofinder.py --help
```

</div>

<br>

## Usage

<div align="center">

### Quick Summary
```bash
python rofinder.py roblox
```

### Full Intelligence Sweep
```bash
python rofinder.py roblox --full
```

### Custom Sections
```bash
python rofinder.py roblox --sections profile,stats,presence,badges,groups
```

### Avatar Forensics Only
```bash
python rofinder.py roblox --avatar
```

### Save JSON Report
```bash
python rofinder.py roblox --full --save report.json --format json
```

### Save Markdown Report
```bash
python rofinder.py roblox --full --save report.md --format md
```

### Disable Animations
```bash
python rofinder.py roblox --no-anim
```

### Monochrome Theme
```bash
python rofinder.py roblox --theme mono
```

</div>

<br>

## Exporting

RoFinder can generate developer-friendly JSON exports or clean TXT/Markdown reports for sharing and archiving.

<br>

## Roadmap

<div align="center">

```mermaid
gantt
    title RoFinder Development
    dateFormat  YYYY-MM-DD
    section v3.0 (Current)
    Remastered UI           :done, 2026-03-01, 7d
    Resilient API Client    :done, 2026-03-05, 5d
    section Next
    GUI Mode                :2026-04-01, 60d
    Discord Webhooks        :2026-05-15, 30d
```

</div>

<br>

## License

<div align="center">

This project is licensed under the **MIT License**.

Copyright (c) 2026 **osfv**

</div>
