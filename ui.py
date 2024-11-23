import io
import sys
import torch
from main import use_neuro, model
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>332</width>
    <height>559</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string> Анализ</string>
  </property>
  <property name="styleSheet">
   <string notr="true">background-color: rgb(62, 137, 20);</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLabel" name="namesport">
    <property name="geometry">
     <rect>
      <x>50</x>
      <y>10</y>
      <width>261</width>
      <height>21</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">color: rgb(255, 255, 255);
</string>
    </property>
    <property name="text">
     <string>fffffffffffffffffffffffffffffffff</string>
    </property>
   </widget>
   <widget class="QDateEdit" name="dateEdit">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>50</y>
      <width>271</width>
      <height>31</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">background-color: rgb(255, 255, 255);</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton">
    <property name="geometry">
     <rect>
      <x>-10</x>
      <y>430</y>
      <width>351</width>
      <height>101</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">background-color: rgb(225, 96, 54);</string>
    </property>
    <property name="text">
     <string>Нажмите, чтобы анлизировать шансы на победу</string>
    </property>
   </widget>
   <widget class="QLCDNumber" name="team1result">
    <property name="geometry">
     <rect>
      <x>140</x>
      <y>110</y>
      <width>161</width>
      <height>71</height>
     </rect>
    </property>
    <property name="frameShape">
     <enum>QFrame::NoFrame</enum>
    </property>
   </widget>
   <widget class="QLCDNumber" name="team2result">
    <property name="geometry">
     <rect>
      <x>120</x>
      <y>220</y>
      <width>211</width>
      <height>61</height>
     </rect>
    </property>
    <property name="frameShape">
     <enum>QFrame::NoFrame</enum>
    </property>
    <property name="smallDecimalPoint">
     <bool>false</bool>
    </property>
    <property name="segmentStyle">
     <enum>QLCDNumber::Filled</enum>
    </property>
   </widget>
   <widget class="QLabel" name="nameteam">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>80</y>
      <width>191</width>
      <height>41</height>
     </rect>
    </property>
    <property name="text">
     <string>Введите название команд:</string>
    </property>
   </widget>
   <widget class="QLabel" name="reasultteam">
    <property name="geometry">
     <rect>
      <x>40</x>
      <y>330</y>
      <width>271</width>
      <height>16</height>
     </rect>
    </property>
    <property name="text">
     <string>Команда, которя победит с большим шансом:</string>
    </property>
    <property name="textFormat">
     <enum>Qt::RichText</enum>
    </property>
   </widget>
   <widget class="QTextEdit" name="textEdit">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>130</y>
      <width>211</width>
      <height>41</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">background-color: rgb(255, 255, 255);</string>
    </property>
    <property name="placeholderText">
     <string>Название 1 команды</string>
    </property>
   </widget>
   <widget class="QTextEdit" name="textEdit_2">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>230</y>
      <width>211</width>
      <height>41</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">background-color: rgb(255, 255, 255);</string>
    </property>
    <property name="placeholderText">
     <string>Название 2 команды</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_5">
    <property name="geometry">
     <rect>
      <x>80</x>
      <y>370</y>
      <width>171</width>
      <height>41</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">background-color: rgb(225, 96, 54);
border-radius: 20px;</string>
    </property>
    <property name="text">
     <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p align=&quot;center&quot;&gt;Пока нет результатов&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_6">
    <property name="geometry">
     <rect>
      <x>220</x>
      <y>90</y>
      <width>111</width>
      <height>21</height>
     </rect>
    </property>
    <property name="text">
     <string>В процентах, %</string>
    </property>
   </widget>
   <zorder>reasultteam</zorder>
   <zorder>namesport</zorder>
   <zorder>dateEdit</zorder>
   <zorder>pushButton</zorder>
   <zorder>team1result</zorder>
   <zorder>team2result</zorder>
   <zorder>nameteam</zorder>
   <zorder>textEdit</zorder>
   <zorder>textEdit_2</zorder>
   <zorder>label_5</zorder>
   <zorder>label_6</zorder>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>332</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""

onewindow = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>289</width>
    <height>291</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Выбор спорта</string>
  </property>
  <property name="styleSheet">
   <string notr="true">background-color: rgb(148, 201, 169);</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLabel" name="sports">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>0</y>
      <width>281</width>
      <height>31</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">font: 75 10pt &quot;Arial&quot;;
font: 75 12pt &quot;PT Astra Sans&quot;;
</string>
    </property>
    <property name="text">
     <string>Выбирите интересующию вас команду:</string>
    </property>
    <property name="textFormat">
     <enum>Qt::AutoText</enum>
    </property>
    <property name="scaledContents">
     <bool>false</bool>
    </property>
   </widget>
   <widget class="QLabel" name="label_2">
    <property name="geometry">
     <rect>
      <x>90</x>
      <y>40</y>
      <width>131</width>
      <height>81</height>
     </rect>
    </property>
    <property name="text">
     <string/>
    </property>
    <property name="pixmap">
     <pixmap>bear.png</pixmap>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton">
    <property name="geometry">
     <rect>
      <x>40</x>
      <y>130</y>
      <width>201</width>
      <height>51</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">background-color: rgb(225, 96, 54);
color: rgb(255, 255, 255);
border-radius: 20px;
</string>
    </property>
    <property name="text">
     <string>Футбол</string>
    </property>
   </widget>
   <widget class="QPushButton" name="pushButton_2">
    <property name="geometry">
     <rect>
      <x>40</x>
      <y>190</y>
      <width>201</width>
      <height>51</height>
     </rect>
    </property>
    <property name="styleSheet">
     <string notr="true">background-color: rgb(225, 96, 54);
color: rgb(255, 255, 255);
border-radius: 20px;</string>
    </property>
    <property name="text">
     <string>Баскетбол</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>289</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>

"""


class FlagMaker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        f = io.StringIO(onewindow)
        uic.loadUi(f, self)
        self.pushButton.clicked.connect(self.soccer)
        self.pushButton_2.clicked.connect(self.basketball)

    def soccer(self):
        self.soccer_window = Soccer()
        self.soccer_window.show()

    def basketball(self):
        self.basketball_window = Basketball()
        self.basketball_window.show()

class Soccer(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, *args):
        q = io.StringIO(template)
        uic.loadUi(q, self)
        self.namesport.setText('Анализ игр футбола:')
        self.pushButton.clicked.connect(self.qwert)


    def qwert(self):
        text = self.textEdit.toPlainText()
        text2 = self.textEdit_2.toPlainText()
        value = self.dateEdit.date()
        value1 = value.toPyDate()
        self.chance1, self.chance2, self.winner = use_neuro(text, text2, value1, model)
        self.team1result.display(self.chance1)
        self.team1result.repaint()
        self.team2result.display(self.chance2)
        self.team2result.repaint()
        self.label_5.setText(self.winner)




class Basketball(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, *args):
        a = io.StringIO(template)
        uic.loadUi(a, self)
        self.namesport.setText('Анализ игр баскетбола:')
        self.pushButton.clicked.connect(self.qwert)

    def qwert(self):
        text = self.textEdit.toPlainText()
        text2 = self.textEdit_2.toPlainText()
        value = self.dateEdit.date()
        value1 = value.toPyDate()
        self.chance1, self.chance2, self.winner = use_neuro(text, text2, value1, model)
        self.team1result.display(self.chance1)
        self.team1result.repaint()
        self.team2result.display(self.chance2)
        self.team2result.repaint()
        self.label_5.setText(self.winner)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FlagMaker()
    ex.show()
    sys.exit(app.exec())