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

You can use PM Flavored Markdown for:
+ Overview
+ Description
+ Tasks
+ Sprints
+ Results


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
