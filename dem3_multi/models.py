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
    @classmethod
    def from_row(cls, row:Row):
        new_obj = cls()

        for key in row.keys():
            setattr(new_obj, key, row[key]) #? Do Row objects have __getitem__?

class User(Model):
    __slots__ = ["id", "username", "password", "games"]

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def from_row(row:Row) -> 'User':
        return User(row.id, row.username, row.password)

    def __repr__(self): return f"{self.username}"
        

class Character:
    __slots__ = ["name", "game"]

class Game(Model):
    __slots__ = ["name", "users"]