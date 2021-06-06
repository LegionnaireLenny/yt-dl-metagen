import sys

import ripper
import cache
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput


def start_ripping(self):
    ripper.rip_selected_videos(metadata.get_cached_url(),
                               playlist_dictionary.get_selected_videos(),
                               metadata.get_artist(),
                               metadata.get_album())
    playlist_dictionary.clear()


class UrlInput(BoxLayout):
    def __init__(self):
        super().__init__()

        self.size_hint = (1, None)
        self.size = (self.width, 30)

        self.button = Button(text="Fetch", size_hint=(None, 1), size=(60, self.height))
        self.button.bind(on_press=self.retrieve_playlist)

        self.input = TextInput(text=metadata.get_playlist_url(),
                               hint_text="Enter playlist URL here",
                               multiline=False,
                               write_tab=False)
        self.input.bind(text=self.on_text)

        self.add_widget(self.button)
        self.add_widget(self.input)

    def retrieve_playlist(self, instance):
        metadata.set_cached_url(metadata.get_playlist_url())
        downloader.root.load_playlist()

    def on_text(self, instance, value):
        metadata.set_playlist_url(value)
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

        self.input = TextInput(text=metadata.get_artist(),
                               hint_text="Enter artist name here",
                               multiline=False,
                               write_tab=False)
        self.input.bind(text=self.on_text)
        self.add_widget(self.input)

    def on_text(self, instance, value):
        metadata.set_artist(value)


class AlbumInput(BoxLayout):
    def __init__(self):
        super().__init__()

        self.size_hint = (1, None)
        self.size = (self.width, 30)

        self.input = TextInput(text=metadata.get_album(),
                               hint_text="Enter album name here",
                               multiline=False,
                               write_tab=False)
        self.input.bind(text=self.on_text)
        self.add_widget(self.input)

    def on_text(self, instance, value):
        metadata.set_album(value)


class MetadataInput(BoxLayout):
    def __init__(self):
        super().__init__()

        self.size_hint = (1, None)
        self.size = (self.width, 30)

        self.input = TextInput(text=metadata.get_album(),
                               hint_text="Enter album name here",
                               multiline=False,
                               write_tab=False)
        self.input.bind(text=self.on_text)
        self.add_widget(self.input)

    def on_text(self, instance, value):
        metadata.set_album(value)


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

        playlist_dictionary.add_video(self.index, label_text, self.checkbox.active)

    def on_checkbox_active(self, checkbox, value):
        playlist_dictionary.set_selected(index=self.index, is_selected=value)


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
        if metadata.get_playlist_url() != "":
            self.video_list.clear_list()
            playlist_dictionary.clear()

            playlist_info = ripper.get_playlist_info(metadata.get_playlist_url())

            if len(playlist_info[0]) > 0:
                playlist = playlist_info[0]
                metadata.set_album(playlist_info[1])

                index = 1
                for item_name in playlist:
                    self.video_list.add_to_list(ItemSelector(index, item_name))
                    index += 1

                # metadata.set_cached_url(metadata.get_playlist_url())
            else:
                print("[Error] Invalid playlist information returned")
        else:
            print("[Warning] No playlist entered")


class MetagenApp(App):
    def build(self):
        return MainGui()


if __name__ == '__main__':
    playlist_dictionary = cache.PlaylistDictionary()
    metadata = cache.MetadataCache()

    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = ""

    metadata.set_playlist_url(url)

    downloader = MetagenApp()
    downloader.run()
