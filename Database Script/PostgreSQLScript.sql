DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255),
    role VARCHAR(255) NOT NULL DEFAULT 'user'
);

DROP TABLE IF EXISTS resumes;

CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    owner_id INTEGER REFERENCES users(id)
);
