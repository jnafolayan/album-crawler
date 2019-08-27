
from api_calls import get_track_url_youtube
from utils import get_album_data, download_file, download_song


album = get_album_data('Glory Sound Prep')
download_file(album.cover_art_link, album.to_string, album.to_string)

for track in album:
    url = get_track_url_youtube(track.search_term)
    track.download_link = url

for track in album:
    download_song(track.download_link, album.to_string, str(track))
