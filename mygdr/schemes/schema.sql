DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  ncorrect INTEGER DEFAULT 0,
  permission INTEGER NOT NULL DEFAULT 0,
  rewards_id INTEGER,
  FOREIGN KEY (rewards_id) REFERENCES rewards (id)
);

DROP TABLE IF EXISTS rewards;

CREATE TABLE rewards (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT,
  path_to TEXT UNIQUE,
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


