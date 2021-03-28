# About
*yt-dl-metagen* is a simple GUI wrapper for downloading and extracting audio from Youtube playlists using youtube-dl, with
the option of automatically filling in additional metadata for the downloaded files. Currently, only the Ogg Vorbis (.ogg)
format is supported. Other formats can be specified by manually editing *ripper.py* before running the program. 

# Setting up yt-dl-metagen

1. Install Python 3.6 or later
   1. https://www.python.org/

1. Install the mutagen library
   1. https://github.com/quodlibet/mutagen
   1. https://mutagen.readthedocs.io/en/latest/
    
1. Download youtube-dl.exe
   1. https://github.com/ytdl-org/youtube-dl
   1. You need the executable not the python files
    
1. Download the Windows executables for ffmpeg
   1. https://ffmpeg.org/download.html
    
1. Create a _bin_ folder in the project root folder and place _youtube-dl.exe_, _ffmpeg.exe_, and _ffprobe.exe_ in the _bin_ folder 
<pre>
Example directory structure

yt-dl-metagen
|
├── bin
│   ├── ffmpeg.exe
│   ├── ffprobe.exe
│   └── youtube-dl.exe
└── metagen
    ├── main.py
    ├── metagen.py
    └── ripper.py
</pre>

# Running yt-dl-metagen
1. Enter the URL of a Youtube playlist

1. Press "Fetch"

1. Select the videos to download

1. (Optional) Enter Artist name or Album title
   
1. Press "Rip playlist"
   1. The audio files will be downloaded to the _Ripped Audio\\\<artist>\\\<album>_ folder
   1. Audio files are automatically numbered consecutively based on their position in the playlist
   
# Notes

- Audio files are extracted to the "Ripped Audio" folder in the directory above main.py.
  - Default: _yt-dl-metagen\\Ripped Audio_
- If you enter an artist/album name, it'll extract the audio files to "Ripped Audio\\\<artist name>\\\<album name>
- It tries to clean up the filenames a bit by removing the artist name (if provided) and stuff like (Official Video)
- It will save the filename, artist, album, and tracknumber to the metadata
- Tracks are numbered consecutively based on their position in the playlist. e.g. if you only download videos 1,2,4,6 the tracks will be numbered 1,2,3,4 respectively

# Known Issues

- The program must be closed by closing the Python window, pressing Ctrl+C on CMD/Powershell, or pressing the exit button.
- Regex for removing Official Video, et al. needs improving