# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'album_frame_1400x800.ui'
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
    QLayout, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(432, 77)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 431, 76))
        self.frame.setMinimumSize(QSize(300, 76))
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QFrame.WinPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.layoutWidget_4 = QWidget(self.frame)
        self.layoutWidget_4.setObjectName(u"layoutWidget_4")
        self.layoutWidget_4.setGeometry(QRect(10, 10, 407, 56))
        self.horizontalLayout_15 = QHBoxLayout(self.layoutWidget_4)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setSizeConstraint(QLayout.SetFixedSize)
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.Album_icon = QLabel(self.layoutWidget_4)
        self.Album_icon.setObjectName(u"Album_icon")
        self.Album_icon.setMinimumSize(QSize(47, 53))
        self.Album_icon.setMaximumSize(QSize(47, 53))
        self.Album_icon.setFrameShape(QFrame.WinPanel)
        self.Album_icon.setPixmap(QPixmap(u":/magnifying_glass/Speaker_Icon.svg.png"))
        self.Album_icon.setScaledContents(True)

        self.horizontalLayout_15.addWidget(self.Album_icon)

        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setSpacing(6)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.Album_name = QPushButton(self.layoutWidget_4)
        self.Album_name.setObjectName(u"Album_name")
        self.Album_name.setMinimumSize(QSize(350, 23))
        self.Album_name.setMaximumSize(QSize(350, 23))
        font = QFont()
        font.setBold(True)
        self.Album_name.setFont(font)
        self.Album_name.setLayoutDirection(Qt.LeftToRight)
        self.Album_name.setAutoDefault(False)
        self.Album_name.setFlat(True)

        self.verticalLayout_16.addWidget(self.Album_name)

        self.Artist_name = QPushButton(self.layoutWidget_4)
        self.Artist_name.setObjectName(u"Artist_name")
        self.Artist_name.setMinimumSize(QSize(350, 23))
        self.Artist_name.setMaximumSize(QSize(350, 23))
        self.Artist_name.setFlat(True)

        self.verticalLayout_16.addWidget(self.Artist_name)


        self.horizontalLayout_15.addLayout(self.verticalLayout_16)


        self.retranslateUi(Form)

        self.Album_name.setDefault(False)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.Album_icon.setText("")
        self.Album_name.setText(QCoreApplication.translate("Form", u"Album name", None))
        self.Artist_name.setText(QCoreApplication.translate("Form", u"Artist", None))
    # retranslateUi

