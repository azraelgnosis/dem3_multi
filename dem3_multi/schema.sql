DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS map_users_games;

CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    game INTEGER NOT NULL
    FOREIGN KEY (game) REFERENCES games (id)
)

CREATE TABLE games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country TEXT NOT NULL
);

CREATE TABLE map_users_games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user INTEGER NOT NULL,
    game INTEGER NOT NULL,
    FOREIGN KEY (user) REFERENCES users (id),
    FOREIGN KEY (game) REFERENCES games (id)
);