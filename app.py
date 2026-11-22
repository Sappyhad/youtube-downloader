"""Local YouTube downloader: MP4 (max 1080p), MP3 (320 kbps), WAV (PCM)."""

import ctypes
import os
import shutil
import threading
import uuid
from pathlib import Path
from urllib.parse import urlparse

from flask import Flask, abort, jsonify, request, send_file, send_from_directory
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

BASE_DIR = Path(__file__).resolve().parent
DOWNLOAD_DIR = BASE_DIR / "downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "music.youtube.com", "youtu.be"}
FORMATS = {"mp4", "mp3", "wav"}
MAX_ATTEMPTS = 3

app = Flask(__name__, static_folder=BASE_DIR / "static")
jobs: dict[str, dict] = {}
jobs_lock = threading.Lock()


def find_ffmpeg_dir() -> str | None:
    found = shutil.which("ffmpeg")
    if found:
        return str(Path(found).parent)
    # Fallback for shells started before `winget install Gyan.FFmpeg` updated PATH.
    winget_packages = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Packages"
    candidates = sorted(winget_packages.glob("Gyan.FFmpeg*/*/bin/ffmpeg.exe"))
    return str(candidates[-1].parent) if candidates else None


FFMPEG_DIR = find_ffmpeg_dir()


def is_youtube_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and (parsed.hostname or "").lower() in ALLOWED_HOSTS


def build_options(fmt: str, job_id: str) -> dict:
    options = {
        "outtmpl": str(DOWNLOAD_DIR / job_id / "%(title)s [%(id)s].%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        "ffmpeg_location": FFMPEG_DIR,
        "js_runtimes": {"node": {}, "deno": {}},
        "progress_hooks": [lambda d: on_progress(job_id, d)],
        "postprocessor_hooks": [lambda d: on_postprocess(job_id, d)],
    }
    if fmt == "mp4":
        # "res" = shorter side, so 1080 caps landscape at 1920x1080 and Shorts at 1080x1920.
        # Prefer H.264 + AAC for maximum MP4 player compatibility; resolution always wins over codec.
        options["format"] = "bv*+ba/b"
        options["format_sort"] = ["res:1080", "fps", "vcodec:h264", "acodec:m4a"]
        options["merge_output_format"] = "mp4"
    else:
        # YouTube never serves MP3/WAV: take the best source audio (Opus/AAC) and convert once.
        options["format"] = "bestaudio/best"
        extract = {"key": "FFmpegExtractAudio", "preferredcodec": fmt}
        if fmt == "mp3":
            extract["preferredquality"] = "320"
        options["postprocessors"] = [extract, {"key": "FFmpegMetadata"}]
    return options


def update_job(job_id: str, **fields) -> None:
    with jobs_lock:
        jobs[job_id].update(fields)


def on_progress(job_id: str, d: dict) -> None:
    if d["status"] == "downloading":
        total = d.get("total_bytes") or d.get("total_bytes_estimate")
        percent = round(d["downloaded_bytes"] / total * 100, 1) if total else None
        update_job(job_id, status="downloading", percent=percent)
    elif d["status"] == "finished":
        update_job(job_id, status="processing", percent=100)


def on_postprocess(job_id: str, d: dict) -> None:
    if d["status"] == "started":
        update_job(job_id, status="processing")


def download_with_retry(job_id: str, url: str, fmt: str) -> dict:
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            with YoutubeDL(build_options(fmt, job_id)) as ydl:
                return ydl.extract_info(url, download=True)
        except DownloadError as exc:
            # YouTube sporadically rejects a signed stream URL; a fresh extraction gets new URLs.
            if "HTTP Error 403" not in str(exc) or attempt == MAX_ATTEMPTS:
                raise
            update_job(job_id, status="queued", percent=0)


def run_job(job_id: str, url: str, fmt: str) -> None:
    try:
        info = download_with_retry(job_id, url, fmt)
        files = [p for p in (DOWNLOAD_DIR / job_id).iterdir() if p.suffix == f".{fmt}"]
        if not files:
            raise RuntimeError("Output file not found after download.")
        height, width = info.get("height"), info.get("width")
        update_job(
            job_id,
            status="done",
            percent=100,
            title=info.get("title"),
            file=str(files[0]),
            resolution=f"{width}x{height}" if fmt == "mp4" and width and height else None,
        )
    except Exception as exc:  # surface any yt-dlp/ffmpeg failure to the UI
        update_job(job_id, status="error", error=str(exc))


@app.get("/")
def index():
    return send_from_directory(BASE_DIR / "static", "index.html")


@app.post("/api/download")
def start_download():
    if not request.is_json:  # JSON forces a CORS preflight, so other websites can't trigger jobs
        abort(415)
    url = (request.json.get("url") or "").strip()
    fmt = request.json.get("format")
    if not is_youtube_url(url):
        return jsonify(error="To nie jest link do YouTube."), 400
    if fmt not in FORMATS:
        return jsonify(error="Nieznany format."), 400
    if not FFMPEG_DIR:
        return jsonify(error="Brak ffmpeg w systemie."), 500

    job_id = uuid.uuid4().hex
    with jobs_lock:
        jobs[job_id] = {"status": "queued", "percent": 0, "format": fmt}
    threading.Thread(target=run_job, args=(job_id, url, fmt), daemon=True).start()
    return jsonify(job_id=job_id)


@app.get("/api/status/<job_id>")
def job_status(job_id: str):
    with jobs_lock:
        job = jobs.get(job_id)
        if not job:
            abort(404)
        return jsonify({k: v for k, v in job.items() if k != "file"})


@app.get("/api/file/<job_id>")
def job_file(job_id: str):
    with jobs_lock:
        job = jobs.get(job_id)
    if not job or job["status"] != "done":
        abort(404)
    return send_file(job["file"], as_attachment=True)


def disable_console_quick_edit() -> None:
    """Clicking a Windows console enters QuickEdit selection, which blocks every write to it and freezes the server."""
    if os.name != "nt":
        return
    kernel32 = ctypes.windll.kernel32
    stdin_handle = kernel32.GetStdHandle(-10)  # STD_INPUT_HANDLE
    mode = ctypes.c_uint32()
    if kernel32.GetConsoleMode(stdin_handle, ctypes.byref(mode)):
        enable_quick_edit, enable_extended_flags = 0x0040, 0x0080
        kernel32.SetConsoleMode(stdin_handle, (mode.value & ~enable_quick_edit) | enable_extended_flags)


if __name__ == "__main__":
    disable_console_quick_edit()
    app.run(host="127.0.0.1", port=5000, threaded=True)
