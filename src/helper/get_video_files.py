import os

def get_video_files(media_type):
    """Recursively scan /media/movie or /media/tv_show for video files."""
    base_path = f"/media/{media_type}"
    video_extensions = ['.mp4', '.mkv', '.avi', '.mov']
    video_files = []

    # Walk through the directory and get all video files
    for root, _, files in os.walk(base_path):
        for file in files:
            if any(file.endswith(ext) for ext in video_extensions):
                # Store the relative path
                relative_path = os.path.relpath(os.path.join(root, file), base_path)
                video_files.append(relative_path)

    return video_files
