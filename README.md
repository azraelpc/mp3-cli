# YouTube to MP3 Downloader (CLI)

A lightweight, zero-configuration command-line Python tool to search for YouTube videos, filter out long content, and download the audio directly as high-quality MP3 files. It utilizes your system's native environment to securely bypass JavaScript challenges and bot detection without needing browser cookies.

## Features

- **Inline Arguments**: Pass search terms directly via the terminal command.
- **Interactive Search**: Prompt fallback if run without arguments.
- **Smart Filtering**: Automatically filters out videos longer than 10 minutes (e.g., podcasts, streams).
- **Clean Output**: Mutes generic verbose logs, displaying only a clean, native download progress bar.
- **Post-Download Options**: Options to download folder / play song / copy path to clipboard / exit.
- **Help Interface**: Clean manual available using `-H`, `-h`, or `--help` flags.

## Prerequisites (Important!)

Before running the script, ensure you have the following installed and configured in your system's `PATH`:

1. **Python 3.x**
2. **yt-dlp** (Python package)
3. **FFmpeg** (Required by `yt_dlp` for extracting and converting audio streams to `.mp3`)
4. **Deno** or **Node.js** (Required globally to automatically solve YouTube's internal JavaScript challenges)

## Installation

1. Clone or download `mp3.py` to your desired working directory.
2. Install the `yt_dlp` library using `pip`:

```bash
pip install -U yt-dlp
```

Note: ensure you don't have an old yt-dlp.exe (in windows) in the same folder, just in case.

3. Verify that `ffmpeg` and `deno` (or `node`) are accessible from your terminal:

```bash
ffmpeg -version
deno --version
```

## Usage

### Direct Search

Pass your search terms directly as arguments following the script name:

```bash
python mp3.py shakira the one
```

```bash
python mp3.py andy hunter go
```

### Interactive Mode

Run the script without arguments to be prompted for search terms:

```bash
python mp3.py
```

### Help Menu

Display the help interface and usage examples:

```bash
python mp3.py --help
```

## How It Works

1. **Metadata Extraction**: The script fetches up to 35 items matching your query using a flat extraction method that avoids heavy stream parsing.
2. **Duration Filter**: Videos over 600 seconds (10 minutes) are discarded. The top 25 results are displayed in an aligned index.
3. **Secure Download**: Upon selection, the script initiates a native shell subprocess invoking `yt-dlp`. This subprocess utilizes your global `Deno` engine to compute the signature challenges seamlessly.
4. **Conversion**: `FFmpeg` strips the video stream container and saves a 192kbps CBR `.mp3` directly in the execution folder.
