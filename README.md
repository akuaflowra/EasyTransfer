# EasyTransfer
EasyTransfer is a python script for copying the x and y cords of an event and turning it into a tkoolbridge command so its easier to make teleports!

(this is intended and only tested on RPG Maker 2000 and 2003 Steam Version)

* Link to tkoolbridge and translation patch:
  * http://suppy.bob.buttobi.net/tool/tb.html
  * https://u6.getuploader.com/yumenikkig/download/121

It is open source under the Apache License 2.0 license so anyone can update it because I'm a beginner programmer in phython

### Suggestions for updates:
* Make it so it automatically converts into a rpg maker command without needing tkoolbridge.
* Somehow figure out how to detect the map id without needing to type it in.

## How to build exe with pyinstaller.
Make sure you have python installed in your system and use the command in terminal:
```sh
pip install pyinstaller
```
Put the .py and .ico into a seperate folder then open cmd in the folder and run:
```sh
pyinstaller --onefile --icon=EasyTransfer.ico EasyTransfer.py
```

## Using the Py version
Make sure you have python installed in your system and use the command in terminal:
```sh
pip install pywin32
```
This will install the required dependency to run the script properly.

## Credits
* Kuraud for the image in the ico file
* GPT-5 for assistance
