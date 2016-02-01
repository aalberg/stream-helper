import colorsys
import os
import sys
import shutil
from PIL import Image
from PyQt4 import QtCore, QtGui

text_folder = "output/"
sprite_folder = "SSBMsprites/"
image_dest_folder = "output/img/"
image_dest_prefix = "char_"
image_suffix = ".png"

def CreateDirectories():
  if not os.path.exists(text_folder):
    print "Creating text output folder", text_folder
    os.makedirs(text_folder)
  if not os.path.exists(image_dest_folder):
    print "Creating image output folder", image_dest_folder
    os.makedirs(image_dest_folder)

def ConvertImage(filename):
  im = Image.open(filename)
  ld = im.load()
  width, height = im.size
  for y in range(height):
    for x in range(width):
      r, g, b, a = ld[x,y]
      h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
      s = s / 2.0
      r, g, b = colorsys.hsv_to_rgb(h, s, v)
      ld[x,y] = (int(r * 255.9999), int(g * 255.9999), int(b * 255.9999), a)
  im.save(filename)

class AutoTextBox(QtGui.QLineEdit):
  def __init__(self, parent, other, filepath, placeholder):
    super(AutoTextBox, self).__init__(parent)
    self.other = other
    self.filepath = filepath
    self.setPlaceholderText(placeholder)
    self.autosave = False

    self.connect(self, QtCore.SIGNAL("textChanged(QString)"), self.OnChanged)

  def Save(self):
    with open(self.filepath, "w") as f:
      f.write(self.text())

  def SetAutosave(self, state):
    self.autosave = state
    if self.autosave:
      self.Save()

  def OnChanged(self, text):
    if self.autosave:
      self.Save()

class SwapButton(QtGui.QPushButton):
  def __init__(self, parent, text, pairs):
    super(SwapButton, self).__init__(text, parent)
    self.pairs = pairs

    self.connect(self, QtCore.SIGNAL("clicked()"), self.Swap)

  def Swap(self):
    for pair in self.pairs:
      temp_text = pair[0].text()
      pair[0].setText(pair[1].text())
      pair[1].setText(temp_text)

class CharHeadComboBox(QtGui.QComboBox):
  def __init__(self, parent, dest_path, num, files, check_box):
    super(CharHeadComboBox, self).__init__(parent)
    self.dest_path = dest_path
    self.num = num
    self.check_box = check_box
    self.autosave = False

    self.addItems(files)
    self.empty_index = self.findText("Empty" + image_suffix, QtCore.Qt.MatchFixedString)
    self.setCurrentIndex(self.empty_index)
    self.connect(self, QtCore.SIGNAL("currentIndexChanged(int)"), self.OnIndexChanged)
    check_box.connect(check_box, QtCore.SIGNAL("stateChanged(int)"), self.CheckboxChanged)

  def Save(self):
    src = sprite_folder + str(self.currentText())
    shutil.copyfile(src, self.dest_path)
    if self.check_box.isChecked():
      ConvertImage(self.dest_path)

  def SetAutosave(self, state):
    self.autosave = state
    if self.autosave:
      self.Save()

  def OnIndexChanged(self, index):
    if self.autosave:
      self.Save()

  def CheckboxChanged(self, i):
    self.OnIndexChanged(self.currentIndex())

