const headers = {
    headers: {
        'Content-Type': 'application/json'
    }
}
google.charts.load('current', {
    'packages': ['corechart', 'gantt']
});
google.charts.setOnLoadCallback(function () {
  drawTables(url_id);
});

const overview_fields = ["Project name", "Stakeholders", "Team",
                         "Chat rooms", "Cloud storage", "Duration", "Deliverables"]

const description_fields = ["Goal", "Background", "Problem", "Approach", "Results", "KPI"]


function getRows(data, mandatory_keys) {

    if (mandatory_keys == null) {
        mandatory_keys = Object.keys(data);
    }

    var rows = [];
    for (const key in mandatory_keys) {
        key_name = mandatory_keys[key]
        if (!( key_name in data )) {
            row = `<tr> <td><b> ${key_name} </b></td> <td><p style="color:red;">Key not available</p></td> </tr>`;
        }
        else if (data[key_name].length == 1) {
            row = `<tr><td><b> ${key_name} </b></td> <td> ${data[key_name]} </td></tr>`;
        }
        else {
            html_list = []
            for (const element of data[key_name]) {
                li = `<li> ${element} </li>`;
                html_list.push(li);
            }
            html_list = html_list.join('');
            row = `<tr><td><b> ${key_name} </b></td><td> <ul>${html_list} </ul></td></tr>`;
        }
        rows.push(row);
    }
    return rows.join('');
}


function createTable(data, json_key, element_key, mandatory_keys) {
  const rows = getRows(data[json_key], mandatory_keys);
  const html = `
    <table class="table table-striped">
      <tbody>
         ${rows}
      </tbody>
    </table>
  `
  var container = document.getElementById(element_key);
  container.insertAdjacentHTML('beforeend', html);
}

function drawTaskTable(data, element_key) {

    var table = ['<table class="table table-striped"><tbody>'];
    table.push('<tr><th>Task</th><th>Phase</th><th>Description</th></tr>');
    for (const [task_name, value] of Object.entries(data)) {
        table.push('<tr>');
        table.push(`<td>${task_name.slice(1)}</td>`);

        resource = parseTags(String(data[task_name]))[1];
        table.push(`<td>${resource.slice(1)}</td>`);

        description = String(data[task_name]).split(']')[1]
        table.push(`<td>${description}</td>`);
        table.push('</tr>');
    }
    table.push('</tbody></table>');

    var container = document.getElementById(element_key);
    container.insertAdjacentHTML('beforeend', table.join('\n'));
}

function drawSprintTable(data, element_key) {

    sprints = parseSprints(data['Sprints'], data['Tasks']);
    sprints = sprints.sort(function(a, b) {
        return b[3] > a[3];
    });

//    console.log(sprints);

    var table = ['<table class="table table-striped"><tbody>'];
    table.push('<tr><th>Task</th><th>Phase</th><th>User</th><th>Start</th><th>End</th><th>Description</th></tr>');
    for (const sprint of Object.entries(sprints)) {

//        console.log('sprint: ' + sprint);

        s = sprint[1]
        table.push('<tr>');
        table.push(`<td>${s[0]}</td>`);
        table.push(`<td>${s[2]}</td>`);
        table.push(`<td>${s[8]}</td>`);

        table.push(`<td>${moment(s[3]).format('YYYY-MM-DD')}</td>`);
        table.push(`<td>${moment(s[4]).format('YYYY-MM-DD')}</td>`);
        table.push(`<td>${s[9]}</td>`);
        table.push('</tr>');
    }
    table.push('</tbody></table>');

    var container = document.getElementById(element_key);
    container.insertAdjacentHTML('beforeend', table.join('\n'));
}


function drawTables(url_id) {
    fetch("/api/url/" + url_id, {
            method: "GET",
            headers: headers
        })
        .then(response => response.json())
        .then(function (data) {
            createTable(data, 'Overview', 'project_overview', overview_fields);
            createTable(data, 'Description', 'project_description', description_fields);
            drawTaskTable(data['Tasks'], 'project_tasks');
            drawSprintTable(data, 'project_sprints');
            createTable(data, 'Results', 'project_results', null);
            drawCharts(data);
        })
        .catch(function (err) {
            console.log('error: ' + err);
        });
}

function parseTags(str) {
    try {
        // [&Demo, @j00760260, %75]
        tags = str.trim().match(/\[(.*?)\]/);
        if ( !tags ) {
            throw new Error('Unable to parse task tags: ' + str);
        }
    } catch (err) {
        let notify = document.getElementById("err");
        notify.innerHTML = err;
        notify.style.display = "block";
    }
    return tags
}

