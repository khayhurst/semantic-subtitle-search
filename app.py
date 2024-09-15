import streamlit as st
from src.lib.subtitle_parser import SubtitleParser
from src.lib.database_manager import DatabaseManager
from src.helper.get_video_files import get_video_files
from sentence_transformers import SentenceTransformer

# Initialize the database connection
db_manager = DatabaseManager(
    dbname="postgres",  # Using "postgres" as the database name
    user="admin",
    password="admin123",
    host="postgres",
    port="5432"
)
db_manager.connect()

# Sidebar menu to select between pages
page = st.sidebar.selectbox("Select a Page", ["SRT Parsing", "Query Subtitles"])

if page == "SRT Parsing":
    # SRT Parsing Page
    st.title("SRT File Parser")

    # Input fields for movie or TV show
    media_type = st.selectbox("Select media type", ["movie", "tv_show"])
    title = st.text_input("Enter the title")
    release_year = st.number_input("Enter the release year", min_value=1900, max_value=2100)

    # Video file selection logic
    if media_type == "movie":
        video_files = get_video_files('movie')
        selected_file = st.selectbox("Select the movie file", video_files)
    elif media_type == "tv_show":
        video_files = get_video_files('tv_show')
        selected_file = st.selectbox("Select the episode file", video_files)

    uploaded_file = st.file_uploader("Choose an SRT file", type="srt")

    # Process uploaded file
    if st.button("Upload and Parse Subtitles") and uploaded_file is not None:
                # Insert media (movie or TV show) into the media table with file path
        if media_type == "movie":
            media_id = db_manager.insert_media(title, selected_file, media_type, release_year)
            episode_id = None

        elif media_type == "tv_show":
            media_id = db_manager.insert_media(title, selected_file, media_type, release_year)
            episode_id = db_manager.insert_episode(media_id, season, episode, episode_title)


        # SubtitleParser logic
        parser = SubtitleParser(
            uploaded_file=uploaded_file,
            media_type=media_type,
            db_manager=db_manager,
            media_id=media_id if media_type == "movie" else None,
            episode_id=episode_id if media_type == "tv_show" else None
        )

        decoded_data = parser.detect_encoding()
        parser.parse_subtitles(decoded_data)
        parser.vectorize_and_store()

        st.success(f"Subtitles successfully uploaded and stored for {title}")

elif page == "Query Subtitles":
    # Query Subtitles Page
    st.title("Search Subtitles")

    # Create input elements for the query
    query = st.text_input("Enter your query:")

    # Add a search button and use a container for the results
    if st.button("Search"):
        # Create a container for the results at the bottom of the page
        results_container = st.container()
        
        # Perform the search
        if query:
            # Query vector for searching
            model = SentenceTransformer('all-mpnet-base-v2')
            query_vector = model.encode(query)

            # Perform search on pg_vector with vector similarity
            query_results = db_manager.search_subtitles(query_vector)

            # Display search results in the container
            with results_container:
                st.subheader("Search Results")
                if not query_results.empty:
                    st.write(query_results)
                else:
                    st.write("No results found.")
