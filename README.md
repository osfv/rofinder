<div align="center">

# RoFinder v2

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=00ffff,ff00ff&height=180&section=header&text=RoFinder%20v2.4&fontSize=42&fontColor=fff&animation=fadeIn&fontAlignY=32&desc=Advanced%20Roblox%20OSINT%20%26%20Intelligence%20Tool&descAlignY=51&descAlign=50"/>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=3000&pause=1000&color=00FFFF&center=true&vCenter=true&multiline=true&repeat=true&width=600&height=100&lines=User+Intelligence+%F0%9F%94%8D+Asset+Forensics+%F0%9F%91%95+Activity+Tracking+%F0%9F%93%8A;Export+Reports+to+JSON+%2F+TXT;Built+by+osfv" alt="Typing SVG" />
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

## About RoFinder

<table>
<tr>
<td width="60%">

**RoFinder v2** is a professional-grade OSINT (Open Source Intelligence) tool for Roblox. It is designed to extract deep user information, analyze avatar assets, track activity status, and generate detailed reports in milliseconds.

Featuring a beautiful **Cyberpunk CLI** interface powered by `rich`, RoFinder transforms raw API data into readable, actionable intelligence. It supports exporting data to **JSON** for developers and **TXT** for shareable reports.

</td>
<td width="40%">

```text
╔═══════════════════════════╗
║   Why Choose RoFinder?    ║
╠═══════════════════════════╣
║ ⚡ Real-Time Presence     ║
║ 🎨 Cyberpunk UI           ║
║ 📂 JSON/TXT Exporting     ║
║ 👔 Avatar Asset Scan      ║
║ 💎 Premium Detection      ║
║ 🔒 100% Safe (Read-Only)  ║
╚═══════════════════════════╝
```

</td>
</tr>
</table>

<br>

## Features

<details open>
<summary><b>🕵️ User Intelligence</b></summary>
<br>

<table>
<tr><td>

- **Robust Lookup:** Advanced `POST` method resolution (100% accurate User IDs).
- **Deep Profile:** Account age, creation date, bio analysis.
- **Status Checks:** Detects **Premium** subscription and **Verified** badges.
- **Reputation:** Banned status detection.

</td></tr>
</table>

</details>

<details open>
<summary><b>👁️ Presence & Activity</b></summary>
<br>

<table>
<tr><td>

- **Real-Time Status:** Detects if user is **Online**, **Offline**, **In-Game**, or in **Roblox Studio**.
- **Last Seen:** Exact timestamp of when they were last active.
- **Game History:** Scans user's Favorite Games list.

</td></tr>
</table>

</details>

<details open>
<summary><b>👚 Avatar Forensics</b></summary>
<br>

<table>
<tr><td>

- **Asset Scanner:** Lists every item the user is currently wearing.
- **Item IDs:** Returns Asset IDs for Hats, Shirts, Faces, and Accessories.
- **Thumbnails:** Fetches high-res avatar headshot URLs.

</td></tr>
</table>

</details>

<details open>
<summary><b>💾 Data Exporting</b></summary>
<br>

<table>
<tr><td>

- **Developer Ready:** Export full datasets to `.json`.
- **Report Mode:** Generate clean, readable `.txt` files for sharing.
- **Timestamps:** All exports include generation time for record keeping.

</td></tr>
</table>

</details>

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

### ⚡ Quick Lookup
Get basic stats and ID.
```bash
python rofinder.py roblox
```

### 🔍 Detailed Intelligence
Fetches Badges, Groups, Avatar Items, and Favorites.
```bash
python rofinder.py roblox --detailed
```

### 💾 Generate Text Report
Saves a readable file `report.txt` to your folder.
```bash
python rofinder.py roblox --save report.txt
```

### 👨‍💻 Developer JSON Export
Dumps raw data for use in your own apps.
```bash
python rofinder.py roblox --detailed --save data.json --format json
```

</div>

<br>

## Screenshots / Demo

```text
 ____       _____ _           _           
|  _ \ ___ |  ___(_)_ __   __| | ___ _ __ 
| |_) / _ \| |_  | | '_ \ / _` |/ _ \ '__|
|  _ < (_) |  _| | | | | | (_| |  __/ |   
|_| \_\___/|_|   |_|_| |_|\__,_|\___|_|   

            By osfv

╭─ User Intelligence: Roblox ────────────────────────────────────────────────╮
│                                      │ Metric      │                 Value │
│  User:    @Roblox  ☑️  💎 PREM       │ Friends     │                   169 │
│  Display: Roblox                     │ Followers   │            12,405,102 │
│  ID:      1                          │ Following   │                     0 │
│  Status:  ● Online                   │ Banned      │                    No │
│  Seen:    2025-01-01 12:30           ╰─────────────┴───────────────────────╯
│  Age:     6345 days                                                         
│                                                                            
╰────────────────────────────────────────────────────────────────────────────╯
```

<br>

## Roadmap

<div align="center">

```mermaid
gantt
    title RoFinder Development
    dateFormat  YYYY-MM-DD
    section v1.0
    Basic Lookup           :done, 2024-01-01, 30d
    section v2.0
    UI Overhaul (Rich)     :done, 2024-02-01, 15d
    Presence Detection     :done, 2024-02-05, 10d
    section v2.4 (Current)
    Export System          :done, 2024-02-15, 5d
    Avatar Forensics       :done, 2024-02-20, 5d
    section Future
    Discord Webhooks       :active, 2024-04-01, 30d
    GUI Mode               :2024-05-01, 60d
```

</div>

<br>

## License

<div align="center">

This project is licensed under the **MIT License**.

Copyright (c) 2026 **osfv**

</div>

