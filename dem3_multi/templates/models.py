class Model:
    pass

class User:
    __slots__ = ["username", "games"]

class Game(Model):
    __slots__ = ["name", "players"]