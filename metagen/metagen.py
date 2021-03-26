import mutagen
from mutagen.oggvorbis import OggVorbis


def add_vorbis_metadata(filepath, artist, title, album, tracknumber):

    try:
        vorbis = OggVorbis(filepath)
        vorbis_tags = vorbis.tags
        vorbis_tags['artist'] = [artist]
        vorbis_tags['title'] = [title]
        vorbis_tags['album'] = [album]
        vorbis_tags['tracknumber'] = [tracknumber]

        vorbis.save()
        print(f"[Log] Saved metadata for {title}")
    except mutagen.MutagenError as e:
        print(f"[Error] Mutagen could not find file: {filepath} -> {title}")
        print(f"[Mutagen] {e}")





