# -*- coding: utf-8 -*-
from PySide2.QtWidgets import *
import pyopenjtalk
import numpy
import simpleaudio as sa
from scipy.io import wavfile

class MyFirstDialog(QDialog):
    def __init__(self, parent=None):
        super(MyFirstDialog, self).__init__(parent)
        self.setWindowTitle("My First Dialog")
        myLabel = QLabel("Please type something.")
        self.myLineEdit = QLineEdit("おめでとうございます。")
        myButton = QPushButton("Push!!")
        myButton.clicked.connect(self.myButtonClicked)
        layout = QVBoxLayout()
        layout.addWidget(myLabel)
        layout.addWidget(self.myLineEdit)
        layout.addWidget(myButton)
        self.setLayout(layout)
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

        QMessageBox.information(self, "Message", text + '\n' + pyopenjtalk.g2p(text))


if __name__ == '__main__':
        import sys
        app = QApplication(sys.argv)
        ui = MyFirstDialog()
        ui.show()
        app.exec_()

