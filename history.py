import os
from typing import List

from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem
from PyQt5 import uic
import pandas as pd
from joblib import load, dump

from util import resource_path

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
        df = pd.read_excel(fileName)
        self.entries: List[HistoryEntry] = [HistoryEntry(row) for row in df.itertuples()]
    def __iter__(self):
        return iter(self.entries)

class HistoryWindow(QDialog):
    def __init__(self, parent):
        super(HistoryWindow, self).__init__(parent)
        self.load_ui()
        try:
            self.history: History = load('data/history.pkl')
        except:
            self.history: History = None
        self.partnums = set()

        self.closeButton.clicked.connect(self.close_history)
        self.selectButton.clicked.connect(self.part_selected)

    def load_ui(self):
        uic.loadUi(resource_path('history.ui'), self)

    def open(self):
        if self.history is not None and len(self.partnums) == 0:
            for entry in self.history:
                self.partnums.add(entry.partnum)
            self.comboBox.addItems(sorted(self.partnums))
        self.show()

    def part_selected(self):
        table: QTableWidget = self.tableWidget
        table.setRowCount(0)
        selected = self.comboBox.currentText()
        entries = [entry for entry in self.history if entry.partnum == selected]
        for i, entry in enumerate(entries):
            table.insertRow(i)
            table.setItem(i, DATE_COL, QTableWidgetItem(str(entry.date)))
            table.setItem(i, TAILNO_COL, QTableWidgetItem(str(entry.tailnum)))
            table.setItem(i, FLIGHTHOURS_COL, QTableWidgetItem(str(entry.flighthours)))
            table.setItem(i, CONCLUSION_COL, QTableWidgetItem(str(entry.result)))

    def set_history(self, history: History):
        self.history = history
        os.makedirs('data', exist_ok=True)
        dump(history, "data/history.pkl")

    def close_history(self):
        self.hide()
