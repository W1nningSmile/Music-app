# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_page_1400x800.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QScrollArea, QSizePolicy, QSlider,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1400, 800)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 0, 1391, 761))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_35 = QLabel(self.horizontalLayoutWidget)
        self.label_35.setObjectName(u"label_35")

        self.horizontalLayout_13.addWidget(self.label_35)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_3)

        self.pushButton_3 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        font = QFont()
        font.setPointSize(14)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setFocusPolicy(Qt.StrongFocus)
        self.pushButton_3.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.pushButton_3.setAutoFillBackground(True)

        self.horizontalLayout_13.addWidget(self.pushButton_3)


        self.verticalLayout.addLayout(self.horizontalLayout_13)

        self.line_3 = QFrame(self.horizontalLayoutWidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_9)

        self.label_5 = QLabel(self.horizontalLayoutWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(30, 30))
        self.label_5.setMaximumSize(QSize(30, 30))
        self.label_5.setPixmap(QPixmap(u"image_ressources/magnifying-glass-icon.png"))
        self.label_5.setScaledContents(True)

        self.horizontalLayout_10.addWidget(self.label_5)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_10)

        self.lineEdit = QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(400, 0))
        self.lineEdit.setMaximumSize(QSize(475, 20))

        self.horizontalLayout_10.addWidget(self.lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.scrollArea = QScrollArea(self.horizontalLayoutWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 448, 620))
        self.verticalLayout_16 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_16.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout.addWidget(self.scrollArea)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_11)

        self.pushButton = QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(150, 0))
        self.pushButton.setMaximumSize(QSize(150, 23))

        self.horizontalLayout_7.addWidget(self.pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.verticalLayout.setStretch(2, 2)
        self.verticalLayout.setStretch(3, 100)

        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalLayout_10.setContentsMargins(35, -1, 35, -1)
        self.label_2 = QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(420, 420))
        self.label_2.setMaximumSize(QSize(420, 420))
        self.label_2.setPixmap(QPixmap(u":/magnifying_glass/magnifying-glass-icon-26761.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_10.addWidget(self.label_2)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_8)

        self.label_6 = QLabel(self.horizontalLayoutWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(420, 16777215))
        font1 = QFont()
        font1.setPointSize(16)
        font1.setBold(True)
        self.label_6.setFont(font1)
        self.label_6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_10.addWidget(self.label_6)

        self.line_4 = QFrame(self.horizontalLayoutWidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_10.addWidget(self.line_4)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_9)

        self.label = QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName(u"label")
        font2 = QFont()
        font2.setPointSize(12)
        self.label.setFont(font2)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_10.addWidget(self.label)

        self.verticalLayout_17 = QVBoxLayout()
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.horizontalSlider_2 = QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider_2.setObjectName(u"horizontalSlider_2")
        self.horizontalSlider_2.setOrientation(Qt.Horizontal)

        self.verticalLayout_17.addWidget(self.horizontalSlider_2)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.pushButton_4 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_9.addWidget(self.pushButton_4)

        self.pushButton_8 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_8.setObjectName(u"pushButton_8")

        self.horizontalLayout_9.addWidget(self.pushButton_8)

        self.pushButton_7 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_7.setObjectName(u"pushButton_7")

        self.horizontalLayout_9.addWidget(self.pushButton_7)

        self.pushButton_6 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.horizontalLayout_9.addWidget(self.pushButton_6)

        self.pushButton_5 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_9.addWidget(self.pushButton_5)


        self.verticalLayout_17.addLayout(self.horizontalLayout_9)

        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_17.addItem(self.verticalSpacer_10)


        self.verticalLayout_10.addLayout(self.verticalLayout_17)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 10, -1, -1)
        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_12)

        self.label_4 = QLabel(self.horizontalLayoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(40, 40))
        self.label_4.setMaximumSize(QSize(40, 40))
        self.label_4.setPixmap(QPixmap(u"image_ressources/Speaker_Icon.png"))
        self.label_4.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.label_4)

        self.horizontalSlider = QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setMinimumSize(QSize(362, 22))
        self.horizontalSlider.setMaximumSize(QSize(362, 22))
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.horizontalSlider)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_13)


        self.verticalLayout_10.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_11)


        self.horizontalLayout_3.addLayout(self.verticalLayout_10)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_3 = QLabel(self.horizontalLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_14)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.scrollArea_2 = QScrollArea(self.horizontalLayoutWidget)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_4 = QWidget()
        self.scrollAreaWidgetContents_4.setObjectName(u"scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setEnabled(True)
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, 0, 419, 708))
        self.verticalLayout_19 = QVBoxLayout(self.scrollAreaWidgetContents_4)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_19.addItem(self.verticalSpacer_7)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_4)

        self.verticalLayout_2.addWidget(self.scrollArea_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)
        self.horizontalLayout_3.setStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1400, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Your Library</span></p></body></html>", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"+ Add", None))
        self.label_5.setText("")
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Delete selected album", None))
        self.label_2.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Song name", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"0:00 / 0:00", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"shuffle", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"back", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Start/stop", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"next", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"repeat", None))
        self.label_4.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:18pt; font-weight:600;\">Queue:</span></p></body></html>", None))
    # retranslateUi

