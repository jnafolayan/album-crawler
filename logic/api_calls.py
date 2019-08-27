import os
import json

import requests
import musicbrainzngs
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build

from school import Track, Album
from logging.config import *


def get_album_data_lastfm(query: str):  # deprecated, spotify API is superior
    """
    takes a query string and searches music brainz for album matches
    if match found, the album id is used to query the LastFM api for album data
    if a match is found, data is stored in Album object and returned.

    :params query: string, a search term for finding albums

    :returns new_album: logic.school.Album, a list of logic.school.Track
                        objects
    :excepts KeyError: returns none, when data isn't found
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95'
        ' Safari/537.36'
    }

    musicbrainzngs.set_useragent(headers['User-Agent'], version=2)
    result = musicbrainzngs.search_releases(query)
    mbid = result['release-list'][0]['id']  # music brainz album id

    params = {
        'method': 'album.getinfo',
        'api_key': os.environ.get('LASTFM_API_KEY'),
        'format': 'json',
        'mbid': mbid
    }

    url = 'http://ws.audioscrobbler.com/2.0/'
    response = requests.get(url, headers=headers, params=params)
    response_dict = json.loads(response.text)

    try:
        album_name = response_dict['album']['name']
        album_artist = response_dict['album']['artist']
    except KeyError:
        print('Album not found in LastFM.')
        return None

    new_album = Album(album_name, [album_artist])
    new_album.cover_art_link = response_dict['album']['image'][2]['#text']

    for track in response_dict['album']['tracks']['track']:
        new_album.add_track(Track(
            track['name'],
            [track['artist']['name']],
            album=new_album
        ))

    return new_album


def get_album_data_spotify(query: str):
    """
    takes a query string and returns data on album query if found
    : params query: string, a search term for finding albums

    :returns new_album: logic.school.Album object

    :excepts KeyError: returns none, when data isn't found
    """

    client_id = os.environ.get('SPOTIFY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
    credentials_manager = SpotifyClientCredentials(client_id=client_id,
                                                   client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=credentials_manager)
    logging.info('Searching Spotify for query: {}'.format(query))
    results = sp.search(q='album: ' + query, type='album')
    try:
        album_id = results['albums']['items'][0]['id']
    except KeyError:
        logging.warning('Query "{}", has no matches'.format(query))
        return None  # album not found

    album = sp.album(album_id)

    album_name = album['name']
    artistes = [artiste['name'] for artiste in album['artists']]

    new_album = Album(name=album_name, artiste=artistes)
    new_album.cover_art_link = album['images'][0]['url']

    for track in album['tracks']['items']:
        track = Track(
            title=track['name'],
            artiste=[track['artists'][0]['name']],
            features=[artist['name'] for artist in track['artists']][0:],
            album=new_album
        )
        new_album.add_track(track)

    logging.info('Album data retrieved for: {}'.format(album_name))
    return new_album


def get_track_url_youtube(query: str):
    """
    gets streaming url for tracks from youtube
    :params query: string, to search for the track

    :returns url: string, url for the audio file
    """

    api_key = os.environ.get('GOOGLE_API_KEY')
    api_service = 'youtube'
    api_version = 'v3'

    youtube = build(api_service, api_version, developerKey=api_key,
                    cache_discovery=False)

    logging.info('Getting Youtube results for query: {}'.format(query))
    results = youtube.search().list(
        q=query + ' audio',
        part='snippet',
        maxResults=3,
        type='video'
    ).execute()

    try:
        first_result = results['items'][0]['id']['videoId']
        url = 'https://youtube.com/watch?v={}'.format(first_result)
    except IndexError:
        logging.info('No results found for: "{}"'.format(query))
        return None

    logging.info('Url gotten for query: {}'.format(url))
    return url
