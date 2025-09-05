import os
import json
from typing import Tuple, List

import metanums
import metagen
import subprocess
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURR_DIR = os.path.dirname(os.path.realpath(__file__))

YTDLP_PATH = os.path.join(CURR_DIR, "..\\bin\\yt-dlp.exe")
FFMPEG_PATH = os.path.join(CURR_DIR, "..\\bin\\ffmpeg.exe")
FFPROBE_PATH = os.path.join(CURR_DIR, "..\\bin\\ffprobe.exe")

DOWNLOAD_DIR = os.path.join(CURR_DIR, "..\\Ripped Audio")
AUDIO_ARGS = "--extract-audio --audio-format vorbis --audio-quality 0"
FILENAME_ARGS = "--restrict-filenames"
OPTIONS = "--abort-on-error"
SIM_ARGS = "-s --get-filename"

CLEAR_ON_FAILED_DOWNLOAD = True
DRY_RUN = False


def convert_invalid_characters(string: str) -> str:
    if string is not None:
        double_quotes = "\""
        question_mark = r"\?"
        right_quote = "’"
        invalid_filename_chars = "[\\/:*<>|]"

        string = re.sub(double_quotes, "", string)
        string = re.sub(question_mark, " ", string)
        string = re.sub(right_quote, "'", string)
        string = re.sub(invalid_filename_chars, "_", string)
        string = string.strip()

    return string


def correct_invalid_json(invalid_json: str) -> str:
    print(invalid_json)
    pattern_title = re.compile(fr"\"title\":\s*\"(.*?)\"(,|\s*}})")
    match_title = re.search(pattern_title, invalid_json)
    # https://www.youtube.com/playlist?list=OLAK5uy_mFNUV0q9q1Fu5Q0J3zsQ81lYiV_hV_fcM

    if match_title:
        validated_json = ""
        for match in match_title.groups():
            # matched_text = match
            replacement_text = re.sub(match, re.sub("\"", "", match_title.group(1)), match)
            # replacement_text = re.sub(match, re.sub("\"", "", match_title.group(1)), match)
            # validated_json += re.sub()

            print(validated_json)
        return validated_json
    else:
        return invalid_json


def fix_title(artist, filename):
    print(f"[Log] Original filename: {filename}")
    if artist != "":
        # pattern_open_paren = re.compile(r"\s*(\(|\[)")
        # pattern_no_close_paren = re.compile(r"[^()|\])]*")
        # pattern_lyric_video = re.compile(r"(\s*(\(|\[)[^()|\])]*(Video|Audio|Lyric|Official)[^()|\])]*(\)|]))")
        # pattern_starting_artist = re.compile(fr"(^[^-]*({artist})[^-]*(-\s*|\sx\s))")

        # temp_artist = artist.replace(" ", "_")
        pattern_starting_artist = re.compile(fr"(^.*?{artist}[^-]*(- *| x ))", re.IGNORECASE)
        # pattern_starting_artist = re.compile(fr"(^[^-]*({artist})[^-]*(- *| x ))")
        match_starting_artist = re.search(pattern_starting_artist, filename)

        if match_starting_artist is not None:
            # for group in match_starting_artist.groups():
            #     print(group)
            filename = re.sub(match_starting_artist.group(1), "", filename)
            print(f"[Log] After removing artist name: {filename}")

    pattern_lyric_video = re.compile(r"\s*(\(|\[)?(Official|Lyric)( Audio| Music| Lyric)?( Video| Audio)(\)|\])?", re.IGNORECASE)
    # pattern_lyric_video = re.compile(r"(\s*(\(|\[)[^(\)|\])]*(Video|Audio|Lyric|Official)[^(\)|\])]*(\)|\]))")
    match_lyric_video = re.search(pattern_lyric_video, filename)
    if match_lyric_video is not None:
        filename = filename.replace(match_lyric_video.group(), "")
        print(f"[Log] After removing video type: {filename}")
    return filename


