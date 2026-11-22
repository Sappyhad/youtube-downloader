<div align="center">

# ▶ YT Downloader

Lokalna aplikacja webowa do pobierania filmów z YouTube — wideo w **MP4 do 1080p** lub audio w **MP3 320 kbps** / **WAV**.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)
![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-FF0000?logo=youtube&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-required-007808?logo=ffmpeg&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![Localhost](https://img.shields.io/badge/runs%20on-localhost-blueviolet)

</div>

---

## Funkcje

| Format | Jakość | Szczegóły |
|--------|--------|-----------|
| **MP4** | do 1920×1080 | H.264 + AAC — działa w każdym odtwarzaczu |
| **MP4 (Shorts)** | do 1080×1920 | pionowe wideo w pełnym Full HD |
| **MP3** | 320 kbps | z najlepszej dostępnej ścieżki audio |
| **WAV** | PCM 16-bit, 48 kHz | bezstratny zapis najlepszego źródła |

- Zawsze najwyższa dostępna jakość do 1080p (materiały 4K są zmniejszane do Full HD, nigdy poniżej tego, co oferuje źródło).
- Limit liczony po **krótszym boku** obrazu, więc Shorts trafiają w 1080×1920, a nie w 608×1080.
- Pasek postępu pobierania i konwersji.
- Serwer nasłuchuje wyłącznie na `127.0.0.1` — niedostępny z sieci.

> **O jakości audio:** YouTube nie udostępnia MP3 ani WAV. Źródłem jest zawsze Opus (~160 kbps) lub AAC (128 kbps).
> Aplikacja wybiera najlepszą ścieżkę i konwertuje ją raz. WAV nie poprawi jakości ponad źródło, ale nie dokłada żadnej dodatkowej straty — idealny do dalszej obróbki.

## Wymagania

- [Python](https://www.python.org/) 3.10+
- [FFmpeg](https://ffmpeg.org/) (łączenie strumieni wideo/audio i konwersja)
- [Node.js](https://nodejs.org/) lub [Deno](https://deno.com/) (yt-dlp używa go do obsługi zabezpieczeń YouTube)

## Instalacja

```bash
git clone https://github.com/Sappyhad/youtube-downloader.git
cd youtube-downloader
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt      # Windows
# .venv/bin/pip install -r requirements.txt        # macOS / Linux
```

FFmpeg na Windows:

```powershell
winget install Gyan.FFmpeg
```

## Uruchomienie

**Windows:** dwuklik na `start.bat` — serwer wystartuje i otworzy przeglądarkę.

**Ręcznie:**

```bash
.venv\Scripts\python app.py
```

Następnie otwórz <http://127.0.0.1:5000>, wklej link, wybierz format i kliknij **Pobierz**.
Gotowy plik pobiera się przez przeglądarkę; kopia zostaje w katalogu `downloads/`.

## Aktualizacja yt-dlp

YouTube regularnie zmienia swoje API. Jeśli pobieranie przestanie działać:

```bash
.venv\Scripts\pip install -U "yt-dlp[default]"
```

## Struktura

```
├── app.py             # backend Flask + yt-dlp
├── static/index.html  # interfejs
├── start.bat          # szybki start (Windows)
└── requirements.txt
```

## Uwaga

Projekt do użytku prywatnego. Pobieraj tylko treści, do których masz prawa, zgodnie z [Warunkami korzystania z YouTube](https://www.youtube.com/t/terms).
