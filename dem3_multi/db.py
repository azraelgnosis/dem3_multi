import click
from flask import (
    current_app, g
)
from flask.cli import with_appcontext
import sqlite3
from werkzeug.security import generate_password_hash

from dem3_multi.models import Game, Row, Table, User

map_table_class = {
    'games': Game,
    'tables': Table,
    'users': User,
}

def get_db() -> sqlite3.Connection:
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = Row

    return g.db

#? Might be expanded with Where and Join objects
def select(table:str, columns:list=["*"], id:int=None, name:str=None, datatype=True) -> list:
    """
    SELECT `columns` FROM `table`
        [WHERE `table`.id = `id`]
        [WHERE `table`.name = `name`]

    Returns a list of the results.
    """

    db = get_db()

    columns_str = ", ".join([f"{table}.{column}" for column in columns])
    query = f"SELECT {columns_str} FROM {table}"

    if id:
        query += f" WHERE {table}.id = {id}"
    elif name:
        query += f' WHERE {table}.name = "{name}"'

    results = db.execute(query).fetchall()

    Class = map_table_class.get(table)
    if datatype is True and Class and columns==['*']:
        results = [Class.from_row(row) for row in results]

    return results

#? def insert(table:Str, *vales):
def insert(table:str, values:list=[]) -> None:
    """INSERT INTO `table` VALUES (NULL, `values`);"""

    db = get_db()
    placeholders = ", ".join("?" * len(values))
    query = f"INSERT INTO {table} VALUES (NULL, {placeholders})"
    db.execute(query, (values)) # join requires strings as arguments
    db.commit()

def update(table:str, set:dict, where=None) -> None:
    """
    UPDATE `table`
        SET `mapping`
        [WHERE `table`.id = `id]
        [WHERE `table`.name = `name`]
    """

    SET = ", ".join(f"{key} = {val}" for key, val in set.items())

    WHERE = "WHERE "

    if isinstance(where, int):
        WHERE += f"{table}.id = ?"
    else:
        WHERE += f"{table}.name = ?"

    query = f"UPDATE {table} SET {SET} WHERE {WHERE}"

    get_db().execute(query, (where,))

def get_user(user_info) -> User:
    """
    Retrieve user from database if present.

    Returns `User` object.
    """

    db = get_db()

    query = """
        SELECT users.id, users.username, users.password, roles.name AS role, games.name AS game
            FROM users
            LEFT JOIN map_users_roles AS map_role ON map_role.user_id = users.id
            LEFT JOIN roles ON map_role.role_id = roles.id
            LEFT JOIN map_users_games AS map_game ON map_game.user_id = users.id
            LEFT JOIN games ON map_game.game_id = games.id
        """

    if isinstance(user_info, int):
        query += " WHERE users.id = ?"
    elif isinstance(user_info, str):
        query += " WHERE users.username = ?"

    user_data = db.execute(query, (user_info,)).fetchall()

    try:
        user = User(user_data[0]['id'], user_data[0]['username'], user_data[0]['password'])
        for row in user_data:
            user.add_role(row.role) if row.role else None
            user.add_game(row.game) if row.game else None
    except AttributeError:
        user = None

    return user

def get_usernames() -> list:
    """Select usernames from `users` table and returns them as a list."""
    
    db = get_db()

    query = "SELECT users.username FROM users"

    usernames = db.execute(query).fetchall()
    usernames = [row.username for row in usernames]

    return usernames

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
            role_name=role_name, username=select('users', ['username'], id=user_id) # role_name=role_name, username=get_username(user_id)
        ))

        role_id = select('roles', columns=['id'], name=role_name, datatype=False)[0]['id'] #get_role_id(role_name)
        insert('map_users_roles', values=[user_id, role_id]) 

        db.commit()

def get_games(user_id:int='NULL') -> list:
    db = get_db()

    query = """SELECT games.id, games.name, games.country, map.user_id FROM games 
                LEFT JOIN 
                    (SELECT user_id, game_id FROM map_users_games 
                        WHERE user_id = ?) 
                    AS map on map.game_id = games.id
                """

    results = db.execute(query, (user_id,)).fetchall()

    return results

def get_tables() -> list:
    db = get_db()

    tables = db.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    tables = [Table(table['name'], db) for table in tables[1:]]

    return tables

def get_table(name:str) -> Table:
    """
    Selects everything from `table`.

    Returns Table object.
    """
    db = get_db()
    table = Table(name, db)
    table.rows = select(name)

    return table

def close_db(e=None): 
    if db := g.pop('db', None):
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    root_init()    

# heroku run python -m flask init-db
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the Database.")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

@with_appcontext
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
        insert('users', values=['root', generate_password_hash('toor')]) #! add_user("root", generate_password_hash("toor"))
        add_user_role(1, "admin")
