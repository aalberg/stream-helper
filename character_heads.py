import colorsys
import os
import sys
import shutil
from PIL import Image
from PyQt4 import QtCore, QtGui

sprite_folder = "SSBMsprites/"
dest_prefix = "output/p"
file_suffix = ".png"

def ConvertImage(filename):
  im = Image.open(filename)
  ld = im.load()
  width, height = im.size
  for y in range(height):
    for x in range(width):
      r,g,b,a = ld[x,y]
      h,s,v = colorsys.rgb_to_hsv(r/255., g/255., b/255.)
      s = s/2.0
      r,g,b = colorsys.hsv_to_rgb(h, s, v)
      ld[x,y] = (int(r * 255.9999), int(g * 255.9999), int(b * 255.9999), a)
  im.save(filename)
      
class CharHeadComboBox(QtGui.QComboBox):
  def __init__(self, parent, num, checkbox):
    super(CharHeadComboBox, self).__init__(parent)
    self.num = num
    self.checkbox = checkbox
    self.autosave = False

  def Save(self):
    src = sprite_folder + str(self.currentText())
    dest = dest_prefix + str(self.num) + file_suffix
    #print "copied", src, "to", dest
    shutil.copyfile(src, dest)
    if self.checkbox.isChecked():
      #print "adjusting", dest
      ConvertImage(dest)
      #print "done"
    
  def onIndexChanged(self, index):
    if self.autosave:
      self.Save()

  def checkboxChanged(self, i):
    self.onIndexChanged(self.currentIndex())

class CharHeadWindow(QtGui.QWidget):
  def __init__(self):
    super(CharHeadWindow, self).__init__()
    self.initUI()

  def initUI(self):
    self.setGeometry(300, 300, 500, 120)
    self.setWindowTitle("Character Head Helper")

    # Grid layout
    grid = QtGui.QGridLayout()
    self.setLayout(grid)

    # Create comboboxes and checkboxes.
    self.combo_boxes = [None]*4
    self.check_boxes = [None]*4
    files = os.listdir(sprite_folder)
    empty_index = files.index("Empty" + file_suffix)
    for i in xrange(4):
      self.check_boxes[i] = QtGui.QCheckBox("light colors", self)
      grid.addWidget(self.check_boxes[i], 1, i)
    
      self.combo_boxes[i] = CharHeadComboBox(self, i, self.check_boxes[i])
      self.combo_boxes[i].addItems(files)
      self.combo_boxes[i].connect(self.combo_boxes[i], QtCore.SIGNAL("currentIndexChanged(int)"),
                                  self.combo_boxes[i].onIndexChanged)
      self.combo_boxes[i].setCurrentIndex(empty_index)
      grid.addWidget(self.combo_boxes[i], 0, i)

      self.check_boxes[i].connect(self.check_boxes[i], QtCore.SIGNAL("stateChanged(int)"),
                                  self.combo_boxes[i].checkboxChanged)
                             
    # Reset button
    self.reset_btn = QtGui.QPushButton("Reset", self)
    self.reset_btn.connect(self.reset_btn, QtCore.SIGNAL('clicked()'), self.Reset)
    grid.addWidget(self.reset_btn, 2, 0)

    # Autosave checkbox
    self.autosave_box = QtGui.QCheckBox("autosave", self)
    self.autosave_box.connect(self.autosave_box, QtCore.SIGNAL("stateChanged(int)"),
                              self.AutosaveChanged)
    grid.addWidget(self.autosave_box, 2, 1)
    
    # Save button
    save_btn = QtGui.QPushButton("Save", self)
    save_btn.connect(save_btn, QtCore.SIGNAL('clicked()'), self.Save)
    grid.addWidget(save_btn, 2, 2)
    
  def Reset(self):
    empty_index = self.combo_boxes[0].findText("Empty" + file_suffix, QtCore.Qt.MatchFixedString)
    for combo_box in self.combo_boxes:
      combo_box.setCurrentIndex(empty_index)
      
    for check_box in self.check_boxes:
      check_box.setCheckState(False)
      
  def AutosaveChanged(self, i):
    state = self.autosave_box.isChecked()
    for combo_box in self.combo_boxes:
      combo_box.autosave = state
      if state:
        combo_box.Save()
      
  def Save(self):
    for combo_box in self.combo_boxes:
      combo_box.Save()
      
def main():
  # Create an PyQT4 application object.
  a = QtGui.QApplication(sys.argv)
  w = CharHeadWindow()

  # Show window
  w.show()

  sys.exit(a.exec_())

if __name__ == "__main__":
  main()