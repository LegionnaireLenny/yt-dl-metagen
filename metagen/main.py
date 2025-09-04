import metanums
import ripper
from kivy.app import App
from kivy.effects.scroll import ScrollEffect
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput


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
        self.add_widget(self.input)

    def fetch_playlist(self, instance):
        downloader.root.load_playlist(self.input.text)


class MetadataInput(BoxLayout):
    def __init__(self, metadata_tag):
        """
        :param metadata_tag (enum):
        """
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
        self.add_widget(self.input)

    def set_tag(self, instance):
        self.tag = metanums.VorbisComments[instance]


class PlaylistItem(BoxLayout):
    def __init__(self, index, label_text):
        super().__init__()

        self.size_hint = (1, None)
        self.size = (self.width, 35)

        self.checkbox = CheckBox(active=True, size_hint=(None, 1), size=(60, self.height))
        self.add_widget(self.checkbox)

        self.index_input = TextInput(text=f"{index}",
                               hint_text=f"{index}",
                               input_filter="int",
                               size_hint=(0, 1),
                               size=(45, self.height),
                               multiline=False)
        self.add_widget(self.index_input)

        # self.label = Label(text=label_text, size_hint=(0.9, 1), text_size=self.size, halign="left")
        self.label = Label(text=f"{label_text}")
        self.add_widget(self.label)


class ScrollStack(ScrollView):
    def __init__(self):
        super().__init__()
        self.scroll_wheel_distance = 40
        self.smooth_scroll_end = 5
        self.effect_cls = ScrollEffect

        self.stack = StackLayout(size_hint=(1, None))
        self.stack.bind(minimum_height=self.stack.setter("height"))
        self.add_widget(self.stack)

    def add(self, item):
        self.stack.add_widget(item)

    def clear(self):
        self.stack.clear_widgets()


class MainGui(BoxLayout):
    def __init__(self):
        super().__init__()

        self.orientation = "vertical"

        self.url_input = UrlInput()
        self.add_widget(self.url_input)

        self.video_list = ScrollStack()
        self.add_widget(self.video_list)

        self.metadata_input = StackLayout(size_hint=(1, None))
        self.metadata_input.add_widget(MetadataInput(metanums.VorbisComments.ARTIST))
        self.metadata_input.add_widget(MetadataInput(metanums.VorbisComments.ALBUM))
        self.metadata_input.add_widget(MetadataInput(metanums.VorbisComments.GENRE))
        self.add_widget(self.metadata_input)

        self.rip_button = Button(text="Rip playlist", size_hint=(1, None), size=(self.width, 50))
        self.rip_button.bind(on_press=self.rip_playlist)
        self.add_widget(self.rip_button)


    def load_playlist(self, url):
        if url != "":
            self.video_list.clear()
            playlist_info = ripper.get_playlist_info(url)

            if len(playlist_info[0]) > 0:
                playlist = playlist_info[0]
                playlist_title = playlist_info[1]
                for child in self.metadata_input.children:
                    if child.tag == metanums.VorbisComments.ALBUM:
                        child.input.text = playlist_title

                index = 1
                for item_name in playlist:
                    self.video_list.add(PlaylistItem(index, item_name))
                    index += 1
            else:
                print("[Error] Invalid playlist information returned")
        else:
            print("[Error] No URL entered")

    def rip_playlist(self, instance):
        url = self.url_input.input.text

        if url != "":
            selected_videos = {}
            for item in self.video_list.stack.children:
                if item.checkbox.active:
                    index = item.index_input.text
                    fallback_index = item.index_input.hint_text
                    selected_videos[index if index != "" else fallback_index ] = item.label.text

            metadata = {}
            for child in self.metadata_input.children:
                for comment in metanums.VorbisComments:
                    if child.tag == comment:
                        metadata[comment.value] = child.input.text

            ripper.rip_selected_videos(url, selected_videos, metadata)
        else:
            print("[Error] No playlist entered")


class MetagenApp(App):
    def build(self):
        return MainGui()


if __name__ == '__main__':
    downloader = MetagenApp()
    downloader.run()
