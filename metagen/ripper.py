import json
from os import replace, path, makedirs
from typing import Tuple, List

import requests
from yt_dlp import YoutubeDL
from yt_dlp.utils import sanitize_filename

import metagen
import metanums
from util import convert_invalid_characters

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
CURR_DIR = path.dirname(path.realpath(__file__))

FFMPEG_PATH = path.realpath(path.join(CURR_DIR, "..\\bin\\ffmpeg.exe"))

MEDIA_DIR = path.realpath(path.join(CURR_DIR, "..\\media"))
AUDIO_DIR = path.join(MEDIA_DIR, "audio")
THUMBNAIL_DIR = path.join(MEDIA_DIR, "thumbnails")

DRY_RUN = False
SKIP_THUMBNAILS = False

__video_type = "none"


# TODO make async
def download_thumbnails(playlist_title: str, artist_name: str, thumbnail_urls: List[str]) -> List[str]:
    print(f"[Debug] Urls {thumbnail_urls}")
    thumbnail_paths = []

    try:
        index = 0
        for url in thumbnail_urls:

            directory = path.join(THUMBNAIL_DIR, artist_name, playlist_title)
            file_path = path.join(directory, f"{index}.{url.split(".")[-1]}")

            if not path.exists(directory):
                makedirs(directory)

            if not SKIP_THUMBNAILS:
                response = requests.get(url)
                if response.status_code == 200:
                    with open(file_path, "wb") as file:
                        print(f"[Debug] Downloading thumbnail {file_path}")
                        file.write(response.content)
            thumbnail_paths.append(file_path)
            index += 1
    except Exception as e:
        print(e)

    print(f"[Debug] Thumbnail paths: {thumbnail_paths}")
    return thumbnail_paths


# TODO make async
def get_playlist_info(playlist_url: str) -> Tuple[List[str], str, str, List[str]]:
    ydl_opts = {
        "extract_flat": True,
        "no_warnings": True
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"[Log] Getting playlist: {playlist_url}")
            info = ydl.extract_info(playlist_url, download=False)
            json_info = json.loads(json.dumps(ydl.sanitize_info(info)))
            print(f"[Debug] Json data: {json_info}")

            global __video_type
            __video_type = json_info["_type"]

            playlist_tracks = []
            playlist_title = ""
            channel_name = json_info["channel"]
            if __video_type == "video":
                playlist_tracks.append(json_info["title"])
                thumbnail_urls = [json_info["thumbnail"]]
            elif __video_type == "playlist":
                playlist_title = json_info["title"]
                thumbnail_urls = [json_info["thumbnails"][-1]["url"].split("?")[0]] # playlist thumbnail
                for entry in json_info["entries"]:
                    playlist_tracks.append(entry["title"])
                    thumbnail_urls.append(entry["thumbnails"][-1]["url"].split("?")[0]) # track thumbnail
            thumbnail_paths = download_thumbnails(playlist_title, channel_name.strip(), thumbnail_urls)

            return playlist_tracks, playlist_title.strip(), channel_name.strip(), thumbnail_paths
        except json.decoder.JSONDecodeError:
            print("[Error] Invalid json obtained from playlist page.")
        except Exception as e:
            print(f"[Error] Failed to get playlist info {e}")

        return [], "", "", []


# TODO make async
def download_selected_videos(url: str, video_list: dict, vorbis_comments: dict):
    """
    :param url: (string) Valid URL
    :param video_list: (dict) Playlist object from cache.py
        key: (int) Video's position in playlist
        value (int, string):
            (int) user-defined tracknumber
            (string) title of the item selected
    :param vorbis_comments: (dict) Metadata object from cache.py
    :return:
    """
    if not video_list.items():
        print("[Error] Video list is empty.")
        return

    global __video_type
    print(f"[Log] url: {url}")

    artist = ""
    album = ""
    for comment in vorbis_comments:
        print(f"[Log] {comment}: {vorbis_comments[comment]}")

        if comment == metanums.VorbisComments.ARTIST.value:
            artist = convert_invalid_characters(vorbis_comments[comment])
        if comment == metanums.VorbisComments.ALBUM.value:
            album = convert_invalid_characters(vorbis_comments[comment])

    download_dir = AUDIO_DIR
    if artist != "":
        download_dir = path.join(download_dir, artist)
    if album != "":
        download_dir = path.join(download_dir, album)

    print("[Log] Pending Playlist")
    _playlist_items = ""
    for item in video_list.items():
        print(f"[Log] {item[1][0]}. {item[1][1]}")
        _playlist_items += f"{item[0]},"

    ydl_opts = {
        "format": "vorbis/bestaudio/best",
        "playlist_items": _playlist_items[:-1],
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "vorbis"}],
        "outtmpl": {"default": path.join(download_dir, "%(playlist_index)s.%(ext)s" if __video_type == "playlist" else "1.%(ext)s")},
        "ffmpeg_location": FFMPEG_PATH,
        "keepvideo": False,
        "no_warnings": True,
        "simulate": True if DRY_RUN else False
    }
    with YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(url)

    if error_code != 0:
        print(f"[Error] Download failed, aborting.")
        return

    if DRY_RUN:
        return

    filename_padding = len(f"{max({int(k):v for k,v in video_list.items()})}")
    for video in video_list.items():
        download_path = path.join(download_dir, f"{str(video[0]).zfill(filename_padding)}.ogg")
        title = f"{video[1][1]}.ogg"
        new_path = path.join(download_dir, sanitize_filename(title, restricted=True))

        try:
            replace(download_path, new_path)
            metagen.add_vorbis_metadata(new_path, title[:-4], str(video[1][0]), vorbis_comments)
        except FileNotFoundError as e:
            print(f"[Error] Download path: {download_path}\n\t\tNew Path: {new_path}\n\t\t{e}")


    print("[Log] Ripping complete")
