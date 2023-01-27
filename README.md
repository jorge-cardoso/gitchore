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
$ git clone https://github.com/jorge-cardoso/pm_as_code.git
$ cd pm_as_code
```

**Install Modules** using a Virtual Environment

```bash
$ virtualenv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```

**Set up the environment**

```bash
$ export FLASK_APP=run.py
$ export FLASK_ENV=development
```

**Sample Data**

- `samples/ultra_scale_aiops.md`


**Start the application**

```bash
$ flask run 
```
