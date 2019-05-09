#  -*- coding: utf-8 -*-

#  Form implementation generated from reading ui file 'Tanksym.ui'
# 
#  Created by: PyQt5 UI code generator 5.11.2
# 
#  WARNING! All changes made in this file will be lost!
import pygame
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QProgressBar, QRadioButton
from PyQt5.QtCore import QRect, QSize, QMetaObject, QCoreApplication
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import sys
from game_ui import main_ui
from help_ui import Ui_Help

# 游戏一级界面，也是由designer生成的，
# 主要功能：选择单人双人模式，显示帮助，点击开始游戏，进度条没有具体实现
class Ui_Form(object):
    pygame.init()
    pygame.mixer.init()
    #  加载音效
    add_sound = pygame.mixer.Sound("./audios/startui.wav")
    add_sound.set_volume(0.5)
    add_sound.play()

    def setupUi(self, Form,Form1):
        #  self.help = help
        self.Form1 = Form1
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(624, 624)
        Form.setStyleSheet("background-color:break")
        self.progressBar = QProgressBar(Form)
        self.progressBar.setGeometry(QRect(20, 330, 611, 10))
        self.progressBar.setStyleSheet("color:white")
        self.progressBar.setProperty("value", 100)
        self.progressBar.setObjectName("progressBar")
        self.label = QLabel(Form)
        self.label.setGeometry(QRect(20, 140, 581, 141))
        self.label.setMinimumSize(QSize(581, 141))
        font = QtGui.QFont()
        font.setPointSize(72)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label.setFont(font)
        self.label.setCursor(QtGui.QCursor(Qt.ArrowCursor))
        self.label.setMouseTracking(True)
        self.label.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.label.setAcceptDrops(False)
        self.label.setToolTipDuration(-1)
        self.label.setStyleSheet("color:white;\n"
"align:center;")
        self.label.setObjectName("label")
        self.help = QPushButton(Form)
        self.help.setGeometry(QRect(30, 520, 561, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.help.setFont(font)
        self.help.setStyleSheet("color:rgb(254, 254, 254)")
        self.help.setObjectName("help")
        self.radio_one = QRadioButton(Form)
        self.radio_one.setGeometry(QRect(140, 390, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.radio_one.setFont(font)
        self.radio_one.setStyleSheet("color:white")
        self.radio_one.setObjectName("radio_one")
        self.radio_two = QRadioButton(Form)
        self.radio_two.setGeometry(QRect(350, 390, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.radio_two.setFont(font)
        self.radio_two.setStyleSheet("color:white")
        self.radio_two.setObjectName("radio_two")
        self.begin = QPushButton(Form)
        self.begin.setGeometry(QRect(30, 460, 561, 31))
        self.begin.clicked.connect(self.begin_game)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.begin.setFont(font)
        self.begin.setStyleSheet("color:white")
        self.begin.setObjectName("begin")

        self.retranslateUi(Form)
        #  self.progressBar.valueChanged['int'].connect(Form.jindu)
        self.help.clicked.connect(self.bangzhu)
        QMetaObject.connectSlotsByName(Form)

    def begin_game(self):
        if self.radio_one.isChecked():
            one = main_ui()
            print('启动单人模式')
            one.show()
        elif self.radio_two.isCheckable():
            two =main_ui('two')
            print('启动双人模式')
            two.show()

    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "坦克大战"))
        self.label.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:48pt; color:# fefefe;\">坦克大战</span></p></body></html>"))
        self.help.setText(_translate("Form", "游戏帮助"))
        self.radio_one.setText(_translate("Form", "单人模式"))
        self.radio_two.setText(_translate("Form", "双人模式"))
        self.begin.setText(_translate("Form", "开始游戏"))

    def bangzhu(self):
        #  self.help.setupUi(self.Form1)
        self.Form1.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Form = QWidget()
    Form_help = QWidget()
    ui = Ui_Form()
    ui.setupUi(Form, Form_help)
    # 初始化帮助界面
    help = Ui_Help()
    help.setupUi(Form_help)

    Form.show()
    sys.exit(app.exec_())

