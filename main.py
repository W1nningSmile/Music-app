import ui.main_page_1400x800 as main_page_ui
import ui.album_frame_1400x800 as album_wdiget_template
import ui.create_album_ui as create_album

from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QDialog, QFileDialog, QMessageBox, QSpacerItem, QSizePolicy
from PySide6.QtGui import QPixmap, QMovie, QFont
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaDevices
from PySide6.QtCore import QUrl, QTimer

import sys
import json
from random import shuffle

from pathlib import Path
from PIL import Image, ImageOps #PIL = Pillow
import shutil
import gc

import config



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = main_page_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(1400, 800)

        self.saving_pannel_state = None

        self.album_frame = {}

        self.selected_album = None
        self.current_movie = None

        self.ui.label_2.setPixmap(QPixmap("image_ressources/default_cover"))

        self.ui.pushButton_3.clicked.connect(self.toggle_saving_pannel)

        self.ui.pushButton_6.clicked.connect(lambda: self.change_position_queue(1))
        self.ui.pushButton_8.clicked.connect(lambda: self.change_position_queue(-1))
        self.ui.pushButton_5.clicked.connect(self.repeat)

        #self.ui.lineEdit.returnPressed.connect(self.album_search) #works by pressing enter
        self.ui.lineEdit.textEdited.connect(self.album_search) #works by just typing (no need to press anything) <-- lowkey better icl

        self.audio_player = AudioPlayer(self)

        self.ui.horizontalSlider.setRange(0,100)
        self.ui.horizontalSlider.valueChanged.connect(self.audio_player.volume_change)
        self.ui.horizontalSlider.setValue(100)

        self.user_active = False #to block updates for Hslider_2

        self.ui.horizontalSlider_2.setRange(0,1000)
        self.ui.horizontalSlider_2.sliderReleased.connect(lambda : self.release_slider_2()) #sliderReleased only calls a function, it  doesnt return anything #window.ui.label_2.movie.setPaused(False)
        self.ui.horizontalSlider_2.sliderPressed.connect(lambda: self.user_activity_state())
        self.ui.horizontalSlider_2.setValue(0)

        self.ui.pushButton_4.clicked.connect(self.shuffle)

        self.ui.pushButton.clicked.connect(self.delete_album) #delete album

        self.song_queue = [] #not needed?
        self.current_song_index = 0
        self.artist_search_state = 0

        self.song_base = dict() #list of all songs downloaded
        self.artist_base = dict()
        
        #anything under here wont load until an album has been selected
        self.ui.pushButton_7.clicked.connect(lambda: self.audio_player.start_stop())
    
    def artist_search(self, artist):
        #print(self.album_frame)
        if not self.artist_search_state%2:
            for key, value in self.artist_base.items():
                #print(key, value)
                if value != artist:
                    self.album_frame[key].hide()
        else: 
            for key, value in self.artist_base.items():
                #print(key, value)
                if value != artist:
                    self.album_frame[key].show()

        self.artist_search_state+=1


    
    def release_media(self):
        if self.current_movie:
            self.current_movie.stop()
            self.current_movie = None
            self.ui.label_2.clear()
        
        self.audio_player.player.stop()
        self.audio_player.player.setSource(QUrl(""))

        QApplication.processEvents()
        gc.collect() #forces garbage collection instead of waiting for a qt cycle

    def delete_album(self): #fix this (bug where you cant delete an album if its already playing or been played?)
        # self.audio_player.Album <-- current album playing
        if not self.selected_album:
            return
        
        album_path = Path(f"songs/Album/{self.selected_album}")

        if not album_path.exists():
            return
        
        self.release_media()

        if Path("temp_delete.txt").exists():
            with open("temp_delete.txt", "a") as f:
                f.write(f"{self.selected_album}\n")       
        else:
            with open("temp_delete.txt", "w") as f:
                pass 

        
        clear_layout(self.ui.verticalLayout_16)
        self.album_frame.pop(self.selected_album, None)
        self.song_base.pop(self.selected_album, None)
        self.artist_base.pop(self.selected_album, None)

        for album in self.song_base.keys():
            frame = Album(album, album_info(album)["Artist"], (f"songs/Album/{album}/cover")).create_AlbumFrame()
            self.album_frame[album] = frame      #key = album name | value = [album name, Artist name, location of cover image]
            self.ui.verticalLayout_16.insertWidget(self.ui.verticalLayout_16.count()-1, frame)

        self.ui.verticalLayout_16.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    
    def repeat(self):
        if not self.audio_player.repeat:
            self.audio_player.repeat = True
            self.ui.pushButton_5.setFlat(True)
        else: 
            self.audio_player.repeat = False
            self.ui.pushButton_5.setFlat(False)
    
    def shuffle(self): #arr = window.song_base[self.Album]
        try:
            if not self.ui.pushButton_4.isFlat():
                shuffle(self.audio_player.queue)
                self.audio_player.current_index = -1 #index = -1 or else it will also count the current song playing as being part of the new queue
                self.ui.pushButton_4.setFlat(True)
            else: 
                self.audio_player.queue = get_song_list(self.selected_album)
                self.ui.pushButton_4.setFlat(False)
            
            print(self.audio_player.queue)

            
        except AttributeError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Can't shuffle the album or playlist because there isnt anything eligible selected to shuffle.")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()


    
    def change_position_queue(self, displacement):
        if self.audio_player.current_index  + displacement < 0:
            displacement = 0
        
        self.audio_player.status_change("signal", displacement)


        

    def release_slider_2(self):
        self.audio_player.change_music_position(self.ui.horizontalSlider_2.value())
        self.user_active = False
        self.audio_player.player.play()
        self.current_movie.setPaused(False)
    
    def user_activity_state(self):
        self.audio_player.player.pause()
        self.current_movie.setPaused(True)
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
            self.saving_pannel_state = SavingPannel()
        self.saving_pannel_state.show()


        

        


