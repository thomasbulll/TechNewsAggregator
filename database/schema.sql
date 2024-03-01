DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS sites;

-- Create the 'sites' table
CREATE TABLE sites (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  site_url TEXT NOT NULL
);

-- Create the 'articles' table with a foreign key reference to 'sites'
CREATE TABLE articles (
  id INTEGER PRIMARY KEY NOT NULL,
  site_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  title_url TEXT NOT NULL,
  sentiment INTEGER NOT NULL DEFAULT 0.0,
  CONSTRAINT fk_site_id FOREIGN KEY (site_id) REFERENCES sites(id)
);