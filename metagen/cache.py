class Cache:
    def __init__(self, url=""):
        super().__init__()

        self._playlist_url = url
        self._cached_url = ""
        self._ripped = False

        self.metadata = self.Metadata()
        self.playlist = self.Playlist()

    def get_playlist_url(self):
        return self._playlist_url

    def set_playlist_url(self, url):
        self._playlist_url = url

    def get_cached_url(self):
        return self._cached_url

    def set_cached_url(self, url):
        self._cached_url = url

    def get_ripped(self):
        return self._ripped

    def set_ripped(self, is_ripped):
        self._ripped = is_ripped

    class Metadata(dict):
        """
        Used to store metadata related to a playlist.

        Attributes:
            self.Key (string): the string representation of a metadata tag, e.g. "artist", "album", etc.
            self.Value (string): the  value of a tag

            Example - {["artist","My Favorite Artist"],["album", "My Favorite Album"]}
        """
        def __init__(self):
            super().__init__()

        def add_metadata(self, tag, value):
            if value != "":
                self[tag] = value
            else:
                print(f"[Error] Blank value provided for \"{tag}\"")

        def get_metadata(self):
            return self

        def get_tag(self, tag):
            if tag in self:
                return self[tag]
            else:
                print("[Error] Tag not found")
                return

        def clear(self):
            super().clear()
            print("[Log] Metadata cleared")

    class Playlist(dict):
        """
        Used to track which items in a playlist have been selected

        Attributes:
            self.Key (int): represents an item's position in a playlist
            self.Value (boolean, string):
              boolean - indicates whether an item has been selected by user
              string - title of the item selected

            IS_SELECTED_INDEX (int): position of the boolean in the value tuple
            TITLE_INDEX (int): position of the title in the value tuple
        """
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

