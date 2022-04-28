from typing import List

from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem
from PyQt5 import uic
import pandas as pd

DATE_COL = 0
SAMPLEID_COL = 1
SAMPLEDATE_COL = 2
FLIGHTHOURS_COL = 3
TAILNO_COL = 4
SPECRESULT_COL = 5
ANALYSIS_COL = 6
CONCLUSION_COL = 7

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
        # TODO add pickling

class HistoryWindow(QDialog):
    def __init__(self, parent):
        super(HistoryWindow, self).__init__(parent)
        self.load_ui()
        self.history: History = None
        self.partnums = set()

        self.closeButton.clicked.connect(self.close_history)
        self.selectButton.clicked.connect(self.part_selected)

    def load_ui(self):
        uic.loadUi('history.ui', self)

    def open(self):
        if self.history is not None and len(self.partnums) == 0:
            for entry in self.history.entries:
                self.partnums.add(entry.partnum)
            self.comboBox.addItems(sorted(self.partnums))
        self.show()

    def part_selected(self):
        table: QTableWidget = self.tableWidget
        table.setRowCount(0)
        selected = self.comboBox.currentText()
        entries = [entry for entry in self.history.entries if entry.partnum == selected]
        for i, entry in enumerate(entries):
            table.insertRow(i)
            table.setItem(i, DATE_COL, QTableWidgetItem(str(entry.date)))
            table.setItem(i, TAILNO_COL, QTableWidgetItem(str(entry.tailnum)))
            table.setItem(i, FLIGHTHOURS_COL, QTableWidgetItem(str(entry.flighthours)))
            table.setItem(i, CONCLUSION_COL, QTableWidgetItem(str(entry.result)))

    def close_history(self):
        self.hide()
