import os
import logging
import re
import unicodedata
import json

import requests

from project import project

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


def size_fmt(n_bytes):
    for symbol in ['B', 'KB', 'MB', 'GB', 'TB', 'EB', 'ZB']:
        if n_bytes < 1024.0:
            return "{0:3.1f} {1}".format(n_bytes, symbol)
        else:
            n_bytes /= 1024.0
    # Return Yottabytes if all else fails.
    return "{0:3.1f} {1}".format(n_bytes, 'YB')


class Downloader:
    """Downloads a file from the internet."""
    def __init__(self, url, local_dir):
        self.url = url
        self.local_dir = local_dir
        self.content = None
        self.project = {}

    def is_url_valid(self) -> dict:
        try:
            resp = requests.head(self.url, allow_redirects=True, verify=False)
            return {
                'Content-Length': resp.headers.get('Content-Length'),
                'Content-Type': resp.headers.get('Content-Type')
            }
        except ValueError:
            return {}

    def get_content(self):
        req = requests.get(self.url, allow_redirects=True, verify=False)
        self.content = req.content
        return self.content

    def get_project(self):
        if not self.content:
            self.get_content()

        proj = project.Project(content=self.content.decode())
        self.project = proj.get_dict()
        return self.project

    def project_name(self):
        if not self.project:
            self.get_project()
        return self.project['Overview']['Project name'][0]

    def save(self):
        md_file = os.path.join(self.local_dir, slugify(self.project_name()) + '.md')
        json_file = os.path.join(self.local_dir, slugify(self.project_name()) + '.json')

        if (self._save_helper(md_file, self.content.decode()) and
                self._save_helper(json_file, json.dumps(self.project, indent=4))):
            return [md_file, json_file]

        return []

    def _save_helper(self, file_name, content):
        logging.debug(f'Saving content to file: {file_name}')
        try:
            with open(file_name, 'w') as f:
                try:
                    f.write(content)
                    return True
                except (IOError, OSError):
                    logging.warning('Error writing to file: %s', file_name)
        except (FileNotFoundError, PermissionError, OSError):
            logging.warning('Error opening file: %s', file_name)
        return False
