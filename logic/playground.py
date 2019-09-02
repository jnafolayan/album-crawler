import os

from api_calls import get_track_url_youtube
from utils import (
    get_album_data,
    download_file,
    download_song,
    encode_metadata,
    zip_music_files
)
from logging_config import *


album = get_album_data('Glory Sound Prep')
artpath = download_file(album.cover_art_link, album.to_string, album.to_string)
album.cover_art_path = artpath
album.dir_path = os.path.dirname(album.cover_art_path)

for track in album:
    track.download_link = get_track_url_youtube(track.search_term)
    track.file_path =\
        download_song(track.download_link, album.to_string, str(track))

    encode_metadata(track)

zip_music_files(album)
