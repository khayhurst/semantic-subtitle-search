import psycopg2
import pandas as pd

class DatabaseManager:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    def connect(self):
        """Connect to the PostgreSQL database"""
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        return self.conn

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()

    def generate_media_path(self, media_type, file_name):
        """Generate the file path based on media type and file name"""
        if media_type == "movie":
            return f"/media/movie/{file_name}"
        elif media_type == "tv_show":
            return f"/media/tv_show/{file_name}"

    def insert_media(self, title, file_name, media_type, release_year):
        """Insert media into the media table with a media path"""
        media_path = self.generate_media_path(media_type, file_name)
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO media (title, media_type, release_year, media_path)
                VALUES (%s, %s, %s, %s) RETURNING id;
            """, (title, media_type, release_year, media_path))
            media_id = cursor.fetchone()[0]
            self.conn.commit()
            return media_id
        except psycopg2.Error as e:
            self.conn.rollback()  # Rollback in case of error
            print(f"Error inserting media: {e}")
            return None
        finally:
            cursor.close()

    def insert_episode(self, media_id, season, episode, title=None):
        """Insert an episode for a TV show and return the episode_id"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO episodes (media_id, season, episode, title)
            VALUES (%s, %s, %s, %s) RETURNING id;
        """, (media_id, season, episode, title))
        episode_id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return episode_id

    def insert_subtitle(self, episode_id, media_id, start_time, end_time, text, vector):
        """Insert subtitle data into the subtitles table"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO subtitles (episode_id, media_id, start_time, end_time, text, vector)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (episode_id, media_id, start_time, end_time, text, vector))
        self.conn.commit()  # Ensure the commit is called
        cursor.close()

    def search_subtitles(self, query_vector, top_n=10):
        """Perform a vector similarity search on the subtitles using pg_vector."""
        cursor = self.conn.cursor()

        # Convert the query vector to a proper string representation with brackets
        query_vector_str = "[" + ",".join(map(str, query_vector)) + "]"

        # SQL query to find the closest matches
        cursor.execute(f"""
            SELECT subtitles.text, media.title, subtitles.start_time, subtitles.end_time, media.media_type, 
                1 - (subtitles.vector <=> '{query_vector_str}'::vector) AS similarity_score
            FROM subtitles
            JOIN media ON media.id = subtitles.media_id
            ORDER BY subtitles.vector <=> '{query_vector_str}'::vector
            LIMIT %s;
        """, (top_n,))

        # Fetch results and create a DataFrame
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=['Subtitle', 'Media Title', 'Start Time', 'End Time', 'Media Type', 'Similarity Score'])

        cursor.close()
        return df
