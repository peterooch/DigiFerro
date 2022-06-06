from os import path

from PyQt5.QtWidgets import QDialog, QFileDialog, QCalendarWidget, QListWidget, QMessageBox
from PyQt5.QtCore import QDate
from PyQt5 import uic

from imageproc import paths_to_imgs
from util import resource_path
from Report import Report

# DigiFerro
# Programmers:
# Baruch Rutman
# Roi Amzallag

class OpenFileWindow(QDialog):
    def __init__(self, parent):
        super(OpenFileWindow, self).__init__(parent)
        self.parent = parent
        self.load_ui()
        self.pushButton.clicked.connect(self.browse)
        self.buttonBox.button(self.buttonBox.Ok).clicked.connect(self.ok)
        self.buttonBox.button(self.buttonBox.Cancel).clicked.connect(self.cancel)

        date = QDate.currentDate()
        date_format = f'{str(date.day()).zfill(2)}{str(date.month()).zfill(2)}{date.year()}'

        if date_format != self.parent.get_setting('last_date', date_format):
            self.parent.set_setting('increment', 0)

        self.parent.set_setting('last_date', date_format)
        current_increment = self.parent.get_setting('increment', 0) + 1
        self.parent.set_setting('increment', current_increment) 
        self.sampleNumLabel.setText(f'{date_format}{str(current_increment).zfill(4)}')

        self.sampleDateEdit.setDate(date)
        self.set_calendar()

        # Set Drag n Drop
        lw: QListWidget = self.imageList
        lw.setDragEnabled(True)
        lw.dragEnterEvent = lambda e: e.acceptProposedAction()
        lw.dragMoveEvent = lambda e: e.acceptProposedAction()
        lw.dropEvent = lambda e: lw.addItems(((url.path()[1:] for url in e.mimeData().urls())))

        # Lockup dialog size
        self.setFixedSize(self.size())

    def load_ui(self):
        uic.loadUi(resource_path('openfile.ui'), self)

    def open(self):
        self.show()

    def browse(self):
        image_dir = self.parent.get_setting('image_file_dir', '')
        fileNames, _ = QFileDialog.getOpenFileNames(self, directory=image_dir)
        if len(fileNames) == 0:
            return

        directory, _ = path.split(fileNames[0])
        self.parent.set_setting('image_file_dir', directory)

        self.imageList.addItems(fileNames)

    def ok(self):
        msgBox: QMessageBox = QMessageBox(self)
        testNumber = self.sampleNumLabel.text()
        squadron = self.squadronEdit.text()
        if (squadron == ''):
            return
        hangar = self.hangarEdit.text()
        if (hangar == ''):
            msgBox.setText('please fill the hangar number')
            msgBox.show()
            return
        sampleDate = self.sampleDateEdit.date()
        tailNumber = self.tailNumEdit.text()
        if (tailNumber == ''):
            msgBox.setText('please fill the tail number')
            msgBox.show()
            return
        partNumber = self.partNumEdit.text()
        if (partNumber == ''):
            msgBox.setText('please fill the part number')
            msgBox.show()
            return
        timeSinceOverhaul = self.overhaulTimeEdit.value()
        iron = self.ironEdit.text()
        if (iron == ''):
            msgBox.setText('please fill the iron number')
            msgBox.show()
            return
        titanium = self.titaniumEdit.text()
        if (titanium == ''):
            msgBox.setText('please fill the titanium number')
            msgBox.show()
            return
        otherMetals = self.otherMetalsComboBox.currentText()
        scale = self.scaleEdit.value()
        report = Report(squadron, hangar, sampleDate, timeSinceOverhaul,
        iron, titanium, otherMetals, scale, testNumber,
        tailNumber, partNumber, 80)

        self.hide()
        # Image stuff
        lw: QListWidget = self.imageList
        paths = [lw.item(i).text() for i in range(lw.count())]

        self.parent.add_images(paths_to_imgs(paths, self.scale))
    
    def cancel(self):
        self.hide()
    
    @property
    def scale(self):
        scale_ = float(self.scaleEdit.value())
        if scale_ <= 0:
            return 1.0
        return scale_

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
