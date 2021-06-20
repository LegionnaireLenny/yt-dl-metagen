import sys
import cache
import metanums
import ripper
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput


def start_ripping(self):
    if downloader.root.get_cache().get_cached_url() != "":
        ripper.rip_selected_videos(downloader.root.get_cache().get_cached_url(),
                                   downloader.root.get_cache().playlist.get_selected_videos(),
                                   # metadata.get_tag(cache.VorbisComments.ARTIST.value),
                                   # metadata.get_tag(cache.VorbisComments.ALBUM.value),
                                   downloader.root.get_cache().metadata.get_metadata())
        downloader.root.get_cache().set_ripped(True)
        # downloader.root.get_cache().metadata.clear_metadata()
    else:
        print("[Error] No playlist entered")


class UrlInput(BoxLayout):
    def __init__(self):
        super().__init__()

        self.size_hint = (1, None)
        self.size = (self.width, 30)

        self.button = Button(text="Fetch", size_hint=(None, 1), size=(60, self.height))
        self.button.bind(on_press=self.fetch_playlist)
        self.add_widget(self.button)

        self.input = TextInput(hint_text="Enter playlist URL here",
                               multiline=False,
                               write_tab=False)
        self.input.bind(text=self.on_text)
        self.add_widget(self.input)

    def fetch_playlist(self, instance):
        downloader.root.load_playlist()

    def on_text(self, instance, value):
        downloader.root.get_cache().set_playlist_url(value)
        instance.background_color = (0.7, 0.7, 0.7, 0.7)


class MetadataInput(BoxLayout):
    def __init__(self, metadata_tag):
        super().__init__()

        self.size_hint = (1, None)
        self.size = (self.width, 30)
        self.tag = metadata_tag

        self.dropdown = DropDown()
        for comment in metanums.VorbisComments:
            drop_button = Button(text=comment.name, size_hint=(1, None), height=self.height)
            drop_button.bind(on_release=lambda drop_button: self.dropdown.select(drop_button.text))

            self.dropdown.add_widget(drop_button)

        self.button = Button(text=self.tag.name, size_hint=(None, 1), size=(120, self.height))
        self.button.bind(on_release=self.dropdown.open)
        self.add_widget(self.button)

        self.dropdown.bind(on_select=lambda instance, x: setattr(self.button, "text", x))
        self.dropdown.bind(on_select=lambda instance, x: self.set_tag(x))

        self.input = TextInput(text="",
                               hint_text=f"Enter {self.tag.value} here",
                               multiline=False,
                               write_tab=False)
        self.input.bind(text=self.on_text)
        self.add_widget(self.input)

    def set_tag(self, instance):
        self.tag = metanums.VorbisComments[instance]

    def on_text(self, instance, value):
        downloader.root.get_cache().metadata.add_metadata(self.tag.value, value)


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

        downloader.root.get_cache().playlist.add_video(self.index, label_text, self.checkbox.active)

    def on_checkbox_active(self, checkbox, value):
        downloader.root.get_cache().playlist.set_selected(index=self.index, is_selected=value)


class MetadataStack(StackLayout):
    def __init__(self):
        super().__init__()

        self.size_hint = (1, None)


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

        self.cache = cache.Cache()

        self.orientation = "vertical"
        self.add_widget(UrlInput())

        self.video_list = ScrollStack()

        self.add_widget(self.video_list)

        self.load_playlist()

        self.metadata_input = MetadataStack()

        self.metadata_input.add_widget(MetadataInput(metanums.VorbisComments.ARTIST))
        self.metadata_input.add_widget(MetadataInput(metanums.VorbisComments.ALBUM))
        self.metadata_input.add_widget(MetadataInput(metanums.VorbisComments.GENRE))

        self.add_widget(self.metadata_input)

        self.rip_button = Button(text="Rip playlist", size_hint=(1, None), size=(self.width, 50))
        self.rip_button.bind(on_press=start_ripping)
        self.add_widget(self.rip_button)

    def get_cache(self):
        return self.cache

    def load_playlist(self):
        if self.cache.get_playlist_url() != "":
            playlist_url = self.cache.get_playlist_url()
            playlist_info = ripper.get_playlist_info(playlist_url)

            self.video_list.clear_list()
            self.cache = cache.Cache(playlist_url)

            if len(playlist_info[0]) > 0:
                playlist = playlist_info[0]
                self.cache.metadata.add_metadata(metanums.VorbisComments.ALBUM.value, playlist_info[1])

                index = 1
                for item_name in playlist:
                    self.video_list.add_to_list(ItemSelector(index, item_name))
                    index += 1

                self.cache.set_cached_url(playlist_url)
            else:
                print("[Error] Invalid playlist information returned")
        else:
            print("[Error] No URL entered")


class MetagenApp(App):
    def build(self):
        return MainGui()


if __name__ == '__main__':
    # if len(sys.argv) > 1:
    #     url = sys.argv[1]
    # else:
    #     url = ""

    downloader = MetagenApp()
    downloader.run()
