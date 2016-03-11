CREATE TABLE player(
  id BIGINT PRIMARY KEY,
  username TEXT,
  main BOOLEAN
);

CREATE TABLE match(
  id BIGINT PRIMARY KEY,
  version TEXT,
  start TIMESTAMP,
  type TEXT,
  queue_type TEXT
);

CREATE TABLE player_match(
  player_id BIGINT REFERENCES player(id),
  match_id BIGINT REFERENCES match(id),
  champion_id INT,
  kills INT,
  deaths INT,
  assists into
);