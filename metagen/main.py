from typing import List

from kivy.app import App
from kivy.core.window import Window
from kivy.effects.scroll import ScrollEffect
# noinspection PyProtectedMember
from kivy.properties import colormap
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.utils import rgba

import metanums
import ripper

# https://www.w3.org/TR/SVG11/types.html#ColorKeywords
scheme_data = {
    "border_none": (0, 0, 0, 0),
    "border_thin": (4, 4, 4, 4),
    "border_medium": (10, 10, 10, 10),
    "border_thick": (16, 16, 16, 16)
}
color_scheme = {
    # URL Fetch button
    "url_button_background": colormap["beige"],
    "url_button_border": scheme_data["border_medium"],
    "url_button_text": colormap["beige"],
    # Metadata label button
    "metadata_button_background": colormap["beige"],
    "metadata_button_border": scheme_data["border_medium"],
    "metadata_button_text": colormap["beige"],
    # Covert art button
    "cover_art_button_background": colormap["beige"],
    "cover_art_button_border": scheme_data["border_medium"],
    "cover_art_button_text": colormap["beige"],
    # Rip playlist button
    "rip_button_background": colormap["beige"],
    "rip_button_border": scheme_data["border_medium"],
    "rip_button_text": colormap["beige"],
    # URL text input
    "url_text_background": colormap["beige"],
    "url_text_border": scheme_data["border_medium"],
    "url_text_text": colormap["saddlebrown"],
    "url_text_hint_text": colormap["darkgoldenrod"],
    "url_text_selection": rgba(244, 164, 96, 100), #sandybrown
    # Metadata text input
    "metadata_text_background": colormap["beige"],
    "metadata_text_border": scheme_data["border_medium"],
    "metadata_text_text": colormap["saddlebrown"],
    "metadata_text_hint_text": colormap["darkgoldenrod"],
    "metadata_text_selection": rgba(222, 184, 135, 130), #burlywood
    # Playlist item checkbox
    "playlist_item_checkbox": colormap["green"],
    # Playlist tracknumber text input
    "playlist_item_tracknumber_background": colormap["beige"],
    "playlist_item_tracknumber_border": scheme_data["border_medium"],
    "playlist_item_tracknumber_text": colormap["saddlebrown"],
    "playlist_item_tracknumber_hint_text": colormap["darkgoldenrod"],
    "playlist_item_tracknumber_selection": rgba(222, 184, 135, 130), #burlywood
    # Playlist title text input
    "playlist_item_title_background": colormap["beige"],
    "playlist_item_title_border": scheme_data["border_medium"],
    "playlist_item_title_text": colormap["saddlebrown"],
    "playlist_item_title_hint_text": colormap["darkgoldenrod"],
    "playlist_item_title_selection": rgba(222, 184, 135, 130), #burlywood
    # Playlist scrollbar
    "scrollbar_active": colormap["forestgreen"],
    "scrollbar_inactive": colormap["green"],
    # Window colors
    "window_background": colormap["peachpuff"],
    "window_title_bar": colormap["peachpuff"],
}
testing_url = ""

class UrlInput(BoxLayout):
    def __init__(self, url=""):
        super().__init__()
        self.size_hint_y = None
        self.height = 30
        self.spacing = 4

        self.button = Button(text="Fetch",
                             size_hint_x=None,
                             width=60,
                             background_color=color_scheme["url_button_background"],
                             border=color_scheme["url_button_border"],
                             color=color_scheme["url_button_text"],
                             on_release=self.fetch_playlist)
        self.add_widget(self.button)

        self.input = TextInput(text=url,
                               hint_text="Enter playlist URL here",
                               background_color=color_scheme["url_text_background"],
                               border=color_scheme["url_text_border"],
                               foreground_color=color_scheme["url_text_text"],
                               hint_text_color=color_scheme["url_text_hint_text"],
                               selection_color=color_scheme["url_text_selection"],
                               multiline=False,
                               write_tab=False,
                               on_text_validate=self.fetch_playlist)
        self.add_widget(self.input)

    def get_url(self) -> str:
        return self.input.text

    # noinspection PyUnusedLocal
    def fetch_playlist(self, instance):
        downloader.root.load_playlist(self.input.text)


