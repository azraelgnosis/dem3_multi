import click
import sqlite3
from flask import current_app, g
from flask.cli import with_appcontext
import os
import re
from werkzeug.security import generate_password_hash
import xml.etree.ElementTree as ET

from dem3_multi.models import (
    Game, Row, User
)
from dem3_multi.game_models import Policy


def get_db() -> sqlite3.Connection:
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = Row

    return g.db

#! Do I actually need this?
def get_users() -> list:
    """
    Select users from database.
    """

    db = get_db()
    query = "SELECT * FROM users"
    users = db.execute(query).fetchall()
    users = [User.from_row(user) for user in users]

    return users

def get_user(username:str) -> User:
    """
    Retrieve user from database if present.
    """

    db = get_db()
    query = "SELECT * FROM users WHERE username = ?"
    user = db.execute(query, (username,)).fetchone()

    try:
        user = User(user.id, user.username, user.password)
    except AttributeError:
        user = None

    return user

def get_username(user_id:int) -> str:
    db = get_db()

    username = db.execute(
        "SELECT users.username FROM users WHERE users.id = ?",
        (user_id,)
    ).fetchone()

    return username.username

def get_usernames() -> list:
    """
    Select usernames from `users` table and return as a list
    """
    db = get_db()

    query = "SELECT users.username FROM users"

    usernames = db.execute(query).fetchall()
    usernames = [row.username for row in usernames]

    return usernames

def add_user(username:str, password:str) -> None:
    """
    Insert username and password into `users` table
    """
    db = get_db()

    query = "INSERT INTO users (username, password) VALUES (?, ?)"
    db.execute(query, (username, password))
    db.commit()

def get_role_id(role_name:str) -> int:
    """
    Retrieve the id of the role by name.

    `role_name` is the name of the role as stored in the database.
    """

    db = get_db()

    role = db.execute(
        "SELECT roles.id FROM roles WHERE roles.name = ?", (role_name,)
    ).fetchone()

    return role.id

def add_user_role(user_id:int, role_name:str) -> None:
    """
    Add a role to a user.
    """
    
    db = get_db()

    check_user_role = db.execute(
        "SELECT map.user_id, map.role_id, roles.name FROM map_users_roles AS map " \
            "LEFT JOIN roles ON roles.id = map.role_id " \
            "WHERE map.user_id = ? AND roles.name = ?", (user_id, role_name)
        ).fetchone()

    if not check_user_role:
        print("Adding role '{role_name}' to '{username}'".format(
            role_name=role_name, username=get_username(user_id)
        ))

        role_id = get_role_id(role_name)
        db.execute(
            "INSERT INTO map_users_roles " \
                "(user_id, role_id) VALUES (?, ?);", (user_id, role_id)
        )

        db.commit()

def get_games() -> list:
    """
    """
    db = get_db()
    query = "SELECT * FROM games"
    games = db.execute(query).fetchall()
    games = [Game.from_row(game) for game in games if game]

    return games

def get_game(id:int) -> Game:
    """
    Return Game based on id
    """
    db = get_db()
    query = "SELECT * FROM games WHERE id = ?"
    game = db.execute(query, (id,)).fetchone()
    game = Game.from_row(game)
    return game

#TODO
def load_save_file(filename:str="test3.xml") -> ET.Element:
    """
    """

    if 'save' not in g:
        save_path = r"C:\Users\root\Documents\My Games\democracy3\savegames"

        with open(os.path.join(save_path, filename), "r") as f:
            xml = f.read()

        xml = "<xml>\n" + xml # add opening <xml> tag to complement end tag

        # replaces <0>...</0> with <_0>...</_0> and <0_hist>...</0_hist> with <_0_hist>...</_0_hist>
        xml = re.sub(r"<(\d{1,2}(?:_hist)?>)(.*)</(\d{1,2}(?:_hist)?>)", r"<_\1\2</_\3", xml)

        root = ET.fromstring(xml)

        g.save = root
    
    return g.save


def get_policies() -> list:
    game = load_save_file()

    policies = game.find(".//policies")
    policies = [Policy.from_xml(policy) for policy in policies.iter('policy')]

    return policies

def get_policy(policy_name:str) -> Policy:
    """
    Finds and returns the specified Policy object.

    `policy_name`: Name of the policy being retrieved.

    Return the Policy object matching `policy_name`.
    """
    policies = get_policies()
    policy = next(filter(lambda p: p.name == policy_name, policies))

    return policy



def close_db(e=None): 
    if db := g.pop('db', None):
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    root_init()    

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the Database.")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def root_init():
    """
    Add root admin account.
    """

    db = get_db()

    check_root = db.execute(
        "SELECT * FROM users WHERE users.username == ?",
        ('root',)
    ).fetchone()

    if not check_root:
        add_user("root", generate_password_hash("toor"))
        add_user_role(1, "admin")
        # db.execute(
        #     "INSERT INTO map_users_roles (user_id, role_id) " \
        #         "VALUES (1, 1)"
        # )