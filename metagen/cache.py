from enum import Enum


class VorbisComments(Enum):
    ARTIST = "artist"
    ALBUM = "album"
    RECORD_LABEL = "organization"
    GENRE = "genre"


class MetadataCache:
    def __init__(self):
        super().__init__()

        self._playlist_url = ""
        self._cached_url = ""
        self._artist = ""
        self._album = ""

    def get_playlist_url(self):
        return self._playlist_url

    def set_playlist_url(self, url):
        self._playlist_url = url

    def get_cached_url(self):
        return self._cached_url

    def set_cached_url(self, url):
        self._cached_url = url

    def get_album(self):
        return self._album

    def set_album(self, album):
        self._album = album

    def get_artist(self):
        return self._artist

    def set_artist(self, artist):
        self._artist = artist


class PlaylistDictionary(dict):
    def __init__(self):
        super().__init__()

        self.IS_SELECTED_INDEX = 0
        self.TITLE_INDEX = 1

    def add_video(self, index, title, is_selected=True):
        self[index] = (is_selected, title)

    def get_title(self, index):
        return self[index][self.TITLE_INDEX]

    def is_selected(self, index):
        return self[index][self.IS_SELECTED_INDEX]

    def set_selected(self, index, is_selected):
        self[index] = (is_selected, self.get_title(index))

    def get_selected_videos(self):
        selected_videos = {}

        for index in range(1, len(self) + 1):
            if self.is_selected(index):
                selected_videos[index] = self[index]

        return selected_videos

    def clear(self):
        super().clear()
        print("[Log] Video list cleared")

