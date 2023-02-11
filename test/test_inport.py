import unittest
import os

from project import inport


class InportTest(unittest.TestCase):

    def setUp(self):
        module_dir = os.path.realpath(os.path.dirname(__file__))
        self.p = inport.Inport(filename=os.path.join(module_dir, 'files', 'ultra_scale_aiops.md'))

    def test_get_html(self):
        project_html = self.p.get_html()
        self.assertTrue('<h1>' in project_html)

    def test_get_dict(self):
        project_dct = self.p.get_dict()
        for k in inport.PROJECT_KEYS:
            self.assertTrue(k in project_dct, f'{k} in not in project dct')


if __name__ == "__main__":
    unittest.main()
