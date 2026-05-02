DROP TABLE IF EXISTS leaderboard;

CREATE TABLE leaderboard (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    score INTEGER NOT NULL,
    level INTEGER NOT NULL,
    date DATE DEFAULT CURRENT_DATE
);