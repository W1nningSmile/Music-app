import ui.main_page_ui as main_page_ui
import ui.album_widget_template as album_wdiget_template
import ui.create_album_ui as create_album

from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QDialog, QFileDialog, QMessageBox
from PySide6.QtGui import QPixmap, QMovie, QFont
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
        self.album_frame = {}
        

        self.ui.label_2.setPixmap(QPixmap("image_ressources/default_cover"))

        self.ui.pushButton_3.clicked.connect(self.toggle_saving_pannel)

        self.ui.pushButton_6.clicked.connect(lambda: self.change_position_queue(1))
        self.ui.pushButton_8.clicked.connect(lambda: self.change_position_queue(-1))
        self.ui.pushButton_5.clicked.connect(self.repeat)

        self.ui.label_3.setText(f"Queue: ")
        self.ui.label_3.setFont(QFont("MS Shell Dlg 2", 16))

        #self.ui.lineEdit.returnPressed.connect(self.album_search) #works by pressing enter
        self.ui.lineEdit.textEdited.connect(self.album_search) #works by just typing (no need to press anything) <-- lowkey better icl

        self.audio_player = AudioPlayer()

        self.ui.horizontalSlider.setRange(0,100)
        self.ui.horizontalSlider.valueChanged.connect(self.audio_player.volume_change)
        self.ui.horizontalSlider.setValue(100)

        self.user_active = False #to block updates for Hslider_2

        self.ui.horizontalSlider_2.setRange(0,1000)
        self.ui.horizontalSlider_2.sliderReleased.connect(lambda : self.release_slider_2()) #sliderReleased only calls a function, it  doesnt return anything #window.ui.label_2.movie.setPaused(False)
        self.ui.horizontalSlider_2.sliderPressed.connect(lambda: self.user_activity_state())
        self.ui.horizontalSlider_2.setValue(0)

        self.song_queue = []
        self.current_song_index = 0

        self.song_base = dict()
        
        #anything under here wont load until an album has been selected
        self.ui.pushButton_7.clicked.connect(lambda: self.audio_player.start_stop())
    
    def repeat(self):
        if not self.audio_player.repeat:
            self.audio_player.repeat = True
            self.ui.pushButton_5.setFlat(True)
        else: 
            self.audio_player.repeat = False
            self.ui.pushButton_5.setFlat(False)
    
    def change_position_queue(self, displacement):
        if self.audio_player.current_index  + displacement < 0:
            displacement = 0
        
        self.audio_player.status_change("signal", displacement)
        print(displacement, self.audio_player.current_index)


        

    def release_slider_2(self):
        print("released")
        self.audio_player.change_music_position(self.ui.horizontalSlider_2.value())
        self.user_active = False
        self.audio_player.player.play()
        window.ui.label_2.movie.setPaused(False)
    
    def user_activity_state(self):
        self.audio_player.player.pause()
        self.ui.label_2.movie.setPaused(True)
        self.user_active = True
    
    def album_search(self):
        search = self.ui.lineEdit.text()
        for key, item in self.album_frame.items(): #adding 2 variables in the for  loop bc .items() returns 2 values <-- lowkey forgot abt being able to do this
            if len(key) < len(search): #otherwise it will make an index error
                key = key + " "
            if search.lower() != key[:len(search)].lower():
                item.hide()
            else:
                item.show()
    
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
    
    def album_name_clicked(self, Song_name, Artist, Album): #change this a bit later --> its kinda slowing down other stuff and hogging the way (fixed?)
        window.ui.label_6.setText(f'"{Song_name}" by {Artist}')
        window.audio_player.play((str(f"songs/Album/{Album}/song_list/{Song_name}.mp3")), Song_name, Artist, Album)
        window.song_queue = get_song_list(Album)
        window.current_song_index = window.song_queue.index(Song_name)
        print(f"song queue: {window.song_queue} and index {window.current_song_index} which is '{window.song_queue[window.current_song_index]}'")