class MetadataInput(BoxLayout):
    def __init__(self, metadata_tag):
        super().__init__()
        self.size_hint_y = None
        self.height = 30
        self.spacing = 4
        self.tag = metadata_tag

        self.button = Button(text=self.tag.name,
                             size_hint_x=None,
                             width=80,
                             background_color=color_scheme["metadata_button_background"],
                             border=color_scheme["metadata_button_border"],
                             color=color_scheme["metadata_button_text"])
        self.button.background_down = self.button.background_normal
        self.add_widget(self.button)

        self.input = TextInput(text="",
                               hint_text=f"Enter {self.tag.value} here",
                               background_color=color_scheme["metadata_text_background"],
                               border=color_scheme["metadata_text_border"],
                               foreground_color=color_scheme["metadata_text_text"],
                               hint_text_color=color_scheme["metadata_text_hint_text"],
                               selection_color=color_scheme["metadata_text_selection"],
                               multiline=False,
                               write_tab=False)
        self.add_widget(self.input)

    def get_tag_label(self) -> metanums.VorbisComments:
        return self.tag

    def set_tag_label(self, instance):
        self.tag = metanums.VorbisComments[instance]

    def get_tag(self) -> str:
        return self.input.text

    def set_tag(self, tag):
        self.input.text = tag


class PlaylistItem(BoxLayout):
    def __init__(self, index, label_text):
        super().__init__()
        self.text_left_padding = (4,1,1,0)
        self.text_center_padding = (0,1,0,0)
        self.size_hint_y = None
        self.height = 20
        self.spacing = 4

        self.checkbox = CheckBox(active=True,
                                 size_hint_x=None,
                                 width=40,
                                 color= color_scheme["playlist_item_checkbox"])
        self.add_widget(self.checkbox)

        self.tracknumber = TextInput(text=f"{index}",
                                     hint_text=f"{index}",
                                     input_filter="int",
                                     size_hint_x=None,
                                     width=40,
                                     halign="center",
                                     padding=self.text_center_padding,
                                     background_color=color_scheme["playlist_item_tracknumber_background"],
                                     border=color_scheme["playlist_item_tracknumber_border"],
                                     foreground_color=color_scheme["playlist_item_tracknumber_text"],
                                     hint_text_color=color_scheme["playlist_item_tracknumber_hint_text"],
                                     selection_color=color_scheme["playlist_item_tracknumber_selection"],
                                     multiline=False,
                                     write_tab=False)
        self.add_widget(self.tracknumber)

        self.title = TextInput(text=f"{label_text}",
                               hint_text=f"{label_text}",
                               padding=self.text_left_padding,
                               background_color=color_scheme["playlist_item_title_background"],
                               border=color_scheme["playlist_item_title_border"],
                               foreground_color=color_scheme["playlist_item_title_text"],
                               hint_text_color=color_scheme["playlist_item_title_hint_text"],
                               selection_color=color_scheme["playlist_item_title_selection"],
                               multiline=False,
                               write_tab=False)
        self.add_widget(self.title)

    def is_selected(self) -> bool:
        return self.checkbox.active

    def get_tracknumber(self) -> str:
        if self.tracknumber.text != "":
            return self.tracknumber.text
        else:
            return self.tracknumber.hint_text

    def get_playlist_index(self) -> str:
        return self.tracknumber.hint_text

    def get_title(self) -> str:
        if self.title.text != "":
            return self.title.text
        else:
            return self.title.hint_text


class ScrollStack(ScrollView):
    def __init__(self):
        super().__init__()
        self.scroll_wheel_distance = 40
        self.smooth_scroll_end = 5
        self.effect_cls = ScrollEffect
        self.bar_width = 3
        self.bar_margin = -1
        self.bar_color = color_scheme["scrollbar_active"]
        self.bar_inactive_color = color_scheme["scrollbar_inactive"]

        self.stack = StackLayout(size_hint_y=None, spacing= 2)
        self.stack.bind(minimum_height=self.stack.setter("height"))
        self.add_widget(self.stack)

    def get_contents(self) -> List[Widget]:
        return self.stack.children

    def add(self, item):
        self.stack.add_widget(item)

    def clear(self):
        self.stack.clear_widgets()


