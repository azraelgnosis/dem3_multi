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
    pass

class Player:
    __slots__ = ["username", "password", "games"]

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self): return f"{self.username}"
        

class Character:
    __slots__ = ["name", "game"]

class Game(Model):
    __slots__ = ["name", "players"]