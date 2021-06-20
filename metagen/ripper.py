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

CLEAR_ON_FAILED_DOWNLOAD = True

def convert_invalid_characters(string):
    double_quotes = "\""
    question_mark = r"\?"
    right_quote = "’"
    invalid_filename_chars = "[\\/:*<>|]"

    string = re.sub(double_quotes, "'", string)
    string = re.sub(question_mark, "", string)
    string = re.sub(invalid_filename_chars, "-", string)

    return string


def get_playlist_info(playlist_url):
    command = f"\"{YOUTUBEDL_PATH}\" --flat-playlist -e -J --get-filename {FILENAME_ARGS} -o %(title)s {playlist_url}"

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

    output_template = f"-o \"{download_dir}%(title)s.%(ext)s\""
    command = f"\"{YOUTUBEDL_PATH}\" {playlist_items} {AUDIO_ARGS} {FILENAME_ARGS} {OPTIONS} {output_template} {url}"
    print(f"[Log] {command}")

    result = subprocess.run(command, stderr=subprocess.PIPE).stderr.decode("unicode_escape")

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

    track_number = 1
    for item in video_list.items():
        filename = f"{item[1][1]}.ogg"
        filepath = os.path.join(download_dir, filename)

        print(f"[Log] Original filename: {filename}")
        if artist != "":
            # pattern_open_paren = re.compile(r"\s*(\(|\[)")
            # pattern_no_close_paren = re.compile(r"[^()|\])]*")
            # pattern_lyric_video = re.compile(r"(\s*(\(|\[)[^()|\])]*(Video|Audio|Lyric|Official)[^()|\])]*(\)|]))")
            # pattern_starting_artist = re.compile(fr"(^[^-]*({artist})[^-]*(-\s*|\sx\s))")

            temp_artist = artist.replace(" ", "_")
            pattern_starting_artist = re.compile(fr"(^[^-]*({temp_artist})[^-]*(-_*|_x_))")
            match_starting_artist = re.search(pattern_starting_artist, filename)

            if match_starting_artist is not None:
                # for group in match_starting_artist.groups():
                #     print(group)
                filename = re.sub(match_starting_artist.group(1), "", filename)
                print(f"[Log] After removing artist name: {filename}")

        pattern_lyric_video = re.compile(r"(_Official|_Lyric)(_Audio|_Music|_Lyric)?(_Video|_Audio)")
        # pattern_lyric_video = re.compile(r"(\s*(\(|\[)[^(\)|\])]*(Video|Audio|Lyric|Official)[^(\)|\])]*(\)|\]))")
        match_lyric_video = re.search(pattern_lyric_video, filename)

        if match_lyric_video is not None:
            filename = filename.replace(match_lyric_video.group(), "")
            print(f"[Log] After removing video type: {filename}")

        original_filepath = filepath
        filename = filename.replace("_", " ")
        print(f"[Log] After removing underscores: {filename}")
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
