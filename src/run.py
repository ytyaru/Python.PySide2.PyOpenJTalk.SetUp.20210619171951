#!/usr/bin/env python3
# coding: utf8
from PySide2.QtWidgets import *
import pyopenjtalk
import numpy
import simpleaudio as sa
from scipy.io import wavfile

class MyDialog(QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        self.setWindowTitle("PySide2 + PyOpenJTalk でテキストボックスに入力した文字列を発話する。")
        self.myLineEdit = QLineEdit("漢字も読めます。")
        self.myButton = QPushButton("話す")
        self.myButton.clicked.connect(self.myButtonClicked)
        self.myLabel = QLabel("音素")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.myLineEdit)
        self.layout.addWidget(self.myButton)
        self.layout.addWidget(self.myLabel)
        self.setLayout(self.layout)
        self.myButton.setFocus()
    def myButtonClicked(self):
        text = self.myLineEdit.text()
        x, sr = pyopenjtalk.tts(text)
        wavfile.write("test.wav", sr, x.astype(numpy.int16))

#        play_obj = sa.play_buffer(x.astype(numpy.int16), 1, 2, 44100)
        play_obj = sa.play_buffer(x.astype(numpy.int16), 1, 2, 48000) # https://github.com/r9y9/pyopenjtalk/blob/master/pyopenjtalk/__init__.py#L133
        play_obj.wait_done()
        #if play_obj.is_playing(): play_obj.stop()

        #x = wave_file.readframes(wave_file.getnframes()) #frameの読み込み
        #x = np.frombuffer(x, dtype= "int16") #numpy.arrayに変換

        phoneme = pyopenjtalk.g2p(text)
        self.myLabel.setText(phoneme)
#        QMessageBox.information(self, "音素に変換する", text + '\n' + phoneme)


if __name__ == '__main__':
        import sys
        app = QApplication(sys.argv)
        ui = MyDialog()
        ui.show()
        app.exec_()