class AlbumFrame(QWidget):
    def __init__(self, album_name, artist, icon, type = 0, parent=None):
        super().__init__(parent)

        #importing the ui
        self.ui = album_wdiget_template.Ui_Form()
        self.ui.setupUi(self)

        self.setMinimumHeight(80)
        self.setMinimumWidth(420)

        self.Album = album_name

        #can modify stuff now
        if not type:
            self.ui.Album_name.setText(album_name)
            self.ui.Artist_name.setText(artist)
            self.ui.Album_icon.setPixmap(QPixmap(icon))

            self.Album_name = album_name
            self.ui.Album_name.clicked.connect(lambda: album_name_clicked(album_name))
            self.ui.Artist_name.clicked.connect(lambda: window.artist_search(artist))
        else:
            self.ui.Album_name.setText(album_name)
            self.ui.Artist_name.setText(artist)
            self.ui.Album_icon.setPixmap(QPixmap(icon))

            self.ui.Album_name.setStyleSheet("""
                QPushButton {
                    border: none;
                    background: transparent;
                    color: palette(window-text);
                    text-align: center;
                    margin: 0;
                    padding: 0;
                }
            """)

            self.ui.Artist_name.setStyleSheet("""
                QPushButton {
                    border: none;
                    background: transparent;
                    color: palette(window-text);
                    text-align: center;
                    margin: 0;
                    padding: 0;
                }
            """)

            self.Album_name = album_name
            self.ui.Album_name.clicked.connect(lambda: album_name_clicked(album_name))

    
class SongFrame(QWidget):
    def __init__(self, window, song_name, Artist, Icon, Album, parent=None):
        super().__init__(parent)
        self.window = window

        #importing the ui
        self.ui = album_wdiget_template.Ui_Form()
        self.ui.setupUi(self)

        self.setMinimumHeight(80)
        self.setMinimumWidth(420)

        #can modify stuff now
        self.ui.Album_name.setText(song_name)
        self.ui.Artist_name.setText(f"{Album} by {Artist}")
        self.ui.Album_icon.setPixmap(QPixmap(Icon))

        self.ui.Album_name.setStyleSheet("""
                QPushButton {
                    border: none;
                    color: palette(window-text);
                    text-align: center;
                    margin: 0;
                    padding: 0;
                }
            """)
        
        self.ui.Artist_name.setStyleSheet("""
                QPushButton {
                    border: none;
                    background: transparent;
                    color: palette(window-text);
                    text-align: center;
                    margin: 0;
                    padding: 0;
                }
            """)
        
        self.ui.Album_name.clicked.connect(lambda: self.album_name_clicked(song_name, Artist, Album))
    
    def album_name_clicked(self, song_name, artist, album): #change this a bit later --> its kinda slowing down other stuff and hogging the way (fixed?)
        self.window.audio_player.current_index = self.window.song_base[album].index(song_name)
        self.window.ui.label_6.setText(f'"{song_name}" by {artist}')
        for item in ["mp3", "FLAC", "WAV"]:
            if Path(str(f"songs/Album/{album}/song_list/{song_name}.{item}")).exists():
                        self.window.audio_player.play((str(f"songs/Album/{album}/song_list/{song_name}.{item}")), song_name, artist, album)
                        self.window.audio_player.queue = get_song_list(album)
        self.window.current_song_index = get_song_list(album).index(song_name)

