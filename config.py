from pathlib import Path
import sys

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

IMG_RESS_DIR = BASE_DIR / "image_ressources"
SONG_DIR = BASE_DIR / "songs" / "Album"

REQUIRED_FOLDERS = [
    IMG_RESS_DIR,
    SONG_DIR,
]