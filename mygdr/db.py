import sqlite3
import json
import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schemes/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    init_db_questions()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def get_data_from_json(str_f):
    with open(str_f) as json_file:
        l = json.load(json_file)
        return l["data"]

def init_db_questions():
    questions = get_data_from_json("mygdr/questions.json")
    print(questions)
    db = get_db()
    for q in questions:
        db.execute(
            'INSERT INTO questions (question, option_a, option_b, option_c, answer)'
            ' VALUES (?, ?, ?, ?, ?)',
            (q['question'], q['options'][0], q['options'][1], q['options'][2], q['answer'])
        )

    db.commit()
