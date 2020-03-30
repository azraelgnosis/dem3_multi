class Model:
    pass

class Player:
    __slots__ = ["username", "games"]

class Character:
    __slots__ = ["name", "game"]

class Game(Model):
    __slots__ = ["name", "players"]