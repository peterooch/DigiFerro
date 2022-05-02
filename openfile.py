from os import path

from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5 import uic

from imageproc import image
from util import resource_path

class OpenFileWindow(QDialog):
    def __init__(self, parent):
        super(OpenFileWindow, self).__init__(parent)
        self.parent = parent
        self.load_ui()
        self.pushButton.clicked.connect(self.browse)
        self.buttonBox.button(self.buttonBox.Ok).clicked.connect(self.ok)
        self.buttonBox.button(self.buttonBox.Cancel).clicked.connect(self.cancel)

    def load_ui(self):
        uic.loadUi(resource_path('openfile.ui'), self)

    def open(self):
        self.show()

    def browse(self):
        image_dir = self.parent.get_setting('image_file_dir', '')
        fileName, _ = QFileDialog.getOpenFileName(self, directory=image_dir)
        if fileName == '':
            return

        directory, _ = path.split(fileName)
        self.parent.set_setting('image_file_dir', directory)

        self.imagePathEdit.setText(fileName)

    def ok(self):
        self.hide()
        img = image(self.imagePathEdit.text())
        self.parent.set_image(img)
        self.parent.show_image('original')
    
    def cancel(self):
        self.hide()
