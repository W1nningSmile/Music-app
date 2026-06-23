import os
import sys
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

class MusicPlayer:
    def __init__(self):
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        
        # Link audio output to the player
        self.player.setAudioOutput(self.audio)
        
        self.audio.setVolume(1) 

    def play_song(self):
        path = r"songs\Album\Sheer Heart Attack\song_list\Killer Queen.mp3"
        absolute_path = os.path.abspath(path) #turns path into url basically
        
        
        print(f"Looking for audio file at: {absolute_path}")
        
        if not os.path.exists(absolute_path):
            print("ERROR: File not found")
            return

        # Wrap in QUrl and start playback
        self.player.setSource(QUrl.fromLocalFile(absolute_path))
        self.player.play()
        print("Playing audio")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    
    music_system = MusicPlayer()
    music_system.play_song()
    

    sys.exit(app.exec())