class Album():
    def __init__(self, name="Album", artist= "Artist", icon="image_ressources/default_cover", type = 0):
        self.name = name
        self.artist = artist
        self.type = type
        if Path(icon+".png").exists() or Path(icon+".jpg").exists():
            self.icon = icon
        else: 
            self.icon = "image_ressources/default_cover"
    
    def create_AlbumFrame(self):
        return AlbumFrame(self.name, self.artist, self.icon, self.type)

class AudioPlayer():
    def __init__(self, window):
        self.window = window
        
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.start_condition = True
        self.duration = 0

        self.album = None
        self.song = None
        self.artist = None

        self.current_index = 0
        
        self.audio.setVolume(1) #bc volume should be %

        self.repeat = False

        default_device = QMediaDevices.defaultAudioOutput()
        self.audio.setDevice(default_device)

        self.player.setAudioOutput(self.audio)
        self.player.durationChanged.connect(self.get_duration) #return duration <-- very weird
        self.player.positionChanged.connect(self.update_duration)
        self.player.mediaStatusChanged.connect(self.status_change) #goat: https://stackoverflow.com/questions/67752696/pyqt5-mediaplayer-how-to-get-if-the-video-ended
    
    def status_change(self, status, displacement = 1):
        if status == QMediaPlayer.EndOfMedia or status == "signal":

            if self.repeat:
                displacement = 0
            
            try:
                self.song = self.queue[self.current_index+displacement] #self.queue = window.song_base[self.Album]
            except IndexError:
                self.player.stop()
                self.window.current_movie.stop()
                return

            self.window.ui.label_6.setText(f'"{self.song}" by {self.artist}') #should i just display the song name?

            for item in ["mp3", "FLAC", "WAV"]:
                if Path(str(f"songs/Album/{self.album}/song_list/{self.song}.{item}")).exists():
                    self.play(Path(str(f"songs/Album/{self.album}/song_list/{self.song}.{item}")), self.song, self.artist, self.album, False)
            self.current_index = self.window.song_base[self.album].index(self.song)



    
    def play(self, source = "", song_name = "???", artist = "???", album = "???", cond = True): 
        self.album = album
        self.song = song_name
        self.artist = artist
        path = Path(source).resolve()
        
        self.queue = self.window.song_base[self.album] 

        try: 
            self.timer.stop()
        except AttributeError:
            pass

        if not path.exists():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Audio file could not be found")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        
        
        self.player.setSource(QUrl.fromLocalFile(path)) 
        self.player.play()

        #cd_gif_making(window.cd)

        if not Path(f"songs/Album/{self.album}/disc_gif.gif").exists():
            final_cd = cd_making(self.album)
            cd_gif_making(final_cd, self.album)
        
        self.window.ui.horizontalSlider_2.setValue(0)
        
        if cond:
            if self.window.current_movie:
                self.window.current_movie.stop()
                self.window.current_movie = None
                self.window.ui.label_2.clear()

                QApplication.processEvents()

            self.window.current_movie = QMovie(f"songs/Album/{self.album}/disc_gif.gif")
            self.window.ui.label_2.setMovie(self.window.current_movie)
            self.window.current_movie.start()
        
        self.visible = 40
        self.count = 0
        self.txt, self.txt_len = self.get_name_len()

        if self.txt_len: 
            self.timer = QTimer()
            self.timer.timeout.connect(lambda: self.change_position_txt())
            self.timer.start(70)
    
    def change_position_txt(self): # <-- make an animation instead?
        visible = self.visible

        scroll = "     " + self.txt + "           " + self.txt

        self.window.ui.label_6.setText(scroll[self.count:self.count+visible])

        self.count +=1

        if self.count >= len(self.txt ) +10:
            self.count = 0
    
    def get_name_len(self):
        txt = self.window.ui.label_6.text()
        txt_len = len(txt)
        
        if txt_len > self.visible:
            return txt, txt_len 
        return None, None

    def get_duration(self, media_duration):
        self.duration = media_duration #in milisec

    
    def update_duration(self, position):
        if not self.window.user_active:
            self.window.ui.label.setText(f"{(position//1000)//60}:{(position//1000)%60:02d} / {(self.duration//1000)//60}:{(self.duration//1000)%60:02d}")
            self.window.ui.horizontalSlider_2.setValue(int(position/self.duration * 1000))
        else:
            self.player.pause()
            #window.ui.label_2.movie.pause()
    
    def change_music_position(self, new_pos):
        self.player.setPosition(int(new_pos/1000 * self.duration))
    
    #audio controls
    def start_stop(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.window.current_movie.setPaused(True) #pauses instead of stopping(aka. needing to restart from begging)
            self.window.ui.pushButton_7.setFlat(True)
        else:
            self.player.play() 
            self.window.current_movie.setPaused(False)
            self.window.ui.pushButton_7.setFlat(False)
    
    def volume_change(self, value):
        self.audio.setVolume(value/100)

class SavingPannel(QDialog): #dont forget to add the disk cover and gif gen here 
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
        self.chosen_cover = "image_ressources/default_cover.jpg"

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
            filter="Image Files (*.png *.jpg)" #add more filters later and turn them all to png
        )
        if file_name:
            self.chosen_cover = file_name
            self.ui.label_6.setText(f"{Path(file_name).name} chosen")
            self.ui.label_7.setPixmap(QPixmap(Path(file_name)))

        
    def multi_file_fetch(self,caption_): #songs
        file_name, _ = QFileDialog.getOpenFileNames(
            parent=None,
            caption = caption_,
            filter="Image Files (*.mp3 *.FLAC *.WAV)" #add more filters later and turn them all to png
        )
        if file_name:
            self.chosen_songs = file_name
            count = ["", "was"]
            file_count = len(file_name)
            if file_count > 1:
                count = ["s","were"]
            self.ui.label_5.setText(f"{file_count} file{count[0]} {count[1]} chosen")
    
    def create_album(self):
        self.chosen_name = self.ui.textEdit.toPlainText()
        self.chosen_artist = self.ui.textEdit_2.toPlainText()

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
            #Path(self.chosen_cover).rename(f"{folder}/cover.png") 
            shutil.copy(self.chosen_cover, f"{folder}/cover.png")

            Path(f"{folder}/info.txt").touch() 
            try:
                with open(f"{folder}/info.txt", "w") as f:
                    f.write(json.dumps(dict(Artist =self.chosen_artist)))
            except FileNotFoundError:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setText("Failed to store the artist of the album")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()
                

            for songs in self.chosen_songs:
                #Path(songs).rename(f"songs/Album/{self.chosen_name}/song_list/{Path(songs).name}")
                shutil.copy(songs, f"songs/Album/{self.chosen_name}/song_list/{Path(songs).name}")

            #gif saving <-- leave this always at end bc it will freeze the app for 1-2 seconds
            self.cd = cd_making(self.chosen_name) #f"songs\Album\{self.chosen_name}\cover.jpg"
            cd_gif_making(self.cd, self.chosen_name)

            show_albums(False, self.chosen_name)
            
            self.close()

        
    def close(self):
        self.hide()

            
        




