-- Table to store subtitle data with vectorization
CREATE TABLE IF NOT EXISTS subtitles (
    id SERIAL PRIMARY KEY,
    episode_id INT,  -- Nullable because movies won't have episodes
    media_id INT,  -- Nullable because TV shows have episodes
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    text TEXT NOT NULL,
    vector vector(768),  -- Vectorized representation of the subtitle text
    FOREIGN KEY (episode_id) REFERENCES episodes(id) ON DELETE CASCADE,
    FOREIGN KEY (media_id) REFERENCES media(id) ON DELETE CASCADE
);
