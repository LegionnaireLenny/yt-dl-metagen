from kivy.properties import colormap
from kivy.utils import rgba

# https://www.w3.org/TR/SVG11/types.html#ColorKeywords
border_themes = {
    "border_none": (0, 0, 0, 0),
    "border_thin": (4, 4, 4, 4),
    "border_medium": (10, 10, 10, 10),
    "border_thick": (16, 16, 16, 16)
}

color_scheme = {
    # URL Fetch button
    "url_button_background": colormap["beige"],
    "url_button_border": border_themes["border_medium"],
    "url_button_text": colormap["beige"],
    # Metadata label button
    "metadata_button_background": colormap["beige"],
    "metadata_button_border": border_themes["border_medium"],
    "metadata_button_text": colormap["beige"],
    # Cover art button
    "cover_art_button_background": colormap["beige"],
    "cover_art_button_border": border_themes["border_medium"],
    "cover_art_button_text": colormap["beige"],
    # Rip playlist button
    "rip_button_background": colormap["beige"],
    "rip_button_border": border_themes["border_medium"],
    "rip_button_text": colormap["beige"],
    # URL text input
    "url_text_background": colormap["beige"],
    "url_text_border": border_themes["border_medium"],
    "url_text_text": colormap["saddlebrown"],
    "url_text_hint_text": colormap["darkgoldenrod"],
    "url_text_selection": rgba(244, 164, 96, 100), #sandybrown
    # Metadata text input
    "metadata_text_background": colormap["beige"],
    "metadata_text_border": border_themes["border_medium"],
    "metadata_text_text": colormap["saddlebrown"],
    "metadata_text_hint_text": colormap["darkgoldenrod"],
    "metadata_text_selection": rgba(222, 184, 135, 130), #burlywood
    # Playlist item checkbox
    "playlist_item_checkbox": colormap["green"],
    # Playlist tracknumber text input
    "playlist_item_tracknumber_background": colormap["beige"],
    "playlist_item_tracknumber_border": border_themes["border_medium"],
    "playlist_item_tracknumber_text": colormap["saddlebrown"],
    "playlist_item_tracknumber_hint_text": colormap["darkgoldenrod"],
    "playlist_item_tracknumber_selection": rgba(222, 184, 135, 130), #burlywood
    # Playlist title text input
    "playlist_item_title_background": colormap["beige"],
    "playlist_item_title_border": border_themes["border_medium"],
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
