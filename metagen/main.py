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
    # _playlist_url = "https://www.youtube.com/playlist?list=OLAK5uy_k0OLmSoKa-MJ5-K5rv6Yxn4QFnPO3hhuA"

_artist = ""
_album = ""
_exit = False


def start_ripping(self):
    return ripper.rip_selected_videos(_playlist_url, _artist, _album)


def get_playlist_url():
    global _playlist_url
    return _playlist_url


def set_url(url):
    global _playlist_url
    _playlist_url = url


def get_artist():
    global _artist
    return _artist


def set_artist(artist):
    global _artist
    _artist = artist


def get_album():
    global _album
    return _album


def set_album(album):
    global _album
    _album = album


def get_exit_status():
    global _exit
    return _exit


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

        self.input = TextInput(text=get_playlist_url(), hint_text="Enter playlist URL here", multiline=False, write_tab=False)
        self.input.bind(text=self.on_text)

        self.add_widget(self.button)
        self.add_widget(self.input)

    def retrieve_playlist(self, instance):
        scraper.stop()

    def on_text(self, instance, value):
        set_url(value)
        instance.background_color = (0.7, 0.7, 0.7, 0.7)


class ArtistInput(BoxLayout):
    def __init__(self):
        super().__init__()

        self.size_hint = (1, None)
        self.size = (self.width, 30)

        self.input = TextInput(text=get_artist(), hint_text="Enter artist name here", multiline=False, write_tab=False)
        self.input.bind(text=self.on_text)
        self.add_widget(self.input)

    def on_text(self, instance, value):
        set_artist(value)


class AlbumInput(BoxLayout):
    def __init__(self):
        super().__init__()

        self.size_hint = (1, None)
        self.size = (self.width, 30)

        self.input = TextInput(text=get_album(), hint_text="Enter album name here", multiline=False, write_tab=False)
        self.input.bind(text=self.on_text)
        self.add_widget(self.input)

    def on_text(self, instance, value):
        set_album(value)


class VideoListItem(BoxLayout):
    def __init__(self, index, label_text):
        super().__init__()

        self.index = index
        self.size_hint = (1, None)
        self.size = (self.width, 35)

        self.checkbox = CheckBox(active=True, size_hint=(None, 1), size=(60, self.height))
        self.checkbox.bind(active=self.on_checkbox_active)

        ripper.add_video(self.index, label_text, self.checkbox.active)

        self.label = Label(text=label_text.replace("_", " "))
        # self.label = Label(text=label_text, size_hint=(0.9, 1), text_size=self.size, halign="left")

        self.add_widget(self.checkbox)
        self.add_widget(self.label)

    def on_checkbox_active(self, checkbox, value):
        ripper.set_video_selected(index=self.index, is_selected=value)


class VideoListApp(App):
    def build(self):
        main_box = BoxLayout(orientation="vertical")
        main_box.add_widget(UrlInput())

        if get_playlist_url() != "":
            playlist_info = ripper.get_playlist_info(get_playlist_url())

            if len(playlist_info[0]) > 0:
                list_scroll = ScrollView()
                list_stack = StackLayout()

                playlist = playlist_info[0]
                set_album(playlist_info[1])

                index = 1
                for item_name in playlist:
                    list_stack.add_widget(VideoListItem(index, item_name))
                    index += 1

                list_scroll.add_widget(list_stack)
                main_box.add_widget(list_scroll)

                artist_input = ArtistInput()
                album_input = AlbumInput()

                main_box.add_widget(artist_input)
                main_box.add_widget(album_input)

                rip_button = Button(text="Rip playlist", size_hint=(1, None), size=(main_box.width, 50))
                rip_button.bind(on_press=start_ripping)

                exit_button = Button(text="Exit", size_hint=(0.2, None), size=(main_box.width, 30))
                exit_button.bind(on_press=self.exit_program)

                main_box.add_widget(rip_button)
                main_box.add_widget(exit_button)
            else:
                print("[Error] Invalid playlist information returned")

        return main_box

    def exit_program(self, button):
        set_exit_status(True)
        scraper.stop()


if __name__ == '__main__':
    while not _exit:
        scraper = VideoListApp()
        scraper.run()