class albums():
    def __init__(self, Name="Album", Artist= "Artist", Icon="image_ressources/default_cover"):
        self.Name = Name
        self.Artist = Artist
        if Path(Icon+".png").exists() or Path(Icon+".jpg").exists():
            self.Icon = Icon
        else: 
            self.Icon = "image_ressources/default_cover"
    
    def create_AlbumFrame(self):
        return AlbumFrame(self.Name, self.Artist, self.Icon)

class AudioPlayer():
    def __init__(self):
        
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.start_condition = True
        self.duration = 0

        self.Album = None
        self.Song = None
        self.Artist = None
        
        self.audio.setVolume(1) #bc volume should be %

        self.current_index = 0
        self.repeat = False

        default_device = QMediaDevices.defaultAudioOutput()
        self.audio.setDevice(default_device)

        self.player.setAudioOutput(self.audio)
        self.player.durationChanged.connect(self.get_duration) #return duration <-- very weird
        self.player.positionChanged.connect(self.update_duration)
        self.player.mediaStatusChanged.connect(self.status_change) #goat: https://stackoverflow.com/questions/67752696/pyqt5-mediaplayer-how-to-get-if-the-video-ended
    
    def status_change(self, status, displacement = 1):
        if status == QMediaPlayer.EndOfMedia or status == "signal":
            print(f"song: '{self.Song}' ended", self.Album)
            print(self.current_index)
            arr = window.song_base[self.Album]

            if self.repeat:
                displacement = 0
            
            try:
                self.Song = arr[self.current_index+displacement]
            except IndexError:
                print("index error")
                self.player.stop()
                window.ui.label_2.movie.stop()
                return

            window.ui.label_6.setText(f'"{self.Song}" by {self.Artist}') #should i just display the song name?
            self.play(Path(str(f"songs/Album/{self.Album}/song_list/{self.Song}.mp3")), self.Song, self.Artist, self.Album, False)
            self.current_index = window.song_base[self.Album].index(self.Song)



    
    def play(self, Source = "", Song_name = "???", Artist = "???", Album = "???", cond = True): 
        self.Album = Album
        self.Song = Song_name
        self.Artist = Artist
        path = Path(Source).resolve()
        print(f"the path is {path}")

        if not path.exists():
            print("Error: Audio file could not be found")
            msg = QMessageBox
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Audio file could not be found")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        
        self.player.setSource(QUrl.fromLocalFile(path)) 
        self.player.play()

        #cd_gif_making(window.cd)

        if not Path(f"songs/Album/{Album}/disc_gif.gif").exists():
            print("pass yo mama")
            final_cd = cd_making(Album)
            print("ppap")
            cd_gif_making(final_cd, Album)
            print("pass yo")
        
        window.ui.horizontalSlider_2.setValue(0)
        
        if cond:
            window.ui.label_2.movie = QMovie(f"songs/Album/{Album}/disc_gif.gif")
            window.ui.label_2.setMovie(window.ui.label_2.movie)
            window.ui.label_2.movie.start()
    
    def get_duration(self, media_duration):
        self.duration = media_duration #in milisec

    
    def update_duration(self, position):
        if not window.user_active:
            window.ui.label.setText(f"{(position//1000)//60}:{(position//1000)%60:02d} / {(self.duration//1000)//60}:{(self.duration//1000)%60:02d}")
            window.ui.horizontalSlider_2.setValue(int(position/self.duration * 1000))
            print(window.ui.horizontalSlider_2.value(), position, self.duration)
        else:
            self.player.pause()
            #window.ui.label_2.movie.pause()
    
    def change_music_position(self, new_pos):
        print("yo")
        self.player.setPosition(int(new_pos/1000 * self.duration))
    
    #audio controls
    def start_stop(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
            window.ui.label_2.movie.setPaused(True) #pauses instead of stopping(aka. needing to restart from begging)
            window.ui.pushButton_7.setFlat(True)
            print("pause")
        else:
            self.player.play() 
            window.ui.label_2.movie.setPaused(False)
            window.ui.pushButton_7.setFlat(False)
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

            #gif saving <-- leave this always at end bc it will freeze the app for 1-2 seconds
            self.cd = cd_making(self.chosen_name) #f"songs\Album\{self.chosen_name}\cover.jpg"
            cd_gif_making(self.cd, self.chosen_name)

            show_albums(False, self.chosen_name)
            
            self.close()

        
    def close(self):
        self.hide()

            
        




def album_name_clicked(Album_name):
        window.ui.label_3.setText(f"Queue: {Album_name}")
        clear_layout(window.ui.verticalLayout_15)
        if not Path(f"songs\Album\{Album_name}\disc.png").exists():
            try:
                cd_making(Album_name)
            except FileNotFoundError:
                pass
        show_songs(Album_name)

def cd_making(Album): #find a way to make it more efficient -> rotate a widget maybe? / add cache to not regenerate gif every click
    template_path = "cd_images/template.png" #move the cd png and gif to be generated automatically when user adds a new album -> easier on script when using it
    output_path = f"songs\Album\{Album}\disc.png"


    template = Image.open(template_path).convert("RGBA")
    for ext in [".png", ".jpg"]:
        fodder = Path(f"songs\Album\{Album}\cover").with_suffix(ext)
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

def cd_gif_making(final_disc, Album):
    frames = []

    for ang in range(0,360, 4):
        rotated_frame = final_disc.rotate(-ang, resample=Image.Resampling.BILINEAR, fillcolor=(255,255,255,255)) #bilinear is faster than cubic
        frames.append(rotated_frame.convert("P", palette=Image.Palette.ADAPTIVE)) #aparently makes the gif size tiny while barely sacrificing quality

    frames[0].save(
        f"songs\Album\{Album}\disc_gif.gif", #gif output path
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
    
    if not window.audio_player.player.source().isValid(): #checks if there is any media playing on qmediaplayer rn --> isPlaying() only checked if it was currently running (pausing meant that it wasnt running)
        window.ui.label_2.setPixmap(QPixmap(f"songs\Album\{album}\disc.png"))
    
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

#def show_albums(condition = False): #make dictionnary here --> make super efficient for the fucks of it
#    clear_layout(window.ui.verticalLayout_13)
#    window.ui.verticalLayout_13.addStretch()
#    songs = []
#    album_list = dict()
#
#    for item in Path("songs/Album/").iterdir():
#        album_list[item.stem] = None
#        songs.append(albums(item.stem, album_info(item.stem)["Artist"], f"{item}/cover"))
#    
#    if condition:
#        pass
#    elif not condition:
#        window.song_base = album_list
#    
#    for i in range(len(songs)):
#        window.ui.verticalLayout_13.insertWidget(i, songs[i].create_AlbumFrame())
#        pass

def show_albums(condition = True, Album = None): #make dictionnary here --> make super efficient for the fucks of it (maybe add a refresh button later to bypass this system?)
    if condition:
        for item in Path("songs/Album/").iterdir():
            window.song_base[item.stem] = None
            frame = albums(item.stem, album_info(item.stem)["Artist"], f"{item}/cover").create_AlbumFrame()
            window.album_frame[item.stem] = frame      #key = album name | value = [album name, Artist name, location of cover image]
            window.ui.verticalLayout_13.insertWidget(window.ui.verticalLayout_13.count()-1, frame)
        
        for i in window.song_base.keys():
            window.song_base[i] = list(item.stem for item in Path(f"songs/Album/{i}/song_list").iterdir()) #now song_base has a dictionnary with every song 
        print("the song base is \n",window.song_base)
    else:
        path = Path(f"songs/Album/{Album}").iterdir()
        window.song_base[Album] = list(item.stem for item in Path(f"songs/Album/{Album}/song_list").iterdir())
        frame = albums(item.stem, album_info(item.stem)["Artist"], f"{item}/cover").create_AlbumFrame()
        window.album_frame[item.stem] = frame
        window.ui.verticalLayout_13.insertWidget(window.ui.verticalLayout_13.count()-1, frame)
        print("the song base is \n",window.song_base)
        




if __name__ == "__main__":
    app = QApplication(sys.argv)

    window  = MainWindow()

    show_albums()
    



    window.show()
    sys.exit(app.exec())