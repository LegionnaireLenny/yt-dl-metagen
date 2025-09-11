# noinspection PyProtectedMember
from kivy.properties import colormap
from kivy.utils import rgba


def modify_color(color_name: str, intensity: float, alpha: int):
    color = rgba([max(0, min(255, x * 255)) * intensity for x in colormap[color_name][:-1]])
    color[3] = alpha / 255
    return color

def get_tinted_color(color_name: str = None, rgb_value = (1, 0, 0, 1), multiplier: float = 2.88):
    color = colormap[color_name] if color_name is not None else rgb_value
    return rgba([(x * 255) / multiplier for x in color[:-1]])

def set_widget_theme(theme, widget_names, widget_type, background=colormap["red"], border=(4,4,4,4),
                     text=colormap["red"], hint=colormap["red"], selection=colormap["red"]):
    for widget_name in widget_names:
        theme[f"{widget_name}_background"] = background
        theme[f"{widget_name}_border"] = border
        theme[f"{widget_name}_text"] = text

        if widget_type == "text_input":
            theme[f"{widget_name}_hint_text"] = hint
            theme[f"{widget_name}_selection"] = selection


# https://www.w3.org/TR/SVG11/types.html#ColorKeywords
border_themes = {
    "border_none": (0, 0, 0, 0),
    "border_thin": (4, 4, 4, 4),
    "border_medium": (10, 10, 10, 10),
    "border_thick": (16, 16, 16, 16)
}

button_names = [
    "url_button",
    "metadata_button",
    "cover_art_button",
    "download_button"
]

text_input_names = [
    "url_text",
    "metadata_text",
    "playlist_item_tracknumber",
    "playlist_item_title"
]

light_theme = {
    # Playlist item checkbox
    "playlist_item_checkbox": colormap["green"],
    # Playlist scrollbar
    "scrollbar_active": colormap["forestgreen"],
    "scrollbar_inactive": colormap["green"],
    # Window colors
    "window_background": colormap["peachpuff"],
    "title_bar_background": get_tinted_color("beige"),
    # Title bar previous action button
    "title_bar_action_previous_text": colormap["white"],
    # Title bar minimize button
    "title_bar_minimize_button_background": colormap["beige"],
    # Title bar maximize button
    "title_bar_maximize_button_background": colormap["beige"],
    # Title bar close button
    "title_bar_close_button_background": colormap["beige"],
}

set_widget_theme(theme=light_theme,
                 widget_names=button_names,
                 widget_type="button",
                 background=colormap["beige"],
                 border=border_themes["border_medium"],
                 text=colormap["beige"])

set_widget_theme(theme=light_theme,
                 widget_names=text_input_names,
                 widget_type="text_input",
                 background= colormap["beige"],
                 border=border_themes["border_medium"],
                 text=colormap["saddlebrown"],
                 hint=colormap["darkgoldenrod"],
                 selection=modify_color("sandybrown", 1, 100))

dark_theme = {
    # Playlist item checkbox
    "playlist_item_checkbox": colormap["plum"],
    # Playlist scrollbar
    "scrollbar_active": modify_color("mediumslateblue", 0.9 , 255),
    "scrollbar_inactive": modify_color("mediumslateblue", 0.7, 255),
    # Window colors
    "window_background": modify_color("cornflowerblue", 0.4, 255),
    "title_bar_background": get_tinted_color(rgb_value=modify_color("cornflowerblue", 0.8, 255)),
    # Title bar previous action button
    "title_bar_action_previous_text": modify_color("lightsteelblue", 1 , 255),
    # Title bar minimize button
    "title_bar_minimize_button_background": colormap["beige"],
    # Title bar maximize button
    "title_bar_maximize_button_background": colormap["beige"],
    # Title bar close button
    "title_bar_close_button_background": colormap["beige"],
}

set_widget_theme(theme=dark_theme,
                 widget_names=button_names,
                 widget_type="button",
                 background=modify_color("cornflowerblue", 0.8, 255),
                 border=border_themes["border_medium"],
                 text=modify_color("lightsteelblue", 1 , 255))

set_widget_theme(theme=dark_theme,
                 widget_names=text_input_names,
                 widget_type="text_input",
                 background=modify_color("cornflowerblue", 0.6 , 255),
                 border=border_themes["border_medium"],
                 text=modify_color("lightsteelblue", 1 , 255),
                 hint=modify_color("darkslateblue", 0.5, 150),
                 selection=modify_color("skyblue", 1, 100))

ui_theme = light_theme
