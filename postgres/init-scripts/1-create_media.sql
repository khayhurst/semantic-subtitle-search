-- Table to store information about movies and TV shows
CREATE TABLE IF NOT EXISTS media (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    media_type TEXT CHECK (media_type IN ('movie', 'tv_show')),  -- Either 'movie' or 'tv_show'
    release_year INT,
    media_path TEXT
);
