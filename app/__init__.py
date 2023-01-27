import os
from flask import Flask

from app.models import db, Project, Description
from app.api import api_blueprint
from app.routes import frontend_blueprint
from app.loader import data_importer, data_importer_json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(frontend_blueprint)
app.register_blueprint(api_blueprint, url_prefix='/api')


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

