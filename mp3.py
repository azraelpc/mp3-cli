import sys
import os
import subprocess
import urllib.parse
from yt_dlp import YoutubeDL

HELP_TEXT = """
====================================================================
YOUTUBE MP3 DOWNLOADER - HELP
====================================================================
Usage:
  python mp3.py [search terms]

Examples:
  python mp3.py shakira the one
  python mp3.py andy hunter go

If you run the script without parameters, it will prompt you for them.
====================================================================
"""

def display_header():
    print("=========================")
    print("YOUTUBE TO MP3 DOWNLOADER")
    print("=========================")

def search_and_download_audio():
    # 1. Manage arguments and help flags
    arguments = sys.argv[1:]
    
    if any(arg in arguments for arg in ["-h", "--help", "-H"]):
        print(HELP_TEXT)
        return

    display_header()

    # Process arguments if present; otherwise prompt the user
    if arguments:
        search_query = " ".join(arguments).strip()
        print(f"Search terms: {search_query}")
    else:
        search_query = input("Enter search terms: ").strip()
        if not search_query:
            print("\n[!] Search query cannot be empty.")
            return

    print("\nSearching for videos with songs...")

    query_encoded = urllib.parse.quote_plus(search_query)
    url_search = f"https://www.youtube.com/results?search_query={query_encoded}"

    # FIX: Increased playlistend to 35 to ensure we get at least 25 results 
    # even after filtering out videos longer than 10 minutes.
    search_options = {
        'extract_flat': 'in_playlist',
        'playlistend': 35,
        'quiet': True,
    }

    try:
        with YoutubeDL(search_options) as ydl:
            result = ydl.extract_info(url_search, download=False)

            if 'entries' not in result or not result['entries']:
                print("\n[!] No videos found.")
                return

            # Filter out entries longer than 10 minutes (600 seconds)
            filtered_videos = []
            for video in result['entries']:
                if video and video.get('duration'):
                    if video['duration'] < 600:
                        filtered_videos.append(video)

            if not filtered_videos:
                filtered_videos = [v for v in result['entries'] if v is not None]

            # Caps the list strictly at 25 results
            videos = filtered_videos[:25]

            # 2. Display results cleanly
            print("\n" + "-" * 28 + " RESULTS " + "-" * 29)
            for idx, video in enumerate(videos, start=1):
                duration_str = ""
                if video.get('duration'):
                    duration_min = int(video['duration']) // 60
                    duration_seg = int(video['duration']) % 60
                    duration_str = f" ({duration_min}:{duration_seg:02d})"
                print(f" [{idx:2d}] {video.get('title')}{duration_str}")
            print("-" * 68)

            # 3. Handle user selection
            while True:
                try:
                    selection = int(input("\nSelect video number: "))
                    if 1 <= selection <= len(videos):
                        chosen_video = videos[selection - 1]
                        break
                    else:
                        print(f"[!] Please select a number between 1 and {len(videos)}.")
                except ValueError:
                    print("[!] Please enter a valid number.")

            video_url = f"https://www.youtube.com/watch?v={chosen_video['id']}"
            
            print(f"\nPreparing download for: {chosen_video.get('title')}\n")

            # 4. Streamlined native execution with progress bar only
            command = [
                "yt-dlp",
                "-x",                       # Extract audio
                "--audio-format", "mp3",    # Target format
                "--audio-quality", "192K",  # Quality setting
                "--quiet",                  # Mutes backend network/signature logs
                "--no-warnings",            # Disables generic warnings
                "--progress",               # Forces the dynamic progress bar display
                video_url
            ]

            subprocess.run(command, check=True)
            print("\nDownload and MP3 conversion completed successfully.")
            
            # 5. Post-download prompt to open destination folder
            open_folder = input("Do you want to open the destination folder? (y/n): ").strip().lower()
            if open_folder in ["y", "yes"]:
                # Executes 'start .' safely via the shell on Windows
                os.system("start .")

            print("")

    except subprocess.CalledProcessError:
        print("\n[!] An error occurred during the download process.")
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")

if __name__ == "__main__":
    search_and_download_audio()
