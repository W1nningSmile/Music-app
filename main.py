import ui.main_page_ui as main_page_ui
import ui.album_widget_template as album_wdiget_template
import ui.create_album_ui as create_album

from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QDialog, QFileDialog, QMessageBox
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaDevices
from PySide6.QtCore import QUrl

import sys
import json

from pathlib import Path
from PIL import Image, ImageOps #PIL = Pillow



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = main_page_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())

        self.saving_pannel_state = None

        self.ui.label_2.setPixmap(QPixmap("image_ressources/default_cover"))
        self.ui.progressBar.setValue(0)

        self.ui.pushButton_3.clicked.connect(self.toggle_saving_pannel)

        self.audio_player = AudioPlayer()

        self.ui.horizontalSlider.setRange(0,100)
        self.ui.horizontalSlider.valueChanged.connect(self.audio_player.volume_change)
        self.ui.horizontalSlider.setValue(100)

        self.song_queue = []
        self.current_song_index = 0
        
        #anything under here wont load until an album has been selected
        self.cd = None
        self.ui.pushButton_7.clicked.connect(lambda: self.audio_player.start_stop())
    
    def toggle_saving_pannel(self):
        if self.saving_pannel_state is None:
            self.saving_pannel_state = saving_pannel()
        self.saving_pannel_state.show()


        

        


class AlbumFrame(QWidget):
    def __init__(self, Album_name, Artist, Icon, parent=None):
        super().__init__(parent)

        #importing the ui
        self.ui = album_wdiget_template.Ui_Form()
        self.ui.setupUi(self)

        self.setMinimumHeight(80)
        self.setMinimumWidth(420)

        #can modify stuff now
        self.ui.Album_name.setText(Album_name)
        self.ui.Artist_name.setText(Artist)
        self.ui.Album_icon.setPixmap(QPixmap(Icon))

        self.Album_name = Album_name
        self.ui.Album_name.clicked.connect(lambda: album_name_clicked(Album_name))
    
class SongFrame(QWidget):
    def __init__(self, Song_name, Artist, Icon, Album, parent=None):
        super().__init__(parent)

        #importing the ui
        self.ui = album_wdiget_template.Ui_Form()
        self.ui.setupUi(self)

        self.setMinimumHeight(80)
        self.setMinimumWidth(420)

        #can modify stuff now
        self.ui.Album_name.setText(Song_name)
        self.ui.Artist_name.setText(f"{Album} by {Artist}")
        self.ui.Album_icon.setPixmap(QPixmap(Icon))
        
        self.ui.Album_name.clicked.connect(lambda: self.album_name_clicked(Song_name, Artist, Album))
    
    def album_name_clicked(self, Song_name, Artist, Album):
        window.audio_player.play((str(f"songs/Album/{Album}/song_list/{Song_name}.mp3")), Song_name, Artist)
        window.song_queue = get_song_list(Album)
        window.current_song_index = window.song_queue.index(Song_name)
        print(f"song queue: {window.song_queue} and index {window.current_song_index} which is '{window.song_queue[window.current_song_index]}'")

class albums():
    def __init__(self, Name="Album", Artist= "Artist", Icon="image_ressources/default_cover"):
        self.Name = Name
        self.Artist = Artist
        self.Icon = Icon
    
    def create_AlbumFrame(self):
        return AlbumFrame(self.Name, self.Artist, self.Icon)

