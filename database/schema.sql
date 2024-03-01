DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS sites;

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
  sentiment TEXT NOT NULL,
  site_id INTEGER NOT NULL,
  FOREIGN KEY (site_id) REFERENCES sites(id)
);