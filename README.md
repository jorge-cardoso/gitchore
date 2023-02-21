# Next Steps
+ Define a language for the description
  + dates, date ranges, metada, headers, list: see https://github.com/hotoo/markline
+ Implement the notion of timeline
  + https://matplotlib.org/stable/gallery/lines_bars_and_markers/timeline.html
  + https://medium.com/unfound-news/auto-timeline-generate-a-high-quality-timeline-of-any-topic-using-machine-learning-269224878eb9
  + https://github.com/jasonreisman/Timeline
+ Write full project description example
+ Implement schema on the client side
+ Test if md files can be retrieved from other CVS
+ Add logging 
+ Write unittests

# Gitchore - Git-based Project Management

Gitchore collects project management descriptions from git repos via HTTP endpoints.
Projects are written using PM Flavored Markdown

Key features/ideas
+ Markdown and extensions for project management
+ Git-driven
+ Decentralized
+ Schema verification

Tech. Stack
+ Markdown, Javascript, Google Charts, Bootstrap, Python, Flask, Flask-RestX, Flask-SqlAlchemy, SQLite


## PM Flavored Markdown

+ for an example, see  https://docs.gauge.org/writing-specifications.html?os=linux&language=javascript&ide=vscode

### Sections
A project description consists of different sections;
some of which are mandatory and few are optional.

The sections of a PM Flavored Markdown are as follows:
+ Overview
+ Description
+ Tasks
+ Sprints
+ Results

Section headings are written in the <h1> Markdown syntax in 
one of the following ways:

#### Example

In the following example, # Overview is the section heading,
followed by tags and steps (statements preceded by *).

> # Overview

#### Overview

#### Description

#### Tasks

Tasks are the executable components of a project that are written 
by using the Markdown unordered list syntax.


#### Sprints

#### Results

### Dates

Parameters are used as placeholders instead of actual values.
These parameters are used when referring to a table column value of a
data table. Data tables are defined at the beginning of a spec.
Parameters are also used as values in a Concept.
Parameters have the following syntax: <param>.

> Login as user <username> and "password"

### Tags

> Verify email text is <tag:research>
 
### Phases



## How to use it

**Clone Repo**

```bash
$ git clone https://github.com/jorge-cardoso/gitchore
$ cd gitchore
```

**Install Modules** using a Virtual Environment

```bash
$ virtualenv env
$ source env/bin/activate
$ pip3 install -r pip-requirements.txt
```

**Set up the environment**

FLASK_DEBUG enables hot reloading. 

```bash
$ export FLASK_APP=run.py
$ export FLASK_ENV=development
$ export FLASK_DEBUG=1  
```

**Directories**

- log to keep the logs
- instance to keep the database 

**Sample Data**

- `samples/ultra_scale_aiops.md`


**Start the application**

```bash
$  flask run --host=0.0.0.0 --port=8011
```
