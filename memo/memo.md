# PyOpenJTalkのインストール

　`pip3`だとエラーになったので、手動でコピペした。

<!-- more -->

# 成果物

* [github](https://github.com/ytyaru/Python.PyOpenJTalk.SetUp.20210619141221)

# 問題

## `pip3 install pyopenjtalk`でエラーになる

```sh
pip3 install pyopenjtalk
```
```sh
Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
Collecting pyopenjtalk
  Cache entry deserialization failed, entry ignored
  Cache entry deserialization failed, entry ignored
Exception:
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/pip/_internal/cli/base_command.py", line 143, in main
    status = self.run(options, args)
  File "/usr/lib/python3/dist-packages/pip/_internal/commands/install.py", line 338, in run
    resolver.resolve(requirement_set)
  File "/usr/lib/python3/dist-packages/pip/_internal/resolve.py", line 102, in resolve
    self._resolve_one(requirement_set, req)
  File "/usr/lib/python3/dist-packages/pip/_internal/resolve.py", line 256, in _resolve_one
    abstract_dist = self._get_abstract_dist_for(req_to_install)
  File "/usr/lib/python3/dist-packages/pip/_internal/resolve.py", line 209, in _get_abstract_dist_for
    self.require_hashes
  File "/usr/lib/python3/dist-packages/pip/_internal/operations/prepare.py", line 283, in prepare_linked_requirement
    progress_bar=self.progress_bar
  File "/usr/lib/python3/dist-packages/pip/_internal/download.py", line 823, in unpack_url
    unpack_file_url(link, location, download_dir, hashes=hashes)
  File "/usr/lib/python3/dist-packages/pip/_internal/download.py", line 728, in unpack_file_url
    unpack_file(from_path, location, content_type, link)
  File "/usr/lib/python3/dist-packages/pip/_internal/utils/misc.py", line 600, in unpack_file
    flatten=not filename.endswith('.whl')
  File "/usr/lib/python3/dist-packages/pip/_internal/utils/misc.py", line 485, in unzip_file
    zip = zipfile.ZipFile(zipfp, allowZip64=True)
  File "/usr/lib/python3.7/zipfile.py", line 1222, in __init__
    self._RealGetContents()
  File "/usr/lib/python3.7/zipfile.py", line 1289, in _RealGetContents
    raise BadZipFile("File is not a zip file")
zipfile.BadZipFile: File is not a zip file
```

# 解決

1. 仮想環境でインストールする
2. システム用パッケージディレクトリへコピーする

## 1. 仮想環境でインストールする

　なぜか仮想環境だとインストールできた。

```python
python3 -m venv env
. ./env/bin/activate
pip install pyopenjtalk
```

　かなり時間がかかる。フリーズしているように見える。

## 2. システム用パッケージディレクトリへコピーする

　仮想環境にインストールしたPyOpenJTalk一式は以下ディレクトリにある。

* `./env/lib/python3.7/site-packages/pyopenjtalk-0.1.0-py3.7.egg-info`
* `./env/lib/python3.7/site-packages/pyopenjtalk`

　これをシステム用パッケージディレクトリへコピーする。

　まず、システム用パッケージディレクトリのパスを調べる。以下のコマンドでわかる。

```sh
python3 -c "import site; print (site.getsitepackages())"
```
```sh
['/usr/local/lib/python3.7/dist-packages', '/usr/lib/python3/dist-packages', '/usr/lib/python3.7/dist-packages']
```

　`/usr/local/lib/python3.7/dist-packages`がそれっぽい。

　最後に、PyOpenJTalk一式をシステム用パッケージディレクトリへコピーする。

* `./env/lib/python3.7/site-packages/pyopenjtalk-0.1.0-py3.7.egg-info`
* `./env/lib/python3.7/site-packages/pyopenjtalk`

```sh
sudo cp -r ./env/lib/python3.7/site-packages/pyopenjtalk-0.1.0-py3.7.egg-info /usr/local/lib/python3.7/dist-packages
sudo cp -r ./env/lib/python3.7/site-packages/pyopenjtalk /usr/local/lib/python3.7/dist-packages
```

# 動かしてみる

　まずは必要なパッケージを入手する。

```sh
pip3 install scipy
pip3 install numpy
pip3 install simpleaudio
```

　なぜ仮想環境でなくシステムにインストールするのか。それはラズパイのPySide2が仮想環境だと参照できなくなってしまうから。以下リンクの下のほうに補足してある。

* [ラズパイでPySimpleGUIQtが使えなかった](https://ytyaru.hatenablog.com/entry/2023/01/30/000000)

　べつにPySide2を使わないなら仮想環境でもいいんだけど。

## 1

a.py
```python
#!/usr/bin/env python3
# coding: utf8
import pyopenjtalk
import numpy
import simpleaudio as sa
from scipy.io import wavfile

x, sr = pyopenjtalk.tts("おめでとうございます")
wavfile.write("test.wav", sr, x.astype(numpy.int16))

play_obj = sa.play_buffer(x.astype(numpy.int16), 1, 2, 44100)
play_obj.wait_done()
#if play_obj.is_playing(): play_obj.stop()

#wavfile.write("test.wav", sr, x.astype(np.int16))

#x = wave_file.readframes(wave_file.getnframes()) #frameの読み込み
#x = np.frombuffer(x, dtype= "int16") #numpy.arrayに変換

print(pyopenjtalk.g2p('こんにちは'))
```
```sh
python3 a.py
```

## 2

b.py
```python
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
        self.myLineEdit = QLineEdit("こんにちは。")
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

        play_obj = sa.play_buffer(x.astype(numpy.int16), 1, 2, 44100)
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
```
```sh
python3 b.py
```

# 所感

　再生できた。なんとかPySide2とPyOpenJTalkが連携できるメドが立った。

　本当はPySimpleGUIQtを使いたかったのだが、[ラズパイでPySimpleGUIQtが使えなかった](https://ytyaru.hatenablog.com/entry/2023/01/30/000000)ので残念だ。さらに仮想環境でも参照できなくなってしまう。なので`pip`はシステムへインストールせねばならない。縛りだらけ。パズルのように難解でウンザリする。

# 対象環境

* <time datetime="2021-06-19T16:41:56+0900" title="実施日">2021-06-19</time>
* [Raspbierry pi](https://ja.wikipedia.org/wiki/Raspberry_Pi) 4 Model B
* [Raspberry Pi OS](https://ja.wikipedia.org/wiki/Raspbian) buster 10.0 2020-08-20 [※](http://ytyaru.hatenablog.com/entry/2020/10/06/111111)
* [bash](https://ja.wikipedia.org/wiki/Bash) 5.0.3(1)-release

```sh
$ uname -a
Linux raspberrypi 5.4.83-v7l+ #1379 SMP Mon Dec 14 13:11:54 GMT 2020 armv7l GNU/Linux
```
