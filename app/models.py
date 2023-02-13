from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Project(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(50), nullable=False, unique=False)
    name = db.Column(db.String(50), nullable=False, unique=False)
    task = db.Column(db.String(50), nullable=False, unique=False)
    phase = db.Column(db.String(50), nullable=True, unique=False)
    start = db.Column(db.String(50), nullable=False, unique=False)
    end = db.Column(db.String(50), nullable=False, unique=False)
    users = db.Column(db.String(50), nullable=False, unique=False)
    completion = db.Column(db.Float)
    risk = db.Column(db.String(50), nullable=False, unique=False)

    def __repr__(self):
        return '<Project %r>' % self.name


class Description(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(500), nullable=False, unique=False)
    Goal = db.Column(db.String(500), nullable=False, unique=False)
    Background = db.Column(db.String(500), nullable=False, unique=False)
    Problem = db.Column(db.String(500), nullable=True, unique=False)
    Approach = db.Column(db.String(500), nullable=False, unique=False)
    Results = db.Column(db.String(500), nullable=False, unique=False)


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(256), nullable=False)
    file = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Url %r>' % self.url
