<div align="center">

# ▶️ YT Downloader

**Local web app for downloading YouTube videos as MP4 (up to 1080p) or audio as MP3 320 kbps / WAV.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-FF0000?logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)
[![FFmpeg](https://img.shields.io/badge/requires-FFmpeg-007808?logo=ffmpeg&logoColor=white)](https://ffmpeg.org/)
[![Node.js](https://img.shields.io/badge/requires-Node.js-5FA04E?logo=nodedotjs&logoColor=white)](https://nodejs.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](#-quick-start)
[![Localhost](https://img.shields.io/badge/runs%20on-localhost-blueviolet)](#-features)
[![Last commit](https://img.shields.io/github/last-commit/Sappyhad/youtube-downloader)](https://github.com/Sappyhad/youtube-downloader/commits)
[![Repo size](https://img.shields.io/github/repo-size/Sappyhad/youtube-downloader)](https://github.com/Sappyhad/youtube-downloader)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

Paste a YouTube link → pick a format → click **Download** → the file lands in your browser's downloads.

---

## ✨ Features

| Format | Quality | Details |
|--------|---------|---------|
| 🎬 **MP4** | up to 1920×1080 | H.264 + AAC — plays in every player |
| 📱 **MP4 (Shorts)** | up to 1080×1920 | vertical video in full Full HD |
| 🎵 **MP3** | 320 kbps | converted from the best available audio track |
| 🎚️ **WAV** | PCM 16-bit, 48 kHz | lossless copy of the best source |

- 🏆 **Always the best quality up to 1080p** — 4K sources are scaled down to Full HD, never below what the source offers.
- 📐 **Shorts-aware limit** — the cap applies to the **shorter side** of the frame, so Shorts come out as 1080×1920, not 608×1080.
- 🔁 **Auto-retry** — when YouTube rejects a stream URL (`HTTP 403`), the download restarts with fresh URLs (up to 3 attempts).
- 📊 **Progress bar** for downloading and converting.
- 🔒 **Local only** — the server listens on `127.0.0.1` and is not reachable from the network.

> [!NOTE]
> **About audio quality:** YouTube never serves MP3 or WAV. The source is always Opus (~160 kbps) or AAC (128 kbps).
> The app picks the best track and converts it exactly once. WAV can't add quality beyond the source, but it adds no
> further loss either — ideal for editing.

---

## 🧰 Requirements

- [Python](https://www.python.org/downloads/) 3.10+
- [FFmpeg](https://ffmpeg.org/) — merges video/audio streams and converts audio
- [Node.js](https://nodejs.org/) or [Deno](https://deno.com/) — used by yt-dlp to solve YouTube's JS challenges

---

## 🚀 Quick start

### 1. Clone and install

```bash
git clone https://github.com/Sappyhad/youtube-downloader.git
cd youtube-downloader
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt      # Windows
# .venv/bin/pip install -r requirements.txt        # macOS / Linux
```

### 2. Install FFmpeg

```powershell
winget install Gyan.FFmpeg      # Windows
# brew install ffmpeg           # macOS
# sudo apt install ffmpeg       # Debian / Ubuntu
```

### 3. Run

**Windows:** double-click `start.bat` — it starts the server and opens the browser.

**Manually:**

```bash
.venv\Scripts\python app.py
```

Then open <http://127.0.0.1:5000>, paste a link, choose a format and click **Download**.
A copy of every file is also kept in the `downloads/` folder.

---

## 🛠️ Troubleshooting

| Problem | What to do |
|---|---|
| `HTTP Error 403: Forbidden` after 3 attempts | YouTube is temporarily throttling your IP. Wait a few minutes and try again. |
| Downloads stopped working entirely | YouTube changed something — update yt-dlp: `.venv\Scripts\pip install -U "yt-dlp[default]"` |
| `FFmpeg is not installed` | Install FFmpeg (see above) and restart the server. |
| Stuck on "Fetching video info…" | Check the server window for errors; restart it if needed. |

---

## 🗂️ Project structure

```
youtube-downloader/
├── app.py             # Flask backend + yt-dlp
├── static/
│   ├── index.html     # web UI markup
│   ├── style.css      # styles
│   └── app.js         # UI logic (start job, poll progress, fetch file)
├── start.bat          # one-click launcher (Windows)
└── requirements.txt
```

---

## 📜 License

[MIT](LICENSE) © Sappyhad

---

<div align="center">
<sub>For personal use only. Download only content you have the rights to, and respect the <a href="https://www.youtube.com/t/terms">YouTube Terms of Service</a>.</sub>
</div>
