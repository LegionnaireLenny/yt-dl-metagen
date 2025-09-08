import base64

from PIL import Image
from mutagen import MutagenError
# noinspection PyProtectedMember
from mutagen.flac import Picture
from mutagen.oggvorbis import OggVorbis

import metanums


def add_vorbis_metadata(filepath, title, tracknumber, vorbis_comments):
    try:
        vorbis = OggVorbis(filepath)
        vorbis.tags["title"] = [title]
        vorbis.tags["tracknumber"] = [tracknumber]

        for comment in vorbis_comments:
            if comment == metanums.VorbisComments.COVER_ART.value:
                with open(vorbis_comments[comment], "rb") as f:
                    data = f.read()
                    image = Image.open(f)

                picture = Picture()
                picture.data = data
                picture.type = 17
                picture.desc = u"Cover Art"
                picture.mime = u"image/jpeg"
                picture.width = image.width
                picture.height = image.height
                picture.depth = 24

                picture_data = picture.write()
                encoded_data = base64.b64encode(picture_data)
                comment_value = encoded_data.decode("ascii")
                vorbis.tags[comment] = comment_value
            else:
                vorbis.tags[comment] = [vorbis_comments[comment]]

        vorbis.save()
        print(f"[Log] Saved metadata for {title}")
    except MutagenError as e:
        print(f"[Error] Mutagen could not find file: {filepath} -> {title}")
        print(f"[Mutagen] {e}")
