"""
Adapted from
+ https://github.com/dougli1sqrd/yamldown/blob/master/yamldown/yamldown.py
"""
from typing import IO, Tuple, Dict
from collections import ChainMap
from functools import lru_cache
import re
import yaml

from project.parser import Parser
from project.fields import FIELDS


class YAMLParser(Parser):
    """
    YAML Parser for projects.
    """
    def __init__(self, stream):
        self.yml_dct, _ = load(stream)

    def get_dict(self) -> dict:
        # return self.yml_dct
        return self.overview() |\
            self.description() |\
            self.milestones() |\
            self.tasks() |\
            self.sprints() |\
            self.results()

    @lru_cache(maxsize=1)
    def name(self) -> str:
        return self.overview()['Project name']

    def overview(self) -> dict:
        return {'Overview': dict(ChainMap(*self.yml_dct['Overview']))}

    def description(self) -> dict:
        return {'Description': dict(ChainMap(*self.yml_dct['Description']))}

    def milestones(self) -> dict:
        m = {}
        for dct in self.yml_dct['Milestones']:
            if not dct:
                continue
            key, value = list(dct.items())[0]
            match = re.search(FIELDS['Milestones']['regex'], value)
            if not match:
                continue
            date, description = match.groups()
            m.update({key: {'date': date, 'description': description}})

        return {'Milestones': m}

    def tasks(self) -> dict:
        m = {}
        for dct in self.yml_dct['Tasks']:
            if not dct:
                continue
            key, value = list(dct.items())[0]
            match = re.search(FIELDS['Task_description']['regex'], value)
            if not match:
                continue
            date, description = match.groups()
            m.update({key: {'phase': date, 'description': description}})

        return {'Tasks': m}

    def sprints(self) -> dict:
        m = []
        for sub_sprint in self.yml_dct['Sprints']:
            if not sub_sprint:
                print('No sub_print:', sub_sprint)
                continue
            _, sprints = list(sub_sprint.items())[0]

            for s in sprints:
                date, value = list(s.items())[0]
                tasks_status = value[0]['Status']
                # parser risk -> function
                risks = value[1]['Risks']
                m1 = []
                for sts in tasks_status:
                    # parser task status -> function
                    match = re.search(FIELDS['Status']['regex'], sts)
                    if not match:
                        print('No match:', sts)
                        continue
                    task, name, _id, perct = match.groups()
                    m1.append({'task_name': task,
                               'user_name': name.strip(),
                               'user_id': _id,
                               '%': perct
                               })

                m.append({date: {'Tasks': m1, 'Risks': risks}})

        return {'Sprints': m}

    def results(self) -> dict:
        return {'Results': dict(ChainMap(*self.yml_dct['Results']))}


class Buffer(object):

    def __init__(self) -> None:
        self.contents = ''

    def append(self, contents: str) -> None:
        self.contents = f'{self.contents}{contents}'

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

        current_buffer.append(line + '\n')

    yml_dict = yaml.load(yml_contents.contents, Loader=yaml.FullLoader)
    return yml_dict, md_contents.contents.strip('\n')


def _is_yaml_start(line: str, reading_yml: bool) -> bool:
    return line.strip('\n').endswith('---') and not reading_yml


def _is_yaml_end(line: str, reading_yml: bool) -> bool:
    return line.strip('\n').endswith('---') and reading_yml


def dump(yml: Dict, markdown: str, yaml_first=True) -> str:

    yaml_out = yaml.dump(yml, default_flow_style=False, indent=2)

    if yaml_first:
        return f'---\n{yaml_out}\n---\n{markdown}'

    return f'{markdown}\n---\n{yaml_out}\n---'
