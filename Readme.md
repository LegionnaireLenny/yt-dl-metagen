# About
*yt-dl-metagen* is a simple GUI wrapper for downloading and extracting audio from Youtube playlists and individual 
videos using yt-dlp, with the option of automatically filling in additional metadata for the downloaded files. 
Currently, only the Ogg Vorbis (.ogg) format is supported.

Only supported on Windows.

# Setting up yt-dl-metagen

1. Install Python 3.9 or later
   1. https://www.python.org/

2. Install the mutagen library
   1. https://github.com/quodlibet/mutagen
   2. https://mutagen.readthedocs.io/en/latest/
    
3. Install the yt-dlp library
   1. https://github.com/yt-dlp/yt-dlp
    
4. Download the Windows executables for ffmpeg
   1. https://ffmpeg.org/download.html
    
5. Create a _bin_ folder in the project root folder and place _ffmpeg.exe_, and _ffprobe.exe_ in the _bin_ folder 
<pre>
Example directory structure

yt-dl-metagen
|
├── bin
│   ├── ffmpeg.exe
│   └── ffprobe.exe
└── metagen
    ├── downloader.py
    ├── main.py
    ├── metagen.py
    ├── metanums.py
    ├── ui_themes.py
    └── util.py
</pre>

# Running yt-dl-metagen
1. Run _main.py_ using Python, CMD, or Powershell

2. Enter the URL of a Youtube playlist

3. Press "Fetch"

4. Select the videos to download

5. (Optional) Enter metadata for playlist

6. Press "Rip playlist"

# Notes

- Autofill
  - Artist: channel name
  - Album: playlist name
  - Track number: playlist position
  - Track title: video title
- Audio files are extracted to the _Ripped Audio_ folder above main.py.
  - Default: _yt-dl-metagen\\Ripped Audio\\_
  - Subfolders are created if the artist or album are given. e.g. _yt-dl-metagen\\Ripped Audio\\\<artist>\\\<album>_
