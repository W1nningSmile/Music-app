from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap
from pathlib import Path
import json
import ui.album_widget_template as album_widget_template

albums = ([])

#loading album + info
def load_album_cover(directory,album_name):
    window.label_2.setPixmap(QPixmap(f"{directory}{album_name}/cover.jpg"))
    load_album_songs(directory,album_name)
    window.pushButton_14.setText(album_info(directory,album_name)["Artist"])

def load_album_songs(directory,album_name):
    song_list = ([])
    for item in Path(f"{directory}{album_name}/song_list").iterdir():
        song_list.append(item.name[10:-4])
    
    print(song_list)

def album_info(directory,album_name):
    with open(f"{directory}/{album_name}/info.txt", "rt") as file:
        info_dump = json.loads(file.read())
    return info_dump

class AlbumFrame(QWidget):
    def __init__(self, Album_name="Album", Artist="Artist", Icon=None, parent=None):
        super().__init__(parent)

        #importing the ui
        self.ui = album_widget_template.Ui_Form()
        self.ui.setupUi(self)

        #can modify stuff now
        self.ui.Album_name.setText(Album_name)
        self.ui.Artist_name.setText(Artist)
        self.ui.Album_icon.setPixmap(QPixmap(Icon))

#startup
def storage_on_startup():
    album_list = ([])
    path = 'songs/Album'

    for item in Path(path).iterdir():
        album_list.append(item.name)
    
    for item in album_list:
        album_load(path, item)

def album_load(path, item):
    albums.append(AlbumFrame(item, album_info(path,item)["Artist"], f"{path}/{item}/cover.jpg"))

    


app = QApplication()
loader = QUiLoader()


file = QFile("main_page.ui")
file.open(QFile.ReadOnly)

window = loader.load(file, None)
window.label_4.setPixmap(QPixmap("image_ressources/Speaker_Icon.png"))
window.label_5.setPixmap(QPixmap('image_ressources/magnifying-glass-icon.png'))
window.label_2.setPixmap(QPixmap('image_ressources/default_cover.jpg'))


directory = "songs/Album/"
album_name = "AfterLyfe"

window.label_32.setPixmap(QPixmap(directory +  album_name + "/thumb.jpg"))
window.pushButton_13.setText(album_name)
window.pushButton_14.setText("Artist")

window.pushButton_13.clicked.connect(lambda: load_album_cover(directory,album_name))

file1 = QFile("album_frame.ui")
file1.open(QFile.ReadOnly)

card = loader.load(file1)
file1.close()
window.verticalLayout_13.addWidget(AlbumFrame("Blurryface", "Twenty One Pilots", "songs/Album/Afterlyfe/cover.jpg"))

storage_on_startup()

window.show()
app.exec()