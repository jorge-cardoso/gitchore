import os
import re
import unicodedata
import json
from datetime import datetime
import logging

from urllib.parse import urlparse
import requests
from flask import Blueprint, render_template, redirect, url_for, request

from app.models import db, Url
from config import CACHE_DIR

from project.project import Project
from project.download import Downloader

logger = logging.getLogger(__name__)

frontend_blueprint = Blueprint('routes', __name__)


def existing_projects():
    response = requests.get('http://127.0.0.1:5000/api/project', verify=False)
    if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type', ''):
        return response.json()['data']
    return {'data': []}


def convert_to_project(content):
    project = Project(content=content.decode())
    return project.get_dict()


@frontend_blueprint.route('/', methods=['GET', 'POST'])
@frontend_blueprint.route('/url', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        project_url = request.form['project_url']

        downloader = Downloader(project_url)

        if not downloader.validate_url():
            logging.warning('Invalid project url: %s', project_url)
            return f'Project url is not valid: {project_url}'

        tmp_filename = downloader.save_tmp()
        # project = Project().load_from_file(tmp_filename)
        # project.name
        content = downloader.get_content()
        project_dict = convert_to_project(content)
        project_name = project_dict['Overview']['Project name'][0]

        exists = Url.query.filter_by(name=project_name).first() is not None
        if exists:
            downloader.delete_tmp()
            return f'Project name already exists: {project_name}'

        try:
            project_file = downloader.mv(tmp_filename, project_name)
            # project_file = downloader.save_project(project_name, project_dict)
            new_url = Url(url=project_url, name=project_name, file=project_file)
            db.session.add(new_url)
            db.session.commit()
            return redirect('/url')
        except Exception:
            os.remove(project_file)
            return f"There was a problem adding new url: {project_url}. File removed: {project_file}"

    else:
        urls = Url.query.order_by(Url.created_at).all()
        return render_template('index.html', urls=urls)


@frontend_blueprint.route('/url/<int:url_id>')
def show(url_id):
    url = Url.query.filter_by(id=url_id).first()
    if not url:
        return f'Project id does not exist: {url_id}'
    urls = Url.query.order_by(Url.created_at).all()
    return render_template('project.html',
                           url_id=url_id,
                           url_name=url.name,
                           urls=urls)


@frontend_blueprint.route('/url/update', methods=['GET'])
def update_all():
    projects = Url.query.all()
    for project in projects:
        content = download_remote_project(project.url)
        project_dict = convert_to_project(content)
        project_name = project_dict['Overview']['Project name']
        if project_name != project.name:
            print("Name of project has changed. Ignoring.")
            continue

        try:
            project_file = save_project_to_file(project_name, project_dict)
            p = Url.query.filter_by(url=project.url).first()
            p.updated_at = datetime.utcnow()
            db.session.commit()
            return redirect('/url')
        except Exception as e:
            return f"There was a problem deleting data: {e}"

    return "Updated"


@frontend_blueprint.route('/url/update/<int:url_id>', methods=['GET', 'POST'])
def update(url_id):
    url = Url.query.get_or_404(url_id)
    print('Update', url)

    if request.method == 'POST':
        url.url = request.form['name']
        print('Post', url.url)

        try:
            db.session.commit()
            return redirect('/url')
        except:
            return "There was a problem updating data."

    else:
        title = "Update Data"
        return render_template('update.html',
                               projects_id=['2'],
                               project_id='1',
                               project_name=['A', 'B'],
                               title=title, url=url)


@frontend_blueprint.route('/url/delete/<int:url_id>')
def delete(url_id):
    url = Url.query.get_or_404(url_id)
    print('Delete', url)

    try:
        db.session.delete(url)
        db.session.commit()
        return redirect('/url')
    except:
        return "There was a problem deleting data."
