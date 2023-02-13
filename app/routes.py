import logging
from datetime import datetime
from sqlalchemy import exc
from flask import Blueprint, render_template, redirect, request

from config import CACHE_DIR
from app.models import db, Url

from project.download import Downloader

logger = logging.getLogger(__name__)

frontend_blueprint = Blueprint('routes', __name__)


@frontend_blueprint.route('/', methods=['GET', 'POST'])
@frontend_blueprint.route('/url', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        project_url = request.form['project_url']

        downloader = Downloader(project_url, CACHE_DIR)

        if not downloader.is_url_valid():
            logging.warning('Invalid project url: %s', project_url)
            return f'Project url is not valid: {project_url}'

        project_name = downloader.project_name()

        if Url.query.filter_by(name=project_name).first() is not None:
            logging.warning('Project name already exists: %s', project_name)
            return f'Project name already exists: {project_name}'

        try:
            project_files = downloader.save()
            if not project_files:
                raise Exception('Unable to save files')
            new_url = Url(url=project_url, name=project_name, file=project_files[1])
            db.session.add(new_url)
            db.session.commit()
            return redirect('/url')
        except (Exception, exc.SQLAlchemyError):
            logging.warning('Unable to add new url: %s', project_url)
            return f'Unable to add new url: {project_url}'

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

        downloader = Downloader(project.url, CACHE_DIR)

        if not downloader.is_url_valid():
            logging.warning('Invalid project url: %s', project.url)
            return f'Project url is not valid: {project.url}'

        if downloader.project_name() != project.name:
            logging.warning('Name of project has changed. Ignoring: %s', project.url)
            continue

        try:
            downloader.save()
            p = Url.query.filter_by(url=project.url).first()
            p.updated_at = datetime.utcnow()
            db.session.commit()

            logging.debug('Project url updated: %s', project.url)

            return redirect('/url')
        except (Exception, exc.SQLAlchemyError) as e:
            return f'Unable to delete data: {e}'

    return 'Updated'


@frontend_blueprint.route('/url/update/<int:url_id>', methods=['GET', 'POST'])
def update(url_id):
    url = Url.query.get_or_404(url_id)

    if request.method == 'POST':
        url.url = request.form['name']
        logger.debug('Updating: %s', url.url)

        try:
            db.session.commit()
            return redirect('/url')
        except exc.SQLAlchemyError:
            return 'Unable to update project url.', 404

    else:
        logger.debug('Fetching: %s', url)
        title = "Update Data"
        return render_template('update.html',
                               projects_id=['2'],
                               project_id='1',
                               project_name=['A', 'B'],
                               title=title, url=url)


@frontend_blueprint.route('/url/delete/<int:url_id>')
def delete(url_id):
    logger.debug('Deleting url_id: %s', url_id)
    try:
        url = Url.query.get_or_404(url_id)
        db.session.delete(url)
        db.session.commit()
        return redirect('/url')
    except exc.SQLAlchemyError:
        logger.warning('Unable to delete url_id: %s', url_id)
        return f'Unable to delete url_id: {url_id}', 404
