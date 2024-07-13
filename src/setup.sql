-- database: ./db.sqlite
-- Use the ▷ button in the top right corner to run the entire file.
CREATE TABLE
    authors (
        name TEXT PRIMARY KEY
    );

CREATE TABLE
    books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        author_name TEXT,
        FOREIGN KEY (author_name) REFERENCES authors (name)
    );