class MainGui(BoxLayout):
    def __init__(self):
        super().__init__()
        Window.clearcolor = colormap["peachpuff"]
        Window.minimum_width = 480
        Window.minimum_height = 320
        self.padding = 5
        self.spacing = 3
        self.orientation = "vertical"

        # TODO Make a custom title bar
        # Window.custom_titlebar = True
        # Window.set_custom_titlebar(CustomTitleBar())

        self.url_input = UrlInput(testing_url)
        self.add_widget(self.url_input)

        self.playlist = ScrollStack()
        self.add_widget(self.playlist)

        self.metadata_box = BoxLayout(orientation="horizontal",
                                      spacing=3,
                                      size_hint_y=None,
                                      height=100)
        self.metadata_input = StackLayout(size_hint=(0.7, None), spacing=4)
        self.metadata_input.add_widget(MetadataInput(metanums.VorbisComments.ARTIST))
        self.metadata_input.add_widget(MetadataInput(metanums.VorbisComments.ALBUM))
        self.metadata_input.add_widget(MetadataInput(metanums.VorbisComments.GENRE))
        self.metadata_box.add_widget(self.metadata_input)

        self.dropdown = DropDown(scroll_wheel_distance=80)
        self.dropdown.bind(on_select=lambda x,y: self.set_cover_art(y))
        self.cover_art_button = Button(text="Cover Art",
                                       size_hint_max=(128,128),
                                       size_hint_min=(64,64),
                                       size_hint=(0.3, None),
                                       background_color=color_scheme["cover_art_button_background"],
                                       border=color_scheme["cover_art_button_border"],
                                       color=color_scheme["cover_art_button_text"],
                                       on_press=self.dropdown.open)
        self.metadata_box.add_widget(self.cover_art_button)
        self.add_widget(self.metadata_box)

        self.rip_button = Button(text="Rip playlist",
                                 size_hint_y=None,
                                 height=50,
                                 background_color=color_scheme["rip_button_background"],
                                 border=color_scheme["rip_button_border"],
                                 color=color_scheme["rip_button_text"])
        self.rip_button.bind(on_press=self.rip_playlist)
        self.add_widget(self.rip_button)

    def set_cover_art(self, thumbnail):
        self.cover_art_button.background_normal = thumbnail
        self.cover_art_button.background_down = thumbnail
        self.cover_art_button.text = ""

    def populate_dropdown(self, thumbnails):
        for thumbnail in thumbnails:
            button = Button(size_hint_max=(128, 128),
                            size_hint_min=(64, 64),
                            size_hint=(0.3, None),
                            background_normal=thumbnail,
                            background_down=thumbnail)
            button.bind(on_release=lambda btn: self.dropdown.select(btn.background_normal))
            self.dropdown.add_widget(button)

    def load_playlist(self, url):
        try:
            if url != "":
                self.playlist.clear()
                playlist_info = ripper.get_playlist_info(url)

                if len(playlist_info[0]) > 0:
                    playlist = playlist_info[0]
                    playlist_title = playlist_info[1]
                    channel_name = playlist_info[2]
                    for child in self.metadata_input.children:
                        if child.get_tag_label() == metanums.VorbisComments.ALBUM:
                            child.set_tag(playlist_title)
                        if child.get_tag_label() == metanums.VorbisComments.ARTIST:
                            child.set_tag(channel_name)

                    index = 1
                    for title in playlist:
                        self.playlist.add(PlaylistItem(index, title))
                        index += 1

                    self.populate_dropdown(playlist_info[3])
                else:
                    print("[Error] Invalid playlist information returned")
            else:
                print("[Error] No URL entered")
        except Exception as e:
            print(f"[Error] Error loading playlist information.\n{e}")

    # noinspection PyUnusedLocal
    def rip_playlist(self, instance):
        url = self.url_input.get_url()

        if url != "":
            selected_videos = {}
            for item in self.playlist.get_contents():
                if item.is_selected():
                    tracknumber = item.get_tracknumber()
                    playlist_index = item.get_playlist_index()
                    title = item.get_title()
                    selected_videos[playlist_index] = (tracknumber, title)

            metadata = {}
            for child in self.metadata_input.children:
                for comment in metanums.VorbisComments:
                    if child.get_tag_label() == comment:
                        metadata[comment.value] = child.get_tag()

            if "thumbnails" in self.cover_art_button.background_normal:
                metadata[metanums.VorbisComments.COVER_ART.value] = self.cover_art_button.background_normal
            ripper.rip_selected_videos(url, selected_videos, metadata)
        else:
            print("[Error] No playlist entered")


class MetagenApp(App):
    def build(self):
        return MainGui()


if __name__ == '__main__':
    downloader = MetagenApp()
    downloader.run()
