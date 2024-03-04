DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS sites;
DROP TABLE IF EXISTS users;

-- Create the 'sites' table
CREATE TABLE sites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_title TEXT NOT NULL,
    site_url TEXT NOT NULL
);

-- Create the 'articles' table with a foreign key reference to 'sites'
CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_title TEXT NOT NULL,
    article_hash BLOB NOT NULL UNIQUE,
    article_url TEXT NOT NULL,
    sentiment TEXT NOT NULL, -- No decimal in sqlite
    site_id INTEGER NOT NULL,
    FOREIGN KEY (site_id) REFERENCES sites(id)
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash BLOB NOT NULL
);
