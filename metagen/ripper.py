import os
import json
import metagen
import subprocess
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURR_DIR = os.path.dirname(os.path.realpath(__file__))

YOUTUBEDL_PATH = os.path.join(CURR_DIR, "../bin/youtube-dl.exe")
FFMPEG_PATH = os.path.join(CURR_DIR, "../bin/ffmpeg.exe")
FFPROBE_PATH = os.path.join(CURR_DIR, "../bin/ffprobe.exe")

DOWNLOAD_DIR = "../Ripped Audio"
AUDIO_ARGS = "--extract-audio --audio-format vorbis --audio-quality 0"
FILENAME_ARGS = "--restrict-filenames"

videos = {}
IS_SELECTED_INDEX = 0
TITLE_INDEX = 1


def convert_invalid_characters(string):
    double_quotes = "\""
    question_mark = r"\?"
    right_quote = "’"
    invalid_filename_chars = "[\\/:*<>|]"

    string = re.sub(double_quotes, "'", string)
    string = re.sub(question_mark, "", string)
    string = re.sub(invalid_filename_chars, "-", string)

    return string


def get_videos():
    return videos


def get_video(index):
    return videos[index]


def get_title(index):
    return videos[index][TITLE_INDEX]


def add_video(index, title, is_selected=True):
    videos[index] = (is_selected, title)


def is_video_selected(index):
    return videos[index][IS_SELECTED_INDEX]


def set_video_selected(index, is_selected):
    videos[index] = (is_selected, get_title(index))


def get_selected_videos():
    selected_videos = {}

    for index in range(1, len(get_videos()) + 1):
        if is_video_selected(index):
            selected_videos[index] = get_video(index)

    return selected_videos


def get_playlist_info(playlist_url):
    command = f"\"{YOUTUBEDL_PATH}\" --flat-playlist -e -J --get-filename {FILENAME_ARGS} -o %(title)s {playlist_url}"

    raw_playlist = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode("unicode_escape")
    raw_playlist = raw_playlist.splitlines()

    playlist = []
    if len(raw_playlist) > 0:
        json_info = raw_playlist.pop(len(raw_playlist) - 1)

        for i in range(1, len(raw_playlist), 2):
            playlist.append(raw_playlist[i])

        try:
            json_dump = json.loads(json_info)
            playlist_title = json_dump['title']
        except json.decoder.JSONDecodeError:
            print("[Error] Invalid json obtained from playlist page.")
            playlist_title = ""
    else:
        playlist = []
        playlist_title = ""
        print("[Error] Playlist is empty")

    return playlist, playlist_title


def rip_selected_videos(url, artist, album):
    print(f"[Log] Url: {url}\n"
          f"[Log] Artist: {artist}\n"
          f"[Log] Album: {album}")

    playlist_items = "--playlist-items "
    video_list = get_selected_videos()

    artist = convert_invalid_characters(artist)
    album = convert_invalid_characters(album)

    print("[Log] Pending Playlist")
    for item in video_list.items():
        print(f"[Log] {item[0]}. {item[1][1]}")
        playlist_items += f"{item[0]},"

    playlist_items = playlist_items[:-1]

    download_dir = f"{DOWNLOAD_DIR}\\{artist}\\{album}\\"
    output_template = f"-o \"{download_dir}%(title)s.%(ext)s\""
    command = f"\"{YOUTUBEDL_PATH}\" {playlist_items} {AUDIO_ARGS} {FILENAME_ARGS} {output_template} {url}"
    print(f"[Log] {command}")

    subprocess.run(command)

    track_number = 1
    for item in video_list.items():
        filename = f"{item[1][1]}.ogg"
        filepath = os.path.join(download_dir, filename)

        if artist != "":
            # pattern_open_paren = re.compile(r"\s*(\(|\[)")
            # pattern_no_close_paren = re.compile(r"[^()|\])]*")
            # pattern_lyric_video = re.compile(r"(\s*(\(|\[)[^()|\])]*(Video|Audio|Lyric|Official)[^()|\])]*(\)|]))")
            temp_artist = artist.replace(" ", "_")
            pattern_starting_artist = re.compile(fr"(^[^-]*({temp_artist})[^-]*(-_*|_x_))")
            # pattern_starting_artist = re.compile(fr"(^[^-]*({artist})[^-]*(-\s*|\sx\s))")
            match_starting_artist = re.search(pattern_starting_artist, filename)

            if match_starting_artist is not None:
                print(f"[Log] Removing artist name: {filename}")
                # for group in match_starting_artist.groups():
                #     print(group)
                filename = re.sub(match_starting_artist.group(1), "", filename)
                print(f"[Log] After artist name: {filename}")

        pattern_lyric_video = re.compile(r"(_Official|Lyric)(_Audio|_Music|_Lyric)?(_Video|Audio)")
        # pattern_lyric_video = re.compile(r"(\s*(\(|\[)[^(\)|\])]*(Video|Audio|Lyric|Official)[^(\)|\])]*(\)|\]))")
        match_lyric_video = re.search(pattern_lyric_video, filename)

        if match_lyric_video is not None:
            print(f"[Log] Removing lyric video: {filename}")
            filename = filename.replace(match_lyric_video.group(), "")
            print(f"[Log] After lyric removal: {filename}")

        original_filepath = filepath
        filename = filename.replace("_", " ")
        filepath = os.path.join(download_dir, filename)

        try:
            os.replace(original_filepath, filepath)
        except FileNotFoundError:
            print(f"[Error] Could not replace file: {original_filepath}")

        if os.path.isfile(filepath):
            metagen.add_vorbis_metadata(filepath, artist, filename[:-4], album, str(track_number))
        else:
            print(f"[Error] Path is not file: {filepath}")

        track_number += 1

    print("[Log] Ripping complete")
