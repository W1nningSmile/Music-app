from pathlib import Path

BASE_DIR = Path(__file__).parent

IMG_RESS_DIR = BASE_DIR / "image_ressources"

SONG_DIR = BASE_DIR / "songs/Album"

UI_DIR = BASE_DIR / "ui"

REQUIRED_FILES = [
    #image_ressources
    IMG_RESS_DIR / "default_cover.jpg", 
    IMG_RESS_DIR / "magnifying-glass-icon.png",
    IMG_RESS_DIR / "Speaker_Icon.png",
    IMG_RESS_DIR / "template.png",

    #ui
    UI_DIR / "album_widget_template.py",
    UI_DIR / "create_album_ui.py",
    UI_DIR / "main_page_ui.py"
]

REQUIRED_FOLDERS = [
    IMG_RESS_DIR,
    SONG_DIR,
    UI_DIR
]