import os
import json
import metanums
import metagen
import subprocess
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURR_DIR = os.path.dirname(os.path.realpath(__file__))

YOUTUBEDL_PATH = os.path.join(CURR_DIR, "..\\bin\\youtube-dl.exe")
FFMPEG_PATH = os.path.join(CURR_DIR, "..\\bin\\ffmpeg.exe")
FFPROBE_PATH = os.path.join(CURR_DIR, "..\\bin\\ffprobe.exe")

DOWNLOAD_DIR = os.path.join(CURR_DIR, "..\\Ripped Audio")
AUDIO_ARGS = "--extract-audio --audio-format vorbis --audio-quality 0"
FILENAME_ARGS = "--restrict-filenames"
OPTIONS = "--abort-on-error"
SIM_ARGS = "-s --get-filename"

CLEAR_ON_FAILED_DOWNLOAD = True
DRY_RUN = False


def convert_invalid_characters(string):
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


def get_playlist_info(playlist_url):
    # command = f"\"{YOUTUBEDL_PATH}\" --flat-playlist -e -J --get-filename {FILENAME_ARGS} -o %(title)s {playlist_url}"
    command = f"\"{YOUTUBEDL_PATH}\" --flat-playlist -e -J --get-filename -o %(title)s {playlist_url}"

    raw_playlist = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode("unicode_escape")
    raw_playlist = raw_playlist.splitlines()

    playlist = []
    playlist_title = ""
    if len(raw_playlist) > 0:
        json_info = raw_playlist.pop(len(raw_playlist) - 1)

        for i in range(1, len(raw_playlist), 2):
            playlist.append(raw_playlist[i])

        try:
            json_dump = json.loads(json_info)
            playlist_title = json_dump['title']
        except json.decoder.JSONDecodeError:
            print("[Error] Invalid json obtained from playlist page.")
    else:
        print("[Error] Playlist is empty")

    return playlist, playlist_title


def rip_selected_videos(url, video_list, vorbis_comments):
    """

    :param url: (string) Valid URL
    :param video_list: (dict) Playlist object from cache.py
        key: (int) Video's position in playlist
        value: (boolean, string)
          boolean - indicates whether an item has been selected by user
          string - title of the item selected
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
        print(f"[Log] {item[0]}. {item[1][1]}")
        playlist_items += f"{item[0]},"

    playlist_items = playlist_items[:-1]

    download_dir = f"{DOWNLOAD_DIR}\\"
    if artist != "":
        download_dir += f"{artist}\\"
    if album != "":
        download_dir += f"{album}\\"

    output_template = f"-o \"{download_dir}%(playlist_index)s.%(ext)s\""
    if DRY_RUN:
        command = f"\"{YOUTUBEDL_PATH}\" {playlist_items} {AUDIO_ARGS} {SIM_ARGS} {OPTIONS} {output_template} {url}"
    else:
        command = f"\"{YOUTUBEDL_PATH}\" {playlist_items} {AUDIO_ARGS} {OPTIONS} {output_template} {url}"
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
    track_number = 1
    for item in video_list.items():
        indexed_filename = f"{str(item[0]).zfill(filename_padding)}.ogg"
        indexed_filepath = os.path.join(download_dir, indexed_filename)
        filename = convert_invalid_characters(f"{item[1][1]}.ogg")
        filepath = os.path.join(download_dir, filename)

        try:
            os.replace(indexed_filepath, filepath)
        except FileNotFoundError:
            print(f"[Error] Could not replace file: {indexed_filepath}")

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

        original_filepath = filepath
        # filename = filename.replace("_", " ")
        # print(f"[Log] After removing underscores: {filename}")
        filepath = os.path.join(download_dir, filename)

        try:
            os.replace(original_filepath, filepath)
        except FileNotFoundError:
            print(f"[Error] Could not replace file: {original_filepath}")

        if os.path.isfile(filepath):
            metagen.add_vorbis_metadata(filepath, filename[:-4], str(track_number), vorbis_comments)
        else:
            print(f"[Error] Path is not file: {filepath}")

        track_number += 1
    print("[Log] Ripping complete")
