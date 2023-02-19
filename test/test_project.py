import unittest
import os
import json

from project.project import Project


class ProjectTest(unittest.TestCase):

    def setUp(self):
        self.module_dir = os.path.realpath(os.path.dirname(__file__))
        filename = os.path.join(self.module_dir, 'files', 'ultra_scale_aiops.md')
        self.project = Project(filename=filename)

    def test_get_html(self):
        html = self.project.get_html()
        self.assertTrue(html.startswith('<'))

    def test_get_dict(self):
        dct = self.project.get_dict()
        self.assertTrue(isinstance(dct, dict))

    def test_json(self):
        dct = self.project.get_dict()
        filename = os.path.join(self.module_dir, 'files', 'ultra_scale_aiops.json')
        with open(filename, 'w') as f:
            json.dump(dct, f, indent=2)
