import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel

class second_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secondary Window")
        self.resize(300, 200)
        
        layout = QVBoxLayout() #swap for custom ui?
        label = QLabel("yo")

        layout.addWidget(label)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.resize(400, 300)
        self.sub_window = None

        # button thingy here
        button = QPushButton("Open Secondary Window")
        button.clicked.connect(self.toggle_sub_window)
        self.setCentralWidget(button)

    def toggle_sub_window(self): #part that opens up secondary window -> keep the basics bc it works for now
        # Check if the window is already created
        if self.sub_window is None:
            self.sub_window = second_window()
            self.sub_window.show()
        else:
            self.sub_window.show

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())