class CharHeadWindow(QtGui.QWidget):
  def __init__(self):
    super(CharHeadWindow, self).__init__()
    self.initUI()

  def initUI(self):
    self.setGeometry(300, 300, 500, 240)
    self.setWindowTitle("PyStreamHelper")
    self.saveable_items = []

    # Title textboxes.
    self.text_boxes = [None]*6
    self.text_boxes[0] = AutoTextBox(self, self.text_boxes[1], text_folder + "title1.txt", "Title 1")
    self.text_boxes[1] = AutoTextBox(self, self.text_boxes[0], text_folder + "title2.txt", "Title 2")

    # Player name and score textboxes.
    self.text_boxes[4] = AutoTextBox(self, self.text_boxes[1], text_folder + "score_l.txt", "")
    self.text_boxes[4].setFixedWidth(30)
    self.text_boxes[2] = AutoTextBox(self, self.text_boxes[1], text_folder + "player_l.txt", "Player L")
    self.text_boxes[3] = AutoTextBox(self, self.text_boxes[1], text_folder + "player_r.txt", "Player R")
    self.text_boxes[5] = AutoTextBox(self, self.text_boxes[1], text_folder + "score_r.txt", "")
    self.text_boxes[5].setFixedWidth(30)

    self.saveable_items.extend(self.text_boxes)

    # Comboboxes and checkboxes.
    self.combo_boxes = [None]*4
    self.check_boxes = [None]*4
    files = os.listdir(sprite_folder)
    for i in xrange(4):
      self.check_boxes[i] = QtGui.QCheckBox("light colors", self)
      self.combo_boxes[i] = CharHeadComboBox(self, image_dest_folder + image_dest_prefix + str(i) + image_suffix,
                                             i, files, self.check_boxes[i])
    self.saveable_items.extend(self.combo_boxes)

    # Reset button.
    self.reset_btn = QtGui.QPushButton("Reset", self)
    self.reset_btn.connect(self.reset_btn, QtCore.SIGNAL('clicked()'), self.Reset)

    # Autosave checkbox.
    self.autosave_box = QtGui.QCheckBox("autosave", self)
    self.autosave_box.connect(self.autosave_box, QtCore.SIGNAL("stateChanged(int)"),
                              self.AutosaveChanged)

    # Save button.
    save_btn = QtGui.QPushButton("Save", self)
    save_btn.connect(save_btn, QtCore.SIGNAL('clicked()'), self.Save)

    # Swap button.
    self.swap_button = SwapButton(self, "Swap Players", ((self.text_boxes[2], self.text_boxes[3]),
                                                         (self.text_boxes[4], self.text_boxes[5])))

    # Add everything to the layout.
    main = QtGui.QVBoxLayout()
    
    # Row 0.
    row = QtGui.QHBoxLayout()
    row.addWidget(self.text_boxes[0])
    row.addWidget(self.text_boxes[1])
    main.addLayout(row)
    
    # Row 1.
    row = QtGui.QHBoxLayout()
    row.addWidget(self.text_boxes[4])
    row.addWidget(self.text_boxes[2])
    row.addWidget(self.text_boxes[3])
    row.addWidget(self.text_boxes[5])
    main.addLayout(row)
    
    # Rows 2+3.
    row1 = QtGui.QHBoxLayout()
    row2 = QtGui.QHBoxLayout()
    for i in xrange(4):
      row1.addWidget(self.combo_boxes[i])
      row2.addWidget(self.check_boxes[i])
    main.addLayout(row1)
    main.addLayout(row2)
      
    # Row 4.
    row = QtGui.QHBoxLayout()
    row.addWidget(self.reset_btn)
    row.addWidget(self.autosave_box)
    row.addWidget(save_btn)
    row.addWidget(self.swap_button)
    main.addLayout(row)
    self.setLayout(main)

  def Reset(self):
    for text_box in self.text_boxes:
      text_box.setText("")
    for combo_box in self.combo_boxes:
      combo_box.setCurrentIndex(combo_box.empty_index)
    for check_box in self.check_boxes:
      check_box.setCheckState(False)

  def AutosaveChanged(self, i):
    state = self.autosave_box.isChecked()
    for item in self.saveable_items:
      item.SetAutosave(state)

  def Save(self):
    for item in self.saveable_items:
      item.Save()

def main():
  CreateDirectories()

  # Create an PyQT4 application object.
  a = QtGui.QApplication(sys.argv)
  w = CharHeadWindow()

  # Show window
  w.show()

  sys.exit(a.exec_())

if __name__ == "__main__":
  main()