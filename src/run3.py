#!/usr/bin/env python3
# coding: utf8
from PySide2.QtWidgets import *
import pyopenjtalk
from pyopenjtalk import *
import numpy
import simpleaudio as sa
from scipy.io import wavfile
import os.path

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
        self.talker = OJT('/home/pi/root/sys/env/tool/openjtalk/voice/htsvoice-tohoku-f01/tohoku-f01-neutral.htsvoice')
    def myButtonClicked(self):
        text = self.myLineEdit.text()

        phoneme = pyopenjtalk.g2p(text)
        self.myLabel.setText(phoneme)

        ply = self.talker.play(text)
#        ply = self.talker.play(text, speed=1.2, half_tone=-7.5, file_name='test2.wav')
#        ply = self.talker.play(text, speed=1.2, half_tone=1.1, file_name='test2.wav')
        ply.wait_done()

#        QMessageBox.information(self, "音素に変換する", text + '\n' + phoneme)

class OJT:
    def __init__(self, voice=None):
        voice = voice.encode('ascii') if os.path.isfile(voice) else pyopenjtalk.DEFAULT_HTS_VOICE
        self.__engine = pyopenjtalk.HTSEngine(voice)
    def tts(self, text, speed=1.0, half_tone=0.0):
        sr = self.__engine.get_sampling_frequency()
        self.__engine.set_speed(speed)
        self.__engine.add_half_tone(half_tone)
        return self.__engine.synthesize(pyopenjtalk.extract_fullcontext(text)), sr
    def play(self, text, speed=1.0, half_tone=0.0, file_name=None):
        x, sr = self.tts(text, speed=speed, half_tone=half_tone) # sr=48000
        if file_name: wavfile.write(file_name, sr, x.astype(numpy.int16)) # test.wav
        return sa.play_buffer(x.astype(numpy.int16), 1, 2, sr) # https://github.com/r9y9/pyopenjtalk/blob/master/pyopenjtalk/__init__.py#L133
        #if play_obj.is_playing(): play_obj.stop()
        #x = wave_file.readframes(wave_file.getnframes()) #frameの読み込み
        #x = np.frombuffer(x, dtype= "int16") #numpy.arrayに変換


if __name__ == '__main__':
        import sys
        app = QApplication(sys.argv)
        ui = MyDialog()
        ui.show()
        app.exec_()

