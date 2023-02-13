import re
import json
import pandas as pd

from project.project import Project


class ExportProject:
    def __init__(self):
        pass

    def dump(self, project):
        name, _ = os.path.splitext(self.filename)
        # project = self.create()
        with open(f'{name}.json', 'w', encoding='utf-8') as f:
            json.dump(project, f, ensure_ascii=False, indent=4)

    def export(self, project):

        data = {}

        print(project['Overview'])
        project_name = project['Overview']['Project name'][0].split(':')[1].strip()
        project_id = project_name.lower().replace(' ', '_')
        # start_date, end_date = [i.strip() for i in project['Overview']['Duration'][0].split('--')]
        duration = project['Overview']['Duration']
        print(duration)
        start_date = pd.to_datetime(duration[0].split(':')[1].strip(), format='%d.%m.%Y')
        end_date = pd.to_datetime(duration[1].split(':')[1].strip(), format='%d.%m.%Y')
        print(start_date)

        for sprint_month in project['Sprints']:
            print(sprint_month)
            month = project['Sprints'][sprint_month]

            # print(month)
            task_phase = {}

            for sprint_week in month:

                phase = 'Other'

                if sprint_week == 'Tasks':
                    print(month[sprint_week])
                    for task, description in month[sprint_week].items():
                        m = re.search(r"\[(.*?)\]", description[0])
                        if not m:
                            print(f'Unable to parse status: {s}')
                            return
                        tags = m.group(1)
                        phase = re.findall(r'(#[A-Za-z0-9_-]*)', tags)[0]
                        task_phase[task] = phase
                    continue

                status = month[sprint_week]['Status']
                risk = month[sprint_week]['Risks']

                for s in status:
                    m = re.search(r"\[(.*?)\]", s)
                    if not m:
                        print(f'Unable to parse status: {s}')
                        return
                    tags = m.group(1)
                    task_name = re.findall(r'(\&[A-Za-z0-9_-]*)', tags)[0]
                    users = re.findall(r'(\@[A-Za-z0-9_-]*)', tags)[0]
                    progress = float(re.findall(r'(%\d+(\.\d+)?)', tags)[0][0][1:]) / 100
                    date = pd.to_datetime(sprint_week, format='%d.%m.%Y')
                    new_task = [project_id, project_name, task_name, task_phase[task_name] if task_name in task_phase else phase,
                                date, date, users, progress, risk]

                    print(new_task)

                    if task_name in data:
                        _tasks = [data[task_name], new_task]
                        start_time = min([t[4] for t in _tasks])
                        end_time = max([t[5] for t in _tasks])
                        max_progress = max([t[7] for t in _tasks])
                        data[task_name] = [project_id, project_name, task_name, new_task[3],
                                           start_time, end_time, new_task[6], max_progress, new_task[-1]]
                    else:
                        data[task_name] = new_task

        return list(data.values()), start_date, end_date


if __name__ == '__main__':
    import os
    print(os.getcwd())

    project = Project(filename='data/project_example.md').get_dict()
    exporter = ExportProject()
    data, start_date, end_date = exporter.export(project)
    print('-' * 30)
    print(data)

    df = pd.DataFrame(data, columns=['id', 'name', 'task', 'phase', 'start', 'end', 'users', 'completion', 'risk'])
    df.to_csv('data/project_example.csv', index=False)
    # pp.pprint(dd, indent=2)
    print(json.dumps(project, indent=2))

