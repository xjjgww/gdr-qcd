DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  permission INTEGER NOT NULL DEFAULT 0
);
INSERT INTO user (username) VALUES ('Guest');

DROP TABLE IF EXISTS rewards;

CREATE TABLE rewards (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT,
  path_to TEXT,
  assign_to INTEGER,
  FOREIGN KEY (assign_to) REFERENCES user (id)
);

DROP TABLE IF EXISTS questions;

CREATE TABLE questions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question TEXT,
  option_a TEXT,
  option_b TEXT,
  option_c TEXT,
  answer INTEGER
);

