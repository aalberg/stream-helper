# stream-helper
Stream helper program for SSBM. Written for UMDsmash.

## Current Version
1.0

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

## Quick Start
1. Download or clone the repository.
2. Run `py_stream_helper.py`.
3. Set your streaming program to read the text and image files in the output directory.
4. Edit the values of the text boxes.
5. Click the save button.

The displayed text in the streaming program should be updated to the text in the helper program.

## Documentation
### Changing the text output files
Edit line 8 of `py_stream_helper.py` (the `text_folder` variable) to change the directory to the desired location.
The program will create the directory on startup if it does not exist.

Edit the filenames starting at line 115 to change the text file each text box will output to.

### Changing the destination folder of the currently selected images
Change the folder specified by `image_dest_folder` on line 10 to the folder you wish images to be copied to.

### Changing the filename of the currently selected images
Change the name contained in `image_dest_prefix` on line 11 to the filename you wish to use.
The numbers 0-3 and `image_suffix` will be appended to the filename.

### Changing the location of the image source folder
Change the folder specified by `sprite_folder` on line 9 to the folder containing the images you wish to select from.

### Changing the images used by the dropbox boxes
Replace the files in the folder identified on line 9 by `sprite_folder` with the images you wish to select from.
These images must be the format specified on line 12 by `image_suffix`.

### Changing the method used to create the light versions of images
The function `ConvertImage` beginning on line 22 of `py_stream_helper.py` converts an image to the lightened version.
By default it works by cutting the saturation of the image in half.
To change the fraction the saturation is divided by, change line 30: `s = s / 2.0` to another equation.
More advanced operations could be performed by replacing the entire function.

## Default values
text_folder = "output/"

sprite_folder = "SSBMsprites/"

image_dest_folder = "output/img/"

image_dest_prefix = "char_"

image_suffix = ".png"