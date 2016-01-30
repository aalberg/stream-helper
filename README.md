# stream-helper
Stream helper program for SSBM. Written for UMDsmash

## Version
.2

[changelog](CHANGES.md)

## Requirements
python 2.7

https://www.python.org/download/releases/2.7/

Qt 4.8.5 VS2010

https://download.qt.io/archive/qt/4.8/4.8.5/

PyQt 4

https://www.riverbankcomputing.com/software/pyqt/download

PILLOW

Run `python -m pip install pillow` in cmd

## Documentation
Real documentation coming Soon(TM)

## Temporary bad documentation
Edit sprite_folder, dest_prefix, file_suffix in character_heads.py to change
the directories being used

Change line 20 to change the saturation divider if desired.

Default Values

sprite_folder = "SSBMsprites/"

dest_prefix = "output/p"

file_suffix = ".png"

Line 20: s = s/2.0