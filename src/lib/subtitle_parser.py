import pysrt
import chardet  # Library to detect file encoding
import logging
from sentence_transformers import SentenceTransformer

# Configure logging
logging.basicConfig(level=logging.INFO)

class SubtitleParser:
    def __init__(self, uploaded_file, media_type, db_manager, media_id=None, episode_id=None):
        self.uploaded_file = uploaded_file
        self.media_type = media_type  # 'movie' or 'tv_show'
        self.media_id = media_id  # For movies
        self.episode_id = episode_id  # For TV show episodes
        self.db_manager = db_manager  # DatabaseManager instance
        self.model = SentenceTransformer('all-mpnet-base-v2')  # Vectorizer model

    def detect_encoding(self):
        """Detect file encoding using chardet"""
        raw_data = self.uploaded_file.read()
        result = chardet.detect(raw_data)
        self.encoding = result['encoding']
        logging.info(f"Detected encoding: {self.encoding}")
        return raw_data.decode(self.encoding)

    def parse_subtitles(self, decoded_data):
        """Parse subtitles from the .srt file"""
        self.subtitles = pysrt.from_string(decoded_data)
        logging.info(f"Parsed {len(self.subtitles)} subtitles.")
        return self.subtitles

    @staticmethod
    def convert_time(subrip_time):
        """Convert SubRipTime object to a string format"""
        return f"{subrip_time.hours:02}:{subrip_time.minutes:02}:{subrip_time.seconds:02}.{subrip_time.milliseconds:03}"

    def vectorize_and_store(self):
        """Vectorize subtitles and store them in the database"""
        for subtitle in self.subtitles:
            text = subtitle.text
            vector = self.model.encode(text)  # Vectorize the subtitle text

            try:
                # Insert the subtitle into the database using the DatabaseManager
                self.db_manager.insert_subtitle(
                    episode_id=self.episode_id if self.media_type == 'tv_show' else None,
                    media_id=self.media_id if self.media_type == 'movie' else None,
                    start_time=self.convert_time(subtitle.start),
                    end_time=self.convert_time(subtitle.end),
                    text=text,
                    vector=vector.tolist()  # Convert numpy array to list
                )
                logging.debug(f"Inserted subtitle: {text}")
            except Exception as e:
                logging.error(f"Error inserting subtitle: {text}, Error: {e}")
