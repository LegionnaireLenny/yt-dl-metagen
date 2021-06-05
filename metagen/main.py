import sys

import ripper
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput


if len(sys.argv) > 1:
    _playlist_url = sys.argv[1]
else:
    _playlist_url = ""

_cached_url = ""
_artist = ""
_album = ""
_exit = False


def start_ripping(self):
    ripper.rip_selected_videos(_cached_url, _artist, _album)


def set_cached_url(url):
    global _cached_url
    _cached_url = url


def set_playlist_url(url):
    global _playlist_url
    _playlist_url = url


def set_artist(artist):
    global _artist
    _artist = artist


def set_album(album):
    global _album
    _album = album


def set_exit_status(exit_status):
    global _exit
    _exit = exit_status


class UrlInput(BoxLayout):
    def __init__(self):
        super().__init__()

        self.size_hint = (1, None)
        self.size = (self.width, 30)

        self.button = Button(text="Fetch", size_hint=(None, 1), size=(60, self.height))
        self.button.bind(on_press=self.retrieve_playlist)

        self.input = TextInput(text=_playlist_url, hint_text="Enter playlist URL here", multiline=False, write_tab=False)
        self.input.bind(text=self.on_text)

        self.add_widget(self.button)
        self.add_widget(self.input)

    def retrieve_playlist(self, instance):
        set_cached_url(_playlist_url)
        downloader.root.load_playlist()

    def on_text(self, instance, value):
        set_playlist_url(value)
        instance.background_color = (0.7, 0.7, 0.7, 0.7)

# TODO
# Convert these two to generic MetadataInput
# MetadataInput needs dropdown box with supported metadata fields
# convert set_x() to generic set_metadata() input that takes enum metadata
# and sets based on enum received


class ArtistInput(BoxLayout):
    def __init__(self):
        super().__init__()

        self.size_hint = (1, None)
        self.size = (self.width, 30)

        self.input = TextInput(text=_artist, hint_text="Enter artist name here", multiline=False, write_tab=False)
        self.input.bind(text=self.on_text)
        self.add_widget(self.input)

    def on_text(self, instance, value):
        set_artist(value)


class AlbumInput(BoxLayout):
    def __init__(self):
        super().__init__()

        self.size_hint = (1, None)
        self.size = (self.width, 30)

        self.input = TextInput(text=_album, hint_text="Enter album name here", multiline=False, write_tab=False)
        self.input.bind(text=self.on_text)
        self.add_widget(self.input)

    def on_text(self, instance, value):
        set_album(value)


class ItemSelector(BoxLayout):
    def __init__(self, index, label_text):
        super().__init__()

        self.index = index
        self.size_hint = (1, None)
        self.size = (self.width, 35)

        self.checkbox = CheckBox(active=True, size_hint=(None, 1), size=(60, self.height))
        self.checkbox.bind(active=self.on_checkbox_active)
        self.add_widget(self.checkbox)

        self.label = Label(text=f"{self.index}. {label_text.replace('_', ' ')}")
        # self.label = Label(text=label_text, size_hint=(0.9, 1), text_size=self.size, halign="left")
        self.add_widget(self.label)

        ripper.add_video(self.index, label_text, self.checkbox.active)

    def on_checkbox_active(self, checkbox, value):
        ripper.set_video_selected(index=self.index, is_selected=value)


class ScrollStack(ScrollView):
    def __init__(self):
        super().__init__()

        self.list_stack = StackLayout(size_hint=(1, None))
        self.add_widget(self.list_stack)

    def add_to_list(self, item):
        self.list_stack.add_widget(item)

    def clear_list(self):
        self.list_stack.clear_widgets()


class MainGui(BoxLayout):
    def __init__(self):
        super().__init__()

        self.orientation = "vertical"
        self.add_widget(UrlInput())

        self.video_list = ScrollStack()

        self.add_widget(self.video_list)

        self.load_playlist()

        self.add_widget(ArtistInput())
        self.add_widget(AlbumInput())

        self.rip_button = Button(text="Rip playlist", size_hint=(1, None), size=(self.width, 50))
        self.rip_button.bind(on_press=start_ripping)
        self.add_widget(self.rip_button)

    def load_playlist(self):
        if _playlist_url != "":
            self.video_list.clear_list()

            playlist_info = ripper.get_playlist_info(_playlist_url)
            set_cached_url(_playlist_url)

            if len(playlist_info[0]) > 0:
                playlist = playlist_info[0]
                set_album(playlist_info[1])

                index = 1
                for item_name in playlist:
                    self.video_list.add_to_list(ItemSelector(index, item_name))
                    index += 1
            else:
                print("[Error] Invalid playlist information returned")
        else:
            print("[Warning] No playlist entered")


class MetagenApp(App):
    def build(self):
        return MainGui()


if __name__ == '__main__':
    downloader = MetagenApp()
    downloader.run()
