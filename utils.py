import os


def ensure_folder_exists(folder_path):
    """Ensure the specified folder exists."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)