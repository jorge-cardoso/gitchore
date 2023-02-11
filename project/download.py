import os
import re
import unicodedata
import json
import tempfile
import shutil

import requests
import werkzeug

from config import CACHE_DIR


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

    def validate_url(self) -> bool:
        try:
            requests.head(self.url, verify=False)
        except ValueError:
            return False
        return True

    def headers(self) -> dict:
        response = requests.head(self.url)

        filename = response.headers.get("Content-Disposition")
        filesize = response.headers.get("Content-Length")
        filetype = response.headers.get("Content-Type")

        if filename:
            parsed_headers = werkzeug.http.parse_options_header(filename)

            for keys in parsed_headers:
                if "filename" in keys:
                    filename = keys["filename"]
            return {"filename": filename, "filesize": filesize, "filetype": filetype}
        else:
            if filetype:
                if "image" in filetype:
                    if "jpeg" in filetype:
                        return {
                            "filename": "download.jpg",
                            "filesize": filesize,
                            "filetype": filetype,
                        }
                    if "gif" in filetype:
                        return {
                            "filename": "download.gif",
                            "filesize": filesize,
                            "filetype": filetype,
                        }
                    if "png" in filetype:
                        return {
                            "filename": "download.png",
                            "filesize": filesize,
                            "filetype": filetype,
                        }
                    if "webp" in filetype:
                        return {
                            "filename": "download.webp",
                            "filesize": filesize,
                            "filetype": filetype,
                        }
            else:
                return {
                    "filename": "download.html",
                    "filesize": filesize,
                    "filetype": filetype,
                }

    def get_file_chunks(self, file_name: str = None):
        file_info = self.headers()
        file_name = file_name or file_info["filename"]
        response = requests.get(self.url, stream=True)

        with open(file_name, "wb") as file:
            if file_info["filesize"]:
                size = int(file_info["filesize"])
                current = 0
                for chunk in response.iter_content(chunk_size=4096):
                    current += len(chunk)
                    downloaded = current / size * 100
                    file.write(chunk)
            else:
                file.write(requests.get(self.url, stream=True).content)

        return file_name

    def save_tmp(self):
        print("Creating a named temporary file..")
        self.tmp = tempfile.NamedTemporaryFile()
        print("Created file is:", self.tmp)
        print("Name of the file is:", self.tmp.name)
        self.get_file_chunks(self.tmp.name)
        return self.tmp.name

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
