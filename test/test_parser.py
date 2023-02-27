import unittest
import os

from project import parser_html


class ParserTest(unittest.TestCase):

    def setUp(self):
        module_dir = os.path.realpath(os.path.dirname(__file__))
        self.parser = parser.Parser(filename=os.path.join(module_dir, 'files', 'ultra_scale_aiops.md'))

    def test_get_element(self):
        section = self.parser.get_element('h1', startswith='Overview')
        self.assertTrue(section)

    def test_get_key_values(self):
        section = self.parser.get_element('h1', startswith='Overview')
        kv = self.parser.get_key_values(section[-1])
        self.assertTrue(isinstance(kv, dict))
