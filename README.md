# Subtitle Search Application

A web-based application that allows users to upload subtitle files (`.srt`), vectorize them using a semantic embedding model, store the vectors in a PostgreSQL database, and perform semantic search queries to find relevant subtitles in TV shows and movies. Built with Python, Streamlit, `sentence-transformers`, and PostgreSQL with `pg_vector`.

## Features

- **Subtitle Upload and Parsing**: Upload subtitle files (`.srt`), parse them, and convert each line into semantic vectors.
- **Vector Storage**: Store vectors in a PostgreSQL database using the `pg_vector` extension.
- **Semantic Search**: Perform vector-based semantic search queries to find relevant subtitles using natural language.

## Tech Stack

- **Python**: Core language for the application logic.
- **Streamlit**: Web framework for the user interface.
- **Sentence Transformers**: For creating semantic vectors from subtitles.
- **PostgreSQL with pg_vector**: Database for storing subtitle vectors and performing similarity search.

## Setup and Installation

### Prerequisites

- **Docker**: Used for containerizing the application and its dependencies.
- **Docker Compose**: To orchestrate multi-container Docker applications.

### Step-by-Step Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/khayhurst/subtitle-search-app.git
   cd subtitle-search-app
   ```

2. **Configure Environment Variables**:

   - Ensure that your PostgreSQL credentials and other configurations are set correctly in the `docker-compose.yml` file.

3. **Build and Run the Application**:

   - Use Docker Compose to build and start the containers:

   ```bash
   docker-compose up --build
   ```

4. **Access the Application**:
   - Once the containers are up and running, open your web browser and navigate to:
   ```
   http://localhost:8501
   ```
   - This will open the Streamlit UI where you can upload subtitles and perform search queries.

## How to Use

### Uploading Subtitles

1. Navigate to the **SRT Parsing** page.
2. Select the media type (movie or TV show).
3. Enter the title, release year, and select the appropriate media file.
4. Upload an `.srt` file to parse and store subtitles in the database.

### Searching for Subtitles

1. Navigate to the **Query Subtitles** page.
2. Enter your search query in natural language and press the "Search" button.
3. View the results, including subtitle text, start and end times, media title, and similarity scores.

## Project Structure

```
subtitle-search-app/
│
├── app.py                      # Main Streamlit application
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Dockerfile for the application
├── src/
│   ├── lib/
│   │   ├── database_manager.py # Database management logic
│   │   ├── subtitle_parser.py  # Subtitle parsing and vectorization logic
│   └── helper/
│       ├── get_video_files.py  # Helper to list video files
├── postgres/
│   ├── vector_extension.sql    # SQL script to set up pg_vector
└── README.md                   # Project README file
```

## Key Code Highlights

### Vectorization of Subtitles

- We use `sentence-transformers` to convert each subtitle line into a semantic vector:
  ```python
  from sentence_transformers import SentenceTransformer
  model = SentenceTransformer('all-mpnet-base-v2')
  vector = model.encode(subtitle_text)
  ```

### Storing Vectors in PostgreSQL

- Subtitle vectors are stored in a PostgreSQL database using the `pg_vector` extension:
  ```python
  def insert_subtitle(self, episode_id, media_id, start_time, end_time, text, vector):
      cursor.execute("""
          INSERT INTO subtitles (episode_id, media_id, start_time, end_time, text, vector)
          VALUES (%s, %s, %s, %s, %s, %s);
      """, (episode_id, media_id, start_time, end_time, text, vector))
  ```

### Performing Vector-Based Search

- Perform a similarity search using PostgreSQL’s `<=>` operator:
  ```python
  cursor.execute(f"""
      SELECT subtitles.text, media.title, subtitles.start_time, subtitles.end_time, media.media_type,
          1 - (subtitles.vector <=> '{query_vector_str}'::vector) AS similarity_score
      FROM subtitles
      JOIN media ON media.id = subtitles.media_id
      ORDER BY subtitles.vector <=> '{query_vector_str}'::vector
      LIMIT %s;
  """, (top_n,))
  ```

## Troubleshooting

- **Cannot connect to PostgreSQL**: Ensure that the PostgreSQL container is running and the credentials in `docker-compose.yml` match your database configuration.
- **pg_vector extension not found**: Make sure the `vector_extension.sql` script is executed when the PostgreSQL container starts.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please open an issue or a pull request for any changes.

## Contact

For any questions or feedback, please contact [kylehayhurst@gmail.com].
