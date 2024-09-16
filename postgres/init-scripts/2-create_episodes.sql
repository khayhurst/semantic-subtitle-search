-- Table to store information about individual episodes for TV shows
CREATE TABLE IF NOT EXISTS episodes (
    id SERIAL PRIMARY KEY,
    media_id INT NOT NULL,
    season INT NOT NULL,
    episode INT NOT NULL,
    title TEXT,
    FOREIGN KEY (media_id) REFERENCES media(id) ON DELETE CASCADE
);
