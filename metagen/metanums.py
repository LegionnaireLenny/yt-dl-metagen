from enum import Enum


class VorbisComments(Enum):
    ARTIST = "artist"
    ALBUM = "album"
    # RECORD_LABEL = "organization"
    GENRE = "genre"
    COVER_ART = "metadata_block_picture"
