import mutagen
from mutagen.oggvorbis import OggVorbis


def add_vorbis_metadata(filepath, title, tracknumber, vorbis_comments):

    try:
        vorbis = OggVorbis(filepath)
        vorbis_tags = vorbis.tags
        vorbis_tags['title'] = [title]
        vorbis_tags['tracknumber'] = [tracknumber]

        for comment in vorbis_comments:
            vorbis_tags[comment] = [vorbis_comments[comment]]

        vorbis.save()
        print(f"[Log] Saved metadata for {title}")
    except mutagen.MutagenError as e:
        print(f"[Error] Mutagen could not find file: {filepath} -> {title}")
        print(f"[Mutagen] {e}")





