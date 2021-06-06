from enum import Enum


class VorbisComments(Enum):
    ARTIST = "artist"
    ALBUM = "album"
    # RECORD_LABEL = "organization"
    GENRE = "genre"


class MetadataCache:
    def __init__(self):
        super().__init__()

        self._playlist_url = ""
        self._cached_url = ""
        self._metadata = {}

    def get_playlist_url(self):
        return self._playlist_url

    def set_playlist_url(self, url):
        self._playlist_url = url

    def get_cached_url(self):
        return self._cached_url

    def set_cached_url(self, url):
        self._cached_url = url

    def add_metadata(self, tag, value):
        if value != "":
            self._metadata[tag] = value
        else:
            print(f"[Error] Blank value provided for \"{tag}\"")

    def get_metadata(self):
        return self._metadata

    def get_tag(self, tag):
        if tag in self._metadata:
            return self._metadata[tag]
        else:
            print("[Error] Tag not found")
            return

    def clear_metadata(self):
        self._metadata.clear()
        print("[Log] Metadata cleared")


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

