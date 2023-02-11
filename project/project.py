import json

from project.parser import Parser


class Project:
    def __init__(self, content=None, filename=None):
        self.parser = Parser(content=content, filename=filename)

    def get_dict(self):
        p = dict()
        p.update(self.overview())
        p.update(self.description())
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
            print('Unable to find section:', 'Overview')
        else:
            d['Overview'] = self.parser.get_key_values(section[-1])
        return d

    def description(self):
        d = dict()
        section = self.parser.get_element('h1', startswith='Description')
        if not section:
            print('Unable to find section:', 'Description')
        else:
            d['Description'] = self.parser.get_key_values(section[-1])
        return d

    def tasks(self):
        d = dict()
        section = self.parser.get_element('h2', startswith='Tasks')
        if not section:
            print('Unable to find section:', 'Tasks')
        else:
            d['Tasks'] = self.parser.get_key_value(section[-1])
        return d

    def sprints(self):
        d = dict()
        section = self.parser.get_element('h2', startswith='Sprints')
        if not section:
            print('Unable to find section:', 'Sprints')
        else:
            d['Sprints'] = self.parser.get_sprints(section[-1])
        return d

    def results(self):
        d = dict()
        section = self.parser.get_element('h1', startswith='Results')
        if not section:
            print('Unable to find section:', 'Results')
        else:
            d['Results'] = self.parser.get_key_values(section[-1])
        return d


if __name__ == '__main__':
    p = Project(filename='samples/ultra_scale_aiops.md')

    project = p.get_html()
    print(json.dumps(project, indent=2))
    with open('samples/ultra_scale_aiops.html', 'w') as f:
        f.write(project)

    project = p.get_dict()
    print(json.dumps(project, indent=2))
    with open('samples/ultra_scale_aiops.json', 'w') as f:
        json.dump(project, f)
