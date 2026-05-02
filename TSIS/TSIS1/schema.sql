DROP TABLE IF EXISTS phones CASCADE;
DROP TABLE IF EXISTS phonebook CASCADE;
DROP TABLE IF EXISTS groups CASCADE;

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO groups (name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other');

CREATE TABLE phonebook (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    birthday DATE,
    group_id INTEGER REFERENCES groups(id)
);

CREATE TABLE phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES phonebook(id) ON DELETE CASCADE,
    phone VARCHAR(20) UNIQUE NOT NULL,
    type VARCHAR(10) CHECK (type IN ('home','work','mobile'))
);