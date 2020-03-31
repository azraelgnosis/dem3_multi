import click
import sqlite3
from flask import current_app, g
from flask.cli import with_appcontext
import os
import re
import xml.etree.ElementTree as ET

def get_db() -> sqlite3.Connection:
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None): 
    if db := g.pop('db', None):
        db.close()

def get_usernames() -> list:
    ":return: list of usernames"
    db = get_db()

    sql_select_usernames = "SELECT players.username FROM players"

    usernames = db.execute(sql_select_usernames)
    usernames = [row.username for row in usernames]

    return usernames

save_path = r"C:\Users\root\Documents\My Games\democracy3\savegames"
save_filename = "test1.xml"

with open(os.path.join(save_path, save_filename)) as f:
    xml = f.read()

xml = "<xml>\n" + xml # add opening <xml> tag to complement end tag

# replaces <0>...</0> with <_0>...</_0> and <0_hist>...</0_hist> with <_0_hist>...</_0_hist>
xml = re.sub(r"<(\d{1,2}(?:_hist)?>)(.*)</(\d{1,2}(?:_hist)?>)", r"<_\1\2</_\3", xml)

root = ET.fromstring(xml)

print("done")




def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the Database.")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)