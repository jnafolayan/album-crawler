
from api_calls import get_track_url_youtube
from utils import get_album_data, download_file, download_song


hc = get_album_data('Glory Sound Prep')
download_file(hc.cover_art_link, hc.to_str, hc.to_str)
for track in hc:
    url = get_track_url_youtube('{} {}'.format(track.title,
                                               ' '.join(track.artiste)))
    track.download_link = url

for track in hc:
    download_song(track.download_link, hc.to_str, str(track))
