import sqlite3

class Row(sqlite3.Row):
    def __init__(self, cursor, values):
        self.cursor = cursor
        self.values = values
        self.columns = [col[0] for col in cursor.description]

        for col, val in zip(self.columns, self.values):
            setattr(self, col, val)

    def __repr__(self): return ", ".join([f"{key}: {self[key]}" for key in self.keys()])

class Model:
    def init(self): ...

    @classmethod
    def from_row(cls, row:Row):
        new_obj = cls()

        for key in row.keys():
            setattr(new_obj, key, row[key])
        
        new_obj.init()

        return new_obj

class Table(Model):
    __slots__ = ["db", "name", "columns", "size", "rows"]

    def __init__(self, name:str, db):
        self.name = name
        self.db = db

        self.columns = []
        self.size = -1
        
        self._set_columns()
        self._set_size()

    # def set_db(self, db:sqlite3.Connection) -> None:
    #     self.db = db

    def _set_columns(self) -> None:
        """
        Retrieves the columns from the database and assigns them to `self.columns` as a list.
        """
        cursor = self.db.execute(f"SELECT * FROM {self.name}")
        self.columns = [col[0] for col in cursor.description]

    def _set_size(self) -> None:
        """
        Retrieves number of rows from database and assigns that to `self.size`
        """

        size = self.db.execute(
                f"SELECT COUNT(*) AS count FROM {self.name}"
            ).fetchone()['count']
        self.size = size

    def __len__(self): return self.size
    def __repr__(self): return f"{self.name}: {', '.join(self.columns)}"

class User(Model):
    __slots__ = ["id", "username", "password", "roles", "games"]

    def __init__(self, id, username, password, roles=set(), games=set()):
        self.id = id
        self.username = username
        self.password = password
        self.roles = roles
        self.games = games

    def add_role(self, role:str):
        self.roles.add(role)

    def add_game(self, game:str):
        self.games.add(game)

    @staticmethod
    def from_row(row:Row) -> 'User':
        return User(row.id, row.username, row.password)

    def __repr__(self): return f"{self.username}"
        

class Character:
    __slots__ = ["name", "game"]

class Game(Model):
    __slots__ = ["name", "country", "users"]

    def init(self): ...


class Save(Model):
    __slots__ = ["date"]