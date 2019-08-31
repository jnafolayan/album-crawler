import os

import zipfile
import requests
import youtube_dl
from tqdm import tqdm

from api_calls import (
    get_album_data_spotify,
    get_album_data_lastfm
)
from logging_config import *


DOWNLOAD_PATH =\
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downloads')
if not os.path.exists(DOWNLOAD_PATH):
    os.mkdir(DOWNLOAD_PATH)

ARCHIVE_PATH = \
    os.path.join("../", "archives")
if not os.path.exists(ARCHIVE_PATH):
    os.mkdir(ARCHIVE_PATH)


def download_file(url, album_name, file_name=None):
    """
    params url: string containing the media file url
    params file_name: string for the storage name of the file to be downloaded
                      if blank, file URI is used.
    params album_name: string for the album name of the file

    returns: string path of downloaded file
    """

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException:
        logging.warning('Could not get url: {}'.format(url))
        return None

    dfile_name = url.split('/')[-1]
    ext = response.headers['content-type'].split('/')[-1]

    file_name = dfile_name if not file_name else '{}.{}'.format(file_name, ext)

    file_size = int(response.headers.get('content-length', 0))

    album_path = os.path.join(DOWNLOAD_PATH, album_name)
    if not os.path.exists(album_path):
        os.mkdir(album_path)

    download_path = os.path.join(album_path, file_name)

    try:
        with open(download_path, 'wb') as f:
            logging.info('Downloading file: {}'.format(file_name))
            written = 0
            for data in tqdm(response.iter_content(),
                             total=file_size,
                             unit='KB',
                             unit_scale=True):
                written += len(data)
                f.write(data)
            logging.info('Download complete, file downloaded to: {}'
                         .format(download_path))

    except KeyboardInterrupt:
        logging.warning('Download stopped. Removing file at {}...'
                        .format(download_path))
        f.close()
        os.unlink(download_path)
        if len(os.listdir(album_path)) == 0:
            os.rmdir(album_path)
        logging.info('File removed.')
        return None

    return download_path

def download_song(url, album_name, file_name):
    path = os.path.join(DOWNLOAD_PATH, album_name)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320'
        }],
        'outtmpl': os.path.join(path, '{}.%(ext)s'.format(file_name))
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    download_path = os.path.join(path, '{}.mp3'.format(file_name))
    return download_path

def get_album_data(query: str):
    album = get_album_data_spotify(query)
    if album is None:
        album = get_album_data_lastfm(query)
    return album

def zip_music_files(path: str, album_obj: Album):
    """Compresses the requested album for download by the user
    
    Arguments:
        path {str} -- [The path where the created .zip file will be stored]
        album_obj {Album} -- [The album object for which a zip file will be created]
    """
    original_dir = os.getcwd()
    os.chdir(DOWNLOAD_PATH)

    album_archive_name = f"{album_obj.to_string}.zip"
    album_archive_path = os.path.join(ARCHIVE_PATH, album_archive_name)
    music_files = [file for file in os.listdir() if file.endswith(".mp3")]

    with zipfile.ZipFile(album_archive_path, "w") as album_archive:
        for music_file in music_files:
            print("Compressing file...")
            album_archive.write(music_file, compress_type=zipfile.ZIP_DEFLATED)
            os.remove(music_file)

    os.chdir(original_dir)