def album_name_clicked(album_name):
        window.ui.label_3.setText(f"Queue: {album_name}")

        current_font = window.ui.label_3.font()
        current_font.setPointSize(18)
        current_font.setBold(0)

        window.ui.label_3.setFont(current_font)

        window.selected_album = album_name
        clear_layout(window.ui.verticalLayout_19)
        if not Path(f"songs/Album/{album_name}/disc.png").exists():
            try:
                cd_making(album_name)
            except FileNotFoundError:
                pass
        show_songs(album_name)

def cd_making(album): #find a way to make it more efficient -> rotate a widget maybe? / add cache to not regenerate gif every click
    template_path = "image_ressources/template.png" #move the cd png and gif to be generated automatically when user adds a new album -> easier on script when using it
    output_path = f"songs/Album/{album}/disc.png"


    template = Image.open(template_path).convert("RGBA")
    for ext in [".png", ".jpg"]:
        fodder = Path(f"songs/Album/{album}/cover").with_suffix(ext)
        if fodder.exists():
            break
    photo = Image.open(fodder).convert("RGBA")

    squared_photo = ImageOps.fit(photo, (736, 736), Image.Resampling.LANCZOS)
    final_disc = Image.alpha_composite(squared_photo, template)

    #creates a white underlayer to hide the black background
    white_bg = Image.new("RGBA", final_disc.size, (255,255,255,255))
    #disc_on_white = Image.alpha_composite(white_bg, final_disc) <-- change for a cd background or smt to make it look nicer

    final_disc.save(output_path, "PNG")

    template.close()
    photo.close()

    return final_disc

