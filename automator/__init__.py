import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LIBRARY_DIR = os.path.join(os.path.join(BASE_DIR, 'Library'))
DOWNLOAD_DIR = os.path.join(LIBRARY_DIR, 'Downloads')
MEDIA_DIR = os.path.join(LIBRARY_DIR, 'Media')
SAVED_TORRENTS_DIR = os.path.join(DOWNLOAD_DIR, '_torrent_files')
BASE_URL = "https://nyaa.si"
from automator.utils import read_json
__version__ = "0.10.3"

def get_categories():
    categories = {
        "1": {
            "name": "Anime",
            "sub_cats": {
                "1": "Anime Music Video",
                "2": "English-translated",
                "3": "Non-English-translated",
                "4": "Raw"
            }
        },
        "2": {
            "name": "Audio",
            "sub_cats": {
                "1": "Lossless",
                "2": "Lossy"
            }
        },
        "3": {
            "name": "Literature",
            "sub_cats": {
                "1": "English-translated",
                "2": "Non-English-translated",
                "3": "Raw"
            }
        },
        "4": {
            "name": "Live Action",
            "sub_cats": {
                "1": "English-translated",
                "2": "Idol/Promotional Video",
                "3": "Non-English-translated",
                "4": "Raw"
            }
        },
        "5": {
            "name": "Pictures",
            "sub_cats": {
                "1": "Graphics",
                "2": "Photos"
            }
        },
        "6": {
            "name": "Software",
            "sub_cats": {
                "1": "Applications",
                "2": "Games"
            }
        }
    }
    return categories

ANIME_TO_AUTO_DOWNLOAD, USERS = read_json()