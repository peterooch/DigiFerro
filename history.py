from typing import List

from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
import pandas as pd

class HistoryWindow(QDialog):
    def __init__(self, parent):
        super(HistoryWindow, self).__init__(parent)
        self.history: History = None
        self.partnums = set()
        self.selected = ""
        self.load_ui()

    def load_ui(self):
        uic.loadUi('history.ui', self)

    def open(self):
        if self.history is not None:
            for entry in self.history.entries:
                self.partnums.add(entry.partnum)
        self.comboBox.addItems(list(self.partnums))
        self.show()

class HistoryEntry:
    def __init__(self, row) -> None:
        self.date = row[1]
        self.tailnum = row[2]
        self.partnum = row[3]
        self.testnum = row[4]
        self.flighthours = row[5]
        self.result = row[6]

class History():
    def __init__(self, fileName) -> None:
        self.fileName = fileName
        self.df = pd.read_excel(fileName)
        self.entries: List[HistoryEntry] = [HistoryEntry(row) for row in self.df.itertuples()]
