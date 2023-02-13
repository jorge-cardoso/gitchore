import os
import logging
import re
import unicodedata
import json
import tempfile
import shutil

import requests
import werkzeug

from config import CACHE_DIR

logger = logging.getLogger(__name__)


def slugify(value, allow_unicode=False):
    """
    Function copied form Django text utils

    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def download_file(url, folder, filename):
    """Downloads a file from the internet, but only if it doesn't already exist on disk.

    Parameters
    ----------
    url : str
      The URL to download.
    folder : list or tuple
      The folder where to store the file, as list.
      For example, use [".", "files", "model"] instead of "./files/model/".
    filename : str
      The name of the file on disk.

    Example
    -------

    >>> download_file(
    ...     'https://upload.wikimedia.org/wikipedia/commons/0/0e/Tree_example_VIS.jpg',
    ...     ('.', 'foo', 'bar'),
    ...     'example.jpg')

    """
    full_filepath = os.path.abspath(os.path.expanduser(os.path.expandvars(
        os.path.join(*tuple(folder)))))

    full_filename = os.path.join(full_filepath, filename)

    if os.path.isfile(full_filename):
        return

    os.makedirs(full_filepath, exist_ok=True)

    resp = requests.get(url, stream=True)

    with open(full_filename, 'wb') as file_desc:
        for chunk in resp.iter_content(chunk_size=5000000):
            file_desc.write(chunk)


def size_fmt(n_bytes):
    for symbol in ['B', 'KB', 'MB', 'GB', 'TB', 'EB', 'ZB']:
        if n_bytes < 1024.0:
            return "{0:3.1f} {1}".format(n_bytes, symbol)
        else:
            n_bytes /= 1024.0
    # Return Yottabytes if all else fails.
    return "{0:3.1f} {1}".format(n_bytes, 'YB')


class Downloader:
    def __init__(self, url):
        self.url = url
        self.tmp = None

    def get_content(self):
        req = requests.get(self.url, allow_redirects=True, verify=False)
        print(req.content)
        return req.content

    def save_project(self, project_name, d):
        filename = os.path.join(CACHE_DIR, slugify(project_name) + '.json')
        print(f'Saving project to file: {filename}')
        with open(filename, 'w') as f:
            json.dump(d, f)
        return filename

    def validate_url(self) -> dict:
        try:
            resp = requests.head(self.url, allow_redirects=True, verify=False)
            return {
                'Content-Length': resp.headers.get('Content-Length'),
                'Content-Type': resp.headers.get('Content-Type')
            }
        except ValueError:
            return {}

    def save_tmp(self):
        self.tmp = tempfile.NamedTemporaryFile()
        logging.debug('Creating temporary file: %s', self.tmp.name)
        self.get_file_chunks(self.tmp.name)
        return self.tmp.name

    def get_file_chunks(self, file_name: str = None):
        logging.debug('Getting remote file: %s', file_name)

        response = requests.get(self.url, stream=True, allow_redirects=True, verify=False)

        with open(file_name, 'wb') as file_desc:
            logging.debug('Saving remote file to: %s', file_name)
            for chunk in response.iter_content(chunk_size=5000000):
                file_desc.write(chunk)

    def delete_tmp(self):
        if not self.tmp:
            print('No tmp file exists')
            return
        self.tmp.close()
        self.tmp = None

    def mv(self, src_filename: str = None, dst_filename: str = None):
        if not self.tmp:
            print('No tmp file exists')
            return

        print("Copy tmp file to: %s", dst_filename)
        shutil.copyfile(src_filename, dst_filename)
        self.tmp.close()
        self.tmp = None
