import os

from utils.folder_file_manager import make_directory_if_not_exists


CUR_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = make_directory_if_not_exists(os.path.join(CUR_DIR, 'output'))
UPLOAD_DIR = make_directory_if_not_exists(os.path.join(CUR_DIR, 'upload'))
BOTTOM_PADDING = 20

LOCAL = True

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000
