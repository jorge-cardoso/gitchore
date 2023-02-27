import logging
from io import StringIO
import re

import mistletoe
from bs4 import BeautifulSoup, Tag

from project.parser import Parser

logger = logging.getLogger(__name__)


class HTMLParser(Parser):
    def __init__(self, content=None, filename=None):
        self.parser = Parser(content=content, filename=filename)

    def get_dict(self):
        p = dict()
        p.update(self.overview())
        p.update(self.description())
        p.update(self.milestones())
        p.update(self.tasks())
        p.update(self.sprints())
        p.update(self.results())
        return p

    def get_html(self):
        return self.parser.get_html()

    def name(self):
        return self.overview()['Project name"']

    def overview(self):
        d = dict()
        section = self.parser.get_element('h1', startswith='Overview')
        if not section:
            logger.warning('Unable to find section: Overview')
        else:
            d['Overview'] = self.parser.get_key_values(section[-1])
        return d

    def description(self):
        d = dict()
        section = self.parser.get_element('h1', startswith='Description')
        if not section:
            logger.warning('Unable to find section: Description')
        else:
            d['Description'] = self.parser.get_key_values(section[-1])
        return d

    def milestones(self):
        d = dict()
        section = self.parser.get_element('h1', startswith='Milestones')
        if not section:
            logger.warning('Unable to find section: Milestones')
        else:
            d['Milestones'] = self.parser.get_key_value(section[-1])
        return d

    def tasks(self):
        d = dict()
        section = self.parser.get_element('h1', startswith='Tasks')
        if not section:
            logger.warning('Unable to find section: Tasks')
        else:
            d['Tasks'] = self.parser.get_key_value(section[-1])
        return d

    def sprints(self):
        d = dict()
        section = self.parser.get_element('h1', startswith='Sprints')
        if not section:
            logger.warning('Unable to find section: Sprints')
        else:
            d['Sprints'] = self.parser.get_sprints(section[-1])
        return d

    def results(self):
        d = dict()
        section = self.parser.get_element('h1', startswith='Results')
        if not section:
            logger.warning('Unable to find section: Results')
        else:
            d['Results'] = self.parser.get_key_values(section[-1])
        return d


def get_tags(element):
    return [i for i in element if isinstance(i, Tag)]


class Parser:
    def __init__(self, content=None, filename=None):
        if content:
            html = mistletoe.markdown(StringIO(content))
        else:
            with open(filename, 'r') as fin:
                html = mistletoe.markdown(fin)

        self.html = html
        self.page = BeautifulSoup(self.html, "html.parser")

    def get_html(self):
        return self.html

    def get_element(self, element, startswith):
        return self.page.find_all(element, text=re.compile(startswith))

    def get_key_value(self, header):
        d = {}
        lu = header.find_next('ul')
        for kv in get_tags(lu):
            tokens = kv.text.split(':')
            # todo(jc): if there is more than one symbol ':', we have a bug
            key, value = tokens[0].strip(), tokens[1].strip()
            d[key] = value
        return d

    def get_key_values(self, header):
        d = {}
        next_node = header.find_next('li')
        if not next_node:
            logger.warning('Unable to find <li> after header: %s', header)
            return
        while True:
            if isinstance(next_node, Tag):
                key = next_node.next_element.text.strip()
                values = [value.text.strip() for value in next_node.find_all('li')]
                d[key] = values
            next_node = next_node.find_next_sibling('li')
            if next_node is None:
                break
        return d

    def get_sprints(self, section):
        d = {}
        sprints = section.find_next_sibling('ul')
        if not sprints:
            logger.warning('Unable to find sprint sections')
            return d

        sprints = sprints.find_all('p', text=re.compile('\\$'))
        for sprint in sprints:
            d.update(self.iterate_sprint(sprint))
        return d

    def iterate_sprint(self, header):

        def get_element(name):
            d = {}
            status = status_rec.find_next('em', text=name)
            if not status:
                logger.warning('Not found: %s', name)
            else:
                status = status.find_next('ul')
                for i in get_tags(status):
                    d.setdefault(name.lower(), []).append(i.text)
            return d

        d = dict()

        siblings = header.next_siblings
        spring_date = header.text
        d[spring_date] = {}
        status_rec = get_tags(siblings)
        if not status_rec:
            logger.warning('Unable to find sprint record')
            return
        if len(status_rec) > 1:
            print('Too many sprint records. Selecting first one')
            logger.warning('Too many sprint records. Selecting first one')
        status_rec = status_rec[0]

        d[spring_date].update(get_element('Status'))
        d[spring_date].update(get_element('Risks'))
        return d
