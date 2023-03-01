import os
import tempfile
import unittest

from project import download


class DownloaderTest(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.url = 'https://raw.githubusercontent.com/jorge-cardoso/gitchore/main/' \
                   'samples/ultra_scale_aiops.md'
        self.dl = download.Downloader(self.url, self.tmp_dir.name)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_download(self):
        self.assertTrue(isinstance(self.dl.download().get_dict(), dict))

    def test_project_name(self):
        project = self.dl.download()
        self.assertTrue(isinstance(project.name(), str))
        self.assertEqual(project.name(), 'AI for Project Management')

    def test_save(self):
        self.files_created = self.dl.save()
        for file_path in self.files_created:
            self.assertTrue(os.path.isfile(file_path))
