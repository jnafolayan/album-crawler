import os
import requests

from tqdm import tqdm


DOWNLOAD_PATH =\
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downloads')
if not os.path.exists(DOWNLOAD_PATH):
    os.mkdir(DOWNLOAD_PATH)


def download_file(url, file_name, album_name):
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
        raise FileNotFoundError('Could not find the file you were looking for')

    dfile_name = url.split('/')[-1]
    ext = dfile_name.split('.')[-1]

    file_name = dfile_name if not file_name else '{}.{}'.format(file_name, ext)

    file_size = int(response.headers.get('content-length', 0))

    album_path = os.path.join(DOWNLOAD_PATH, album_name)
    if not os.path.exists(album_path):
        os.mkdir(album_path)

    download_path = os.path.join(album_path, file_name)

    try:
        with open(download_path, 'wb') as f:
            written = 0
            for data in tqdm(response.iter_content(),
                             total=file_size,
                             unit='KB',
                             unit_scale=True):
                written += len(data)
                f.write(data)
            print('File downloaded to: {}'.format(download_path))

    except:
        f.close()
        os.unlink(download_path)
        if len(os.listdir(album_path)) == 0:
            os.rmdir(album_path)
        return None

    return download_path


# test
download_file('http://sr-sycdn.kuwo.cn/resource/n1/73/60/707899178.mp3', 'Lover - Taylor Swift', 'Lover - Single')