function parseTag(str, regex) {
    try {
        // &Demo,
        tag = str.trim().match(regex);
        if ( !tag ) {
            throw new Error('Unable to parse tag: ' + str);
        }
        tag = String(tag).replace(/,\s*$/, "");
    } catch (err) {
        let notify = document.getElementById("err");
        notify.innerHTML = err;
        notify.style.display = "block";
    }
    return tag
}

function parseTask(str) {
    // [&Demo, @j00760260, %75], description of the work done for the task
    try {
        tags = parseTags(str)[1];

        task_name = parseTag(tags, /&\S+/g);
        if ( task_name == null ) {
            throw new Error('Unable to parse task name: ' + str);
        }

        users = parseTag(tags, /@\S+/g);
        if ( users == null ) {
            throw new Error('Unable to parse task users: ' + str);
        }

        progress = parseTag(tags, /%\S+/g);
        if ( progress == null ) {
            throw new Error('Unable to parse task progress: ' + str);
        }

        status = str.split(']')[1]
        if ( status == null ) {
            throw new Error('Unable to parse task status: ' + str);
        }

    } catch (err) {
        let notify = document.getElementById("err");
        notify.innerHTML = err;
        notify.style.display = "block";
    }

    return [task_name, users, progress, status]
}


function parseSprints(data, tasks) {
    var rows = [];
    for (const [sprint_date, status_and_risks] of Object.entries(data)) {
        var date = sprint_date.slice(1)
        for (idx in status_and_risks['status']) {
            // "17.01.2023"
            start = moment(date, "DD.MM.YYYY").toDate();
            end = moment(date, "DD.MM.YYYY").add(7, 'days').toDate();

            status = status_and_risks['status'][idx];
//            console.log(status);

            [task_name, users, progress, description] = parseTask(status);
            if (!( task_name in tasks )) {
                throw new Error('Unable to parse task resources: ' + task_name);
            }
            resource = parseTags(String(tasks[task_name]))[1];
            row = [task_name.slice(1), task_name.slice(1), resource.slice(1),
                   start, end, null, progress, null, users.slice(1), description
                  ];
            rows.push(row)
        }
    }
    return rows
}

function mergeSprints(rows) {
    var dict = {};
    for (i = 0; i < rows.length; i++) {
        task_name = rows[i][1];
        if ( task_name in dict ) {
            dict[task_name][3] = new Date(Math.min(dict[task_name][3], rows[i][4]));
            dict[task_name][4] = new Date(Math.max(dict[task_name][4], rows[i][4]));
        }
        else {
            dict[task_name] = rows[i]
        }
    }
    rows = Object.values(dict);
    return rows;
}

function drawCharts(data) {

    sprints = parseSprints(data['Sprints'], data['Tasks']);
    sprints = mergeSprints(sprints);

    sprints = sprints.map(function(s) { return s.slice(0, 8); });
    sprints = sprints.map(function(s) { return s.slice(0, 6).concat(parseInt(s[6].substring(1)), s.slice(7)); });

    var table = new google.visualization.DataTable();
    table.addColumn('string', 'Task ID');
    table.addColumn('string', 'Task Name');
    table.addColumn('string', 'Resource');
    table.addColumn('date', 'Start Date');
    table.addColumn('date', 'End Date');
    table.addColumn('number', 'Duration');
    table.addColumn('number', 'Percent Complete');
    table.addColumn('string', 'Dependencies');
    table.addRows(sprints);

    var options = {
        height: sprints.length * 40 + 50,
        gantt: {
            criticalPathEnabled: false, // Critical path arrows will be the same as other arrows.
            arrow: {
                angle: 100,
                width: 1,
                color: 'dodgerblue',
                radius: 0
            },
            labelStyle: {
                fontName: 'Verdana',
                fontSize: 12,
                color: 'dodgerblue'
            },
            barCornerRadius: 2,
            backgroundColor: {
                fill: 'transparent',
            },
            innerGridHorizLine: {
                stroke: '#ddd',
                strokeWidth: 0,
            },
            innerGridTrack: {
                fill: 'transparent'
            },
            innerGridDarkTrack: {
                fill: 'transparent'
            },
            percentEnabled: true,
            // percentStyle: {
            //   fill:	'black',
            // },
            shadowEnabled: true
        }
    };
    var chart = new google.visualization.Gantt(document.getElementById('chart_gantt'));
    chart.draw(table, options);
}
