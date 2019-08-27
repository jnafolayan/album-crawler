
import eyed3

from api_calls import get_track_url_youtube
from utils import get_album_data, download_file, download_song
from logging_config import *


album = get_album_data('Glory Sound Prep')
artpath = download_file(album.cover_art_link, album.to_string, album.to_string)
album.cover_art_path = artpath

for track in album:

    track.download_link = get_track_url_youtube(track.search_term)
    track.file_path =\
        download_song(track.download_link, album.to_string, str(track))

    song = eyed3.load(track.file_path)
    logging.info('Setting metadata for track: {}'.format(track.title))
    if song.tag is None:
        song.initTag()

    logging.debug('Setting artist name - "{}"'.format(track.artiste_to_string))
    song.tag.artist = track.artiste_to_string
    logging.debug('Setting album name - "{}"'.format(album.name))
    song.tag.album = album.name
    logging.debug('Setting track title - "{}"'.format(track.title_to_string))
    song.tag.title = track.title_to_string
    logging.debug('Setting album art - f"{}"'
                  .format(track.album.cover_art_path))
    song.tag.images.set(3,
                        open(track.album.cover_art_path, 'rb').read(),
                        'image/jpeg')
    song.tag.save()
    logging.info('Metadata for track set.')