def cd_gif_making(final_disc, album):
    frames = []

    for ang in range(0,360, 4):
        rotated_frame = final_disc.rotate(-ang, resample=Image.Resampling.BILINEAR, fillcolor=(255,255,255,255)) #bilinear is faster than cubic
        frames.append(rotated_frame.convert("P", palette=Image.Palette.ADAPTIVE)) #aparently makes the gif size tiny while barely sacrificing quality

    frames[0].save(
        f"songs/Album/{album}/disc_gif.gif", #gif output path
        save_all = True,
        append_images=frames[1:], #dont take frame 0 or else we will have 2 at angle 0
        duration =45,
        loop=0, #inf loop
        optimize = True,
        disposal=2 #clears previous frames 
    )

    for frame in frames:
        frame.close()




def album_info(album_name):
    try:
        with open(f"songs/Album/{album_name}/info.txt", "rt") as file:
            info_dump = json.loads(file.read())
        return info_dump
    except FileNotFoundError:
        return {"Artist":"???"}

def show_songs(album):
    song_list = get_song_list(album)

    for i in range(len(song_list)):
        window.ui.verticalLayout_19.insertWidget(i, SongFrame(window, song_list[i], album_info(album)["Artist"], Path(f"songs/Album/{album}/cover"), album))
    window.ui.verticalLayout_19.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
    
    if not window.audio_player.player.source().isValid(): #checks if there is any media playing on qmediaplayer rn --> isPlaying() only checked if it was currently running (pausing meant that it wasnt running)
        if Path(f"songs/Album/{album}/disc.png").exists():
            path_temp = f"songs/Album/{album}/disc.png"
        else: 
            path_temp = "image_ressources/default_cover.jpg"
        window.ui.label_2.setPixmap(QPixmap(path_temp))
    
def get_song_list(album):
    #use to make queue?
    song_list = []

    for item in Path(f"songs/Album/{album}/song_list").iterdir():
        song_list.append((item.stem))

    return song_list

def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()



def show_albums(condition = True, album = None): #make dictionnary here --> make super efficient for the fucks of it (maybe add a refresh button later to bypass this system?)
    if condition:
        for item in Path("songs/Album/").iterdir():
            artist= album_info(item.stem)["Artist"]

            window.song_base[item.stem] = None
            window.artist_base[item.stem] = artist

            frame = Album(item.stem, artist, f"{item}/cover").create_AlbumFrame()
            window.album_frame[item.stem] = frame      #key = album name | value = [album name, Artist name, location of cover image]
            window.ui.verticalLayout_16.insertWidget(window.ui.verticalLayout_16.count()-1, frame)
        
        for i in window.song_base.keys():
            try:
                window.song_base[i] = list(item.stem for item in Path(f"songs/Album/{i}/song_list").iterdir()) #now song_base has a dictionnary with every song 
            except FileNotFoundError:
                pass
    else:
        item = Path(f"songs/Album/{album}")
        window.song_base[album] = list(item.stem for item in Path(f"songs/Album/{album}/song_list").iterdir())
        frame = Album(item.stem, album_info(item.stem)["Artist"], f"{item}/cover").create_AlbumFrame()
        window.album_frame[item.stem] = frame
        window.ui.verticalLayout_16.insertWidget(window.ui.verticalLayout_16.count()-1, frame)

def clean_up_temp():
    try:
        with open("temp_delete.txt", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break

                
                if Path(f"songs/Album/{line.strip()}").exists():
                    try:
                        shutil.rmtree(f"songs/Album/{line.strip()}")
                    except FileNotFoundError:
                        pass
                else:
                    pass
    except FileNotFoundError:
        pass
    
    with open("temp_delete.txt", "w") as f:
        pass

def start_up_check():
    missing = []
    #checks folders
    for folder in config.REQUIRED_FOLDERS:
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
    
    if len(missing):
        txt = "- {f}\n"
        temp = ""

        for i in range(len(missing)):
            temp += txt.format(f=missing[i])

        msgBox = QMessageBox()
        msgBox.setText("Error during start up")
        msgBox.setInformativeText("There are missing files. check the details for seeing which ones.")
        msgBox.setDetailedText(f"the missing files are:\n\n{temp}")
        msgBox.exec()
        return False
    return True
        




if __name__ == "__main__":
    app = QApplication(sys.argv)

    if not start_up_check():
        sys.exit()

    clean_up_temp()

    window  = MainWindow()

    show_albums()

    window.show()
    sys.exit(app.exec())