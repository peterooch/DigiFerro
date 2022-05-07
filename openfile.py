from os import path

from PyQt5.QtWidgets import QDialog, QFileDialog, QCalendarWidget
from PyQt5 import uic

from imageproc import image
from util import resource_path
from Report import Report

class OpenFileWindow(QDialog):
    def __init__(self, parent):
        super(OpenFileWindow, self).__init__(parent)
        self.parent = parent
        self.load_ui()
        self.pushButton.clicked.connect(self.browse)
        self.buttonBox.button(self.buttonBox.Ok).clicked.connect(self.ok)
        self.buttonBox.button(self.buttonBox.Cancel).clicked.connect(self.cancel)
        self.set_calendar()

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
        testNumber = self.sampleNumLabel.text()
        squadron = self.squadronEdit.text()
        hangar = self.hangarEdit.text()
        sampleDate = self.sampleDateEdit.date()
        tailNumber = self.tailNumEdit.text()
        partNumber = self.partNumEdit.text()
        timeSinceOverhaul = self.overhaulTimeEdit.value()
        iron = self.ironEdit.text()
        titanium = self.titaniumEdit.text()
        otherMetals = self.otherMetalsComboBox.currentText()
        scale = self.scaleEdit.value()
        report = Report(squadron, hangar, sampleDate, timeSinceOverhaul,
        iron, titanium, otherMetals, scale, testNumber,
        tailNumber, partNumber, 80)
        img = image(self.imagePathEdit.text())
        self.parent.set_image(img)
        self.parent.show_image('original')
    
    def cancel(self):
        self.hide()
    
    # Popout Calendar code
    def set_calendar(self):
        # Add calendar widget
        self.calendarWidget = QCalendarWidget(self)
        self.calendarWidget.hide() # Hide until needed
        
        # Reposition calendar widget to be below the date widget
        rect = self.sampleDateEdit.geometry()
        self.calendarWidget.move(rect.x(), rect.y() + rect.height())

        # Dialog width fixup (in case dialog is not wide enough to show the calendar)
        size = self.size()
        if size.width() < rect.x() + self.calendarWidget.sizeHint().width():
            size.setWidth(rect.x() + self.calendarWidget.sizeHint().width())
            self.resize(size)

        self.calendarWidget.selectionChanged.connect(lambda *args: self.sampleDateEdit.setDate(self.calendarWidget.selectedDate()))

        # Connect toggle_calendar and set the field it uses
        self.calendarVisible = False
        self.showCalendarButton.clicked.connect(self.toggle_calendar)

    def toggle_calendar(self):
        if self.calendarVisible is False:
            self.calendarWidget.setSelectedDate(self.sampleDateEdit.date())
            self.calendarWidget.show()
            self.calendarVisible = True
            self.showCalendarButton.setText("Hide Calendar")
        else:
            self.calendarWidget.hide()
            self.calendarVisible = False
            self.showCalendarButton.setText("Show Calendar")
