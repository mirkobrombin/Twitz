import os
from pathlib import Path

twitch_streamer_uri = "https://twitch.tv/%s"
twitch_chat_uri = f"https://twitch.tv/popout/%s/chat?darkpopout"
cookies_path = f"{Path.home()}/.cache/cookies.txt"

if "SNAP" in os.environ:
    cookies_path = f"{os.environ['SNAP_USER_DATA']}/cookies.txt"
