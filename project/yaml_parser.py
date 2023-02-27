"""
Adapted from
+ https://github.com/dougli1sqrd/yamldown/blob/master/yamldown/yamldown.py
"""
from typing import IO, Tuple, Dict
from collections import ChainMap
from functools import lru_cache
import yaml

from project.parser import Parser


class YAMLParser(Parser):
    """
    YAML Parser for projects.
    """
    def __init__(self, stream):
        self.yml_dct, _ = load(stream)

    def get_dict(self) -> dict:
        return self.yml_dct

    @lru_cache(maxsize=1)
    def name(self) -> str:
        return self.overview()['Project name']

    def overview(self) -> dict:
        return dict(ChainMap(*self.yml_dct['Overview']))

    def description(self) -> dict:
        return dict(ChainMap(*self.yml_dct['Description']))

    def milestones(self) -> dict:
        return dict(ChainMap(*self.yml_dct['Milestones']))

    def tasks(self) -> dict:
        return dict(ChainMap(*self.yml_dct['Tasks']))

    def sprints(self) -> dict:
        return dict(ChainMap(*self.yml_dct['Sprints']))

    def results(self) -> dict:
        return dict(ChainMap(*self.yml_dct['Results']))


class Buffer(object):

    def __init__(self) -> None:
        self.contents = ""

    def append(self, contents: str) -> None:
        self.contents = "{existing}{end}".format(existing=self.contents, end=contents)

    def empty(self) -> bool:
        return len(self.contents) == 0


def load(stream: IO[str]) -> Tuple[Dict, str]:

    reading_yml = False
    yml_contents = Buffer()
    md_contents = Buffer()
    current_buffer = md_contents

    for line in stream:
        if _is_yaml_start(line, reading_yml):
            reading_yml = True
            current_buffer = yml_contents
            continue

        elif _is_yaml_end(line, reading_yml):
            reading_yml = False
            current_buffer = md_contents
            continue

        current_buffer.append(line)

    yml_dict = yaml.load(yml_contents.contents, Loader=yaml.FullLoader)
    return yml_dict, md_contents.contents.strip("\n")


def _is_yaml_start(line: str, reading_yml: bool) -> bool:
    return line.strip("\n").endswith("---") and not reading_yml


def _is_yaml_end(line: str, reading_yml: bool) -> bool:
    return line.strip("\n").endswith("---") and reading_yml


def dump(yml: Dict, markdown: str, yaml_first=True) -> str:

    yaml_out = yaml.dump(yml, default_flow_style=False, indent=2)

    if yaml_first:
        return "---\n{yml}\n---\n{markdown}".format(yml=yaml_out, markdown=markdown)

    return "{markdown}\n---\n{yml}\n---".format(markdown=markdown, yml=yaml_out)
