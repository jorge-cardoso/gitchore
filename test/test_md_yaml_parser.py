import unittest
import io
from typing import IO

import project.md_yaml_parser as yaml_parser


def yaml_first_yaml_parser() -> str:
    lines = [
        "---",
        "things:",
        "  - hello",
        "  - world",
        "foo: bar",
        "---",
        "This is some markdown text"
    ]
    return "\n".join(lines)


def just_yaml() -> str:
    lines = [
        "---",
        "things:",
        "  - hello",
        "  - world",
        "foo: bar"
    ]
    return "\n".join(lines)


def just_md() -> str:
    return "This is some markdown text"


def md_first_yaml_parser() -> str:
    lines = [
        "This is some markdown text",
        "---",
        "things:",
        "  - hello",
        "  - world",
        "foo: bar",
        "---"
    ]
    return "\n".join(lines)


def buffer_with(contents: str) -> yaml_parser.Buffer:
    b = yaml_parser.Buffer()
    b.append(contents)
    return b


def string_document(contents: str) -> IO[str]:
    return io.StringIO(contents)


class TestYAMLParser(unittest.TestCase):

    def test_yaml_start_at_start(self):
        start = yaml_parser._is_yaml_start("---\n", False)
        self.assertTrue(start)

    def test_yaml_not_started(self):
        start = yaml_parser._is_yaml_start("foo", False)
        self.assertFalse(start)

    def test_yaml_already_started(self):
        start = yaml_parser._is_yaml_start("- foo\n", True)
        self.assertFalse(start)

    def test_yaml_end_at_end(self):
        start = yaml_parser._is_yaml_end("---\n", True)
        self.assertTrue(start)

    def test_yaml_not_ended(self):
        start = yaml_parser._is_yaml_end("- foo\n", True)
        self.assertFalse(start)

    def test_yaml_not_started(self):
        start = yaml_parser._is_yaml_end("foo", False)
        self.assertFalse(start)

    def testload_yaml_first(self):
        doc = string_document(yaml_first_yaml_parser())
        yml_contents, md_contents = yaml_parser.load(doc)

        expected_yml = {
            "things": [
                "hello",
                "world"
            ],
            "foo": "bar"
        }
        expected_md = "This is some markdown text"

        self.assertEqual(yml_contents, expected_yml)
        self.assertEqual(md_contents, expected_md)

    def testload_md_first(self):
        doc = string_document(md_first_yaml_parser())
        yml_contents, md_contents = yaml_parser.load(doc)

        expected_yml = {
            "things": [
                "hello",
                "world"
            ],
            "foo": "bar"
        }
        expected_md = "This is some markdown text"

        self.assertEqual(yml_contents, expected_yml)
        self.assertEqual(md_contents, expected_md)

    def test_load_file(self):
        with open("./test/files/ultra_scale_aiops.md", "r") as f:
            project = yaml_parser.YAMLParser(f)
            print(project.overview())
            print(project.description())
            print(project.milestones())
            print(project.tasks())
            print(project.sprints())
            print(project.results())

            print(project.get_dict())


class TestDump(unittest.TestCase):

    def testdump_yaml_first(self):
        yml = {
            "things": [
                "hello",
                "world"
            ],
            "foo": "bar"
        }
        md = "This is some markdown text"

        yaml_parserdump = yaml_parser.dump(yml, md)
        docdump = string_document(yaml_parserdump)
        expected = string_document(yaml_first_yaml_parser())

        self.assertEqual(yaml_parser.load(docdump), yaml_parser.load(expected))

    def testdump_md_first(self):
        yml = {
            "things": [
                "hello",
                "world"
            ],
            "foo": "bar"
        }
        md = "This is some markdown text"

        yaml_parserdump = yaml_parser.dump(yml, md, yaml_first=True)
        docdump = string_document(yaml_parserdump)
        expected = string_document(md_first_yaml_parser())

        self.assertEqual(yaml_parser.load(docdump), yaml_parser.load(expected))


if __name__ == "__main__":
    unittest.main()