def get_playlist_info(playlist_url: str) -> Tuple[List[str], str, str]:
    # command = f"\"{YTDLP_PATH}\" --flat-playlist -e -J --get-filename {FILENAME_ARGS} -o %(title)s {playlist_url}"
    command = f"\"{YTDLP_PATH}\" --flat-playlist -e -J --get-filename -o %(title)s {playlist_url}"

    raw_playlist = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode("unicode_escape")
    raw_playlist = raw_playlist.splitlines()

    playlist = []
    playlist_title = ""
    channel_name = ""
    if len(raw_playlist) > 0:
        json_info = raw_playlist.pop(len(raw_playlist) - 1)

        for i in range(1, len(raw_playlist), 2):
            playlist.append(raw_playlist[i])

        try:
            # correct_invalid_json(json_info)
            print(f"[Debug] {json_info}")
            json_dump = json.loads(json_info)
            playlist_title = json_dump["title"]
            channel_name = json_dump["channel"]
        except json.decoder.JSONDecodeError:
            print("[Error] Invalid json obtained from playlist page.")
    else:
        print("[Error] Playlist is empty")

    return playlist, playlist_title, channel_name


def rip_selected_videos(url: str, video_list: dict, vorbis_comments: dict):
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
    log = f"[Log] url: {url}\n"

    artist = ""
    album = ""
    for comment in vorbis_comments:
        log += f"[Log] {comment}: {vorbis_comments[comment]}\n"

        if comment == metanums.VorbisComments.ARTIST.value:
            artist = convert_invalid_characters(vorbis_comments[comment])
        if comment == metanums.VorbisComments.ALBUM.value:
            album = convert_invalid_characters(vorbis_comments[comment])

    print(log)

    playlist_items = "--playlist-items "

    print("[Log] Pending Playlist")
    for item in video_list.items():
        print(f"[Log] {item[1][0]}. {item[1][1]}")
        playlist_items += f"{item[0]},"

    playlist_items = playlist_items[:-1]

    download_dir = f"{DOWNLOAD_DIR}\\"
    if artist != "":
        download_dir += f"{artist}\\"
    if album != "":
        download_dir += f"{album}\\"

    output_template = f"-o \"{download_dir}%(playlist_index)s.%(ext)s\""
    if DRY_RUN:
        command = f"\"{YTDLP_PATH}\" {playlist_items} {AUDIO_ARGS} {SIM_ARGS} {OPTIONS} {output_template} {url}"
    else:
        command = f"\"{YTDLP_PATH}\" {playlist_items} {AUDIO_ARGS} {OPTIONS} {output_template} {url}"
    print(f"[Log] {command}")

    result = subprocess.run(command, stderr=subprocess.PIPE).stderr.decode("unicode_escape")

    if DRY_RUN:
        return

    if result != "":
        print(f"[Error] Download failed. {result}\n[Error] Aborting.")

        if CLEAR_ON_FAILED_DOWNLOAD:
            print("[Debug] Removing downloaded files")
            for root, dirs, files in os.walk(download_dir):
                for file in files:
                    r_path = os.path.join(root, file)
                    print(f"[Debug] Removing {r_path}")
                    os.remove(r_path)
        return

    filename_padding = len(f"{(list(video_list.keys())[-1])}")
    for item in video_list.items():
        indexed_filename = f"{str(item[0]).zfill(filename_padding)}.ogg"
        indexed_filepath = os.path.join(download_dir, indexed_filename)
        filename = convert_invalid_characters(f"{item[1][1]}.ogg")
        filepath = os.path.join(download_dir, filename)

        try:
            os.replace(indexed_filepath, filepath)
        except FileNotFoundError:
            print(f"[Error] Could not replace file: {indexed_filepath}")

        # filename = fix_title(artist, filename)

        original_filepath = filepath
        filepath = os.path.join(download_dir, filename)

        try:
            os.replace(original_filepath, filepath)
        except FileNotFoundError:
            print(f"[Error] Could not find file file: {original_filepath}")

        if os.path.isfile(filepath):
            metagen.add_vorbis_metadata(filepath, filename[:-4], str(item[1][0]), vorbis_comments)
        else:
            print(f"[Error] Path is not a file: {filepath}")
    print("[Log] Ripping complete")
