import os
from flask import Flask

from app.config.reader import constants
from config import DB_DIR
from app.models import db, Project, Description
from app.api import api_blueprint
from app.routes import frontend_blueprint
from app.loader import data_importer, data_importer_json

from app.setup import setup_logging


def check_configuration():
    logfile = os.path.abspath(constants.LOG_FILE)
    if not os.path.isdir(os.path.dirname(logfile)):
        raise Exception('Could not create log file. '
                        'Directory does not exist:', os.path.dirname(logfile))


def create_app():
    setup_logging(None)

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(frontend_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app


check_configuration()
app = create_app()


@app.cli.command('load-data')
def load_data():
    db.drop_all()
    db.create_all()

    dir = 'data'
    for filename in os.listdir(dir):
        fname = os.path.join(dir, filename)
        if os.path.isfile(fname) and filename.endswith('.csv'):
            print(f'Loading: {fname}')
            data_importer(db, Project, fname)
        if os.path.isfile(fname) and filename.endswith('.json'):
            print(f'Loading: {fname}')
            data_importer_json(db, Description, fname)


@app.before_first_request
def initialize_database():
    db.create_all() 


db.init_app(app)
