from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QPixmap
import ui.album_widget_template as album_widget_template

class AlbumFrame(QWidget):
    def __init__(self, Album_name="Album", Artist="Artist", Icon=None, parent=None):
        super().__init__(parent)

        #importing the ui
        self.ui = album_widget_template.Ui_Form()
        self.ui.setupUi(self)

        #can modify stuff now
        self.ui.Album_name = Album_name
        self.ui.Artist_name = Artist
        self.ui.Album_icon.setPixmap(QPixmap(Icon))