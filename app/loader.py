import os
import json
from csv import DictReader
import click
import sqlalchemy


def data_importer(db, DataModel, file_path):
    print(f'Loading file: {os.getcwd()}, {file_path}')

    try:
        with open(file_path) as fp:

            rd = DictReader(fp)
            for cnt, row in enumerate(rd):
                print(f'Importing: {row}')
                record = DataModel(**row)
                db.session.add(record)
            db.session.commit()
            click.echo(click.style(f"Added {cnt} records in {DataModel.__name__}", fg="green"))

    except sqlalchemy.exc.IntegrityError:
        click.echo(click.style(f"Could not load data in {DataModel.__name__}, UNIQUE constraint failed", fg="red"))
        db.session.rollback()
    finally:
        db.session.close()


def data_importer_json(db, DataModel, file_path):
    print(f'Loading file: {os.getcwd()}, {file_path}')

    try:
        with open(file_path) as fp:

            j = json.load(fp)
            description = j['Description']
            print(f'Importing: {description}')

            for k, v in description.items():
                description[k] = ' '.join(v)

            # description['id'] = j['Overview']['Project name'].strip()
            description['id'] = 'aiops'
            record = DataModel(**description)
            db.session.add(record)
            db.session.commit()
            click.echo(click.style(f"Added 1 record in {DataModel.__name__}", fg="green"))

    except sqlalchemy.exc.IntegrityError:
        click.echo(click.style(f"Could not load data in {DataModel.__name__}, UNIQUE constraint failed", fg="red"))
        db.session.rollback()
    finally:
        db.session.close()