class AudioPlayer():
    def __init__(self):
        
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.start_condition = True
        
        self.audio.setVolume(1) #bc volume should be %

        default_device = QMediaDevices.defaultAudioOutput()
        self.audio.setDevice(default_device)

        self.player.setAudioOutput(self.audio)
        self.player.durationChanged.connect(self.get_duration) #return duration <-- very weird
        self.player.positionChanged.connect(self.update_duration)

    
    def play(self, Source = "", Song_name = "???", Artist = "???"):
        path = Path(Source).resolve()
        print(f"the path is {path}")

        if not path.exists():
            print("Error: Audio file could not be found")
            exit(1)
        
        self.player.setSource(QUrl.fromLocalFile(path)) 
        window.ui.label_6.setText(f'"{Song_name}" by {Artist}')
        self.player.play()

        cd_gif_making(window.cd)

        window.ui.label_2.movie = QMovie("cd_images/gif_output.gif")
        window.ui.label_2.setMovie(window.ui.label_2.movie)
        window.ui.label_2.movie.start()
    
    def get_duration(self, media_duration):
        self.duration = media_duration #in milisec

    
    def update_duration(self, position):
        window.ui.label.setText(f"{(position//1000)//60}:{(position//1000)%60:02d} / {(self.duration//1000)//60}:{(self.duration//1000)%60:02d}")
        window.ui.progressBar.setValue(position/self.duration * 100)
        print(window.ui.progressBar.value(), position, self.duration)
    
    #audio controls
    def start_stop(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
            window.ui.label_2.movie.setPaused(True) #pauses instead of stopping(aka. needing to restart from begging)
            print("pause")
        else:
            self.player.play() 
            window.ui.label_2.movie.setPaused(False)
            print("play")
    
    def volume_change(self, value):
        self.audio.setVolume(value/100)

class saving_pannel(QDialog): #dont forget to add the disk cover and gif gen here 
                              #Add gif generation  | check if the user has tweaked with the files + fix them | dont move the selected files but copy them instead? --> apparently this is not how apps usually do it 
                              # only generate the gif once and 1 per album --> should i make it so its generated when a song from that album is played for the first time or when its first added through the menu? (leaning towards 2nd option + checking on startup and before a song is played if the gif exists --> prevents tampering and crashes)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("")
        self.ui = create_album.Ui_Dialog()
        self.ui.setupUi(self)

        self.chosen_name = None
        self.chosen_artist = None
        self.chosen_songs = None
        self.chosen_cover = None

        self.ui.textEdit.textChanged.connect(lambda: self.character_limit(self.ui.textEdit.toPlainText(), 106)) #character count > 106 will make it hard to read :/
        self.ui.textEdit_2.textChanged.connect(lambda: self.character_limit(self.ui.textEdit.toPlainText(), 106))

        self.ui.pushButton.clicked.connect(lambda: self.single_file_fetch("Choose cover"))
        self.ui.pushButton_2.clicked.connect(lambda: self.multi_file_fetch("Choose songs"))
        #self.ui.label_5.setText(f"{len(self.chosen_songs)} chosen")

        #ok and cancel buttons
        self.ui.pushButton_3.clicked.connect(lambda: self.create_album()) #ok button
        self.ui.pushButton_4.clicked.connect(lambda: self.close()) #cancel button
    
    def character_limit(self, string, limit): 
        if len(string) > limit:
            self.ui.textEdit.setPlainText(string[:limit])
    
    def single_file_fetch(self,caption_): #cover
        file_name, _ = QFileDialog.getOpenFileName(
            parent=None,
            caption = caption_,
            filter="Image Files (*.png)" #add more filters later and turn them all to png
        )
        if file_name:
            self.chosen_cover = file_name
            self.ui.label_6.setText(f"{Path(file_name).name} chosen")
            self.ui.label_7.setPixmap(QPixmap(Path(file_name)))
        print(Path(file_name).name)

        
    def multi_file_fetch(self,caption_): #songs
        file_name, _ = QFileDialog.getOpenFileNames(
            parent=None,
            caption = caption_,
            filter="Image Files (*.mp3)" #add more filters later and turn them all to png
        )
        if file_name:
            self.chosen_songs = file_name
            count = ["", "was"]
            file_count = len(file_name)
            if file_count > 1:
                count = ["s","were"]
            self.ui.label_5.setText(f"{file_count} file{count[0]} {count[1]} chosen")
        print(file_name)
    
    def create_album(self):
        self.chosen_name = self.ui.textEdit.toPlainText()
        self.chosen_artist = self.ui.textEdit_2.toPlainText()
        print(self.chosen_name)

        if self.chosen_name == "" or self.chosen_cover == None or self.chosen_songs == None or self.chosen_artist == None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Error: Please fill out and/or everything that was requested.")
            msg.setWindowTitle("Error message")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        
        else:
            folder = Path(f"songs/Album/{self.chosen_name}")
            folder.mkdir(parents = True, exist_ok = True)

            Path(f"{folder}/song_list").mkdir(parents = True, exist_ok = True)
            Path(self.chosen_cover).rename(f"{folder}/cover.png") 

            Path(f"{folder}/info.txt").touch() 
            with open(f"{folder}/info.txt", "a") as f:
                f.write(json.dumps(dict(Artist =self.chosen_artist)))

            for songs in self.chosen_songs:
                Path(songs).rename(f"songs/Album/{self.chosen_name}/song_list/{Path(songs).name}")
            
            self.close()

        
    def close(self):
        self.hide()

            
        




def album_name_clicked(Album_name):
        clear_layout(window.ui.verticalLayout_15)
        try:
            window.cd = cd_making(f"songs/Album/{Album_name}/cover")
        except FileNotFoundError:
            pass
        show_songs(Album_name)

def cd_making(photo_path): #find a way to make it more efficient -> rotate a widget maybe? / add cache to not regenerate gif every click
    template_path = "cd_images/template.png" #move the cd png and gif to be generated automatically when user adds a new album -> easier on script when using it
    output_path = "cd_images/test_cd.png"


    template = Image.open(template_path).convert("RGBA")
    for ext in [".png", ".jpg"]:
        fodder = Path(photo_path).with_suffix(ext)
        if fodder.exists():
            break
    photo = Image.open(fodder).convert("RGBA")

    squared_photo = ImageOps.fit(photo, (736, 736), Image.Resampling.LANCZOS)
    final_disc = Image.alpha_composite(squared_photo, template)

    #creates a white underlayer to hide the black background
    white_bg = Image.new("RGBA", final_disc.size, (255,255,255,255))
    disc_on_white = Image.alpha_composite(white_bg, final_disc)

    final_disc.save(output_path, "PNG")
    print(f"Saving to {output_path} succeeded")

    return final_disc

def cd_gif_making(final_disc):
    frames = []

    for ang in range(0,360, 4):
        rotated_frame = final_disc.rotate(-ang, resample=Image.Resampling.BILINEAR, fillcolor=(255,255,255,255)) #bilinear is faster than cubic
        frames.append(rotated_frame.convert("P", palette=Image.Palette.ADAPTIVE)) #aparently makes the gif size tiny while barely sacrificing quality

    frames[0].save(
        "cd_images/gif_output.gif", #gif output path
        save_all = True,
        append_images=frames[1:], #dont take frame 0 or else we will have 2 at angle 0
        duration =45,
        loop=0, #inf loop
        optimize = True,
        disposal=2 #clears previous frames 
    )




def album_info(album_name):
    with open(f"songs/Album/{album_name}/info.txt", "rt") as file:
        info_dump = json.loads(file.read())
    return info_dump

def show_songs(album):
    print(album)
    song_list = get_song_list(album)

    for i in range(len(song_list)):
        window.ui.verticalLayout_15.insertWidget(i, SongFrame(song_list[i], album_info(album)["Artist"], Path(f"songs/Album/{album}/cover"), album))
    window.ui.label_2.setPixmap(QPixmap(f"cd_images/test_cd.png"))
    print(window.song_queue)
def get_song_list(album):
    #use to make queue?
    song_list = []

    for item in Path(f"songs/Album/{album}/song_list").iterdir():
        song_list.append((item.stem))

    print(song_list)
    return song_list

def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window  = MainWindow()

    songs = []

    directory = "songs/Album/"

    album_list = []
    for item in Path("songs/Album/").iterdir():
        album_list.append(item.stem)
        songs.append(albums(item.stem, album_info(item.stem)["Artist"], f"{item}/cover"))
        print(item.stem)
    
    for i in range(len(songs)):
        window.ui.verticalLayout_13.insertWidget(i, songs[i].create_AlbumFrame())
        pass




    window.show()
    sys.exit(app.exec())