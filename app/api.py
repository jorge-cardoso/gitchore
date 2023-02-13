import logging
import os
import json
import click
from flask import Blueprint, request
from flask_restx import Api, Resource, fields
from app.models import db, Project, Url

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

logger = logging.getLogger(__name__)

projects_model = api.model('Project', {
    'id': fields.String,
    'name': fields.String
})

url_model = api.model('Url', {
    'id': fields.String,
    'url': fields.String,
})


def get_files(path, extension=None):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            if not extension or file.endswith(extension):
                yield file


@api.route('/url')
class UrlAPI(Resource):

    @api.marshal_with(url_model, envelope='data')
    def get(self, **kwargs):
        return Url.query.with_entities(Url.id, Url.url).distinct().all()


@api.route('/url/<int:url_id>')
class UrlFileAPI(Resource):

    # @api.marshal_with(project_model, envelope='data')
    def get(self, url_id, **kwargs):
        project = Url.query.get(url_id)
        if not project:
            logger.info('Project url_id does not exist: %s', url_id)
            return {}

        file = project.file
        logger.debug('Loading file: %s', os.path.join(os.getcwd(), project.file))

        if not os.path.exists(file):
            logger.debug('Project file does not exist: %s', file)
            return {}

        with open(file) as fp:
            return json.load(fp)


@api.route('/project/<string:project_name>')
class ProjectAPI(Resource):

    @api.marshal_with(projects_model, envelope='data')
    def get(self, project_name, **kwargs):
        print(f'project_name: {project_name}')
        # return Project.query.all()
        a = Project.query.filter_by(id=project_name).all()
        print(a)
        return a

    @api.expect(projects_model, validate=True)
    def post(self, **kwargs):
        data = request.get_json()
        row = Project(**data)
        db.session.add(row)
        db.session.commit()
        return {'status': 'success'}
