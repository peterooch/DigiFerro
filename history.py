from distutils.log import warn
import os
from typing import List

from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QFileDialog, QHeaderView, QAbstractItemView, QMessageBox
from PyQt5 import uic
import pandas as pd
from joblib import load, dump
from Report import Report

from util import extract_dir, resource_path

DATE_COL = 0
SAMPLEID_COL = 1
SAMPLEDATE_COL = 2
FLIGHTHOURS_COL = 3
TAILNO_COL = 4
SPECRESULT_COL = 5
ANALYSIS_COL = 6
CONCLUSION_COL = 7
ENTRYID_COL = 8

class HistoryEntry:
    '''
    Contains all the information and analysis results from a single sample
    '''
    fixme_once = set()
    def __init__(self, obj) -> None:
        if type(obj) != Report:
            row = obj
            self.date = row[1]
            self.tailnum = row[2]
            self.partnum = row[3]
            self.testnum = row[4]
            self.flighthours = row[5]
            self.result = row[6]
            self.extra_data = None
        else:
            report = obj
            self.date = report.sampleDate
            self.tailnum = report.tailNumber
            self.partnum = report.partNumber
            self.testnum = report.testNumber
            self.flighthours = report.timeSinceOverhaul
            self.result = 'TBD' # FIXME
            self.extra_data = report

    def set_id(self, int_id):
        self._int_id = int_id

    @property
    def id(self):
        return self._int_id

    def __getitem__(self, label):
        '''
        Dictionary-like method to get relevant entry information using its column name
        '''
        if label == "Date":
            return self.date
        if label == "Tail Number":
            return self.tailnum
        if label == "Flight Hours":
            return self.flighthours
        if label == "Analysis Result":
            return self.result
        if label == "Sample ID":
            return self.testnum
        if label not in HistoryEntry.fixme_once:
            warn(f'FIXME: Requested Label "{label}" is not implemented')
            HistoryEntry.fixme_once.add(label)
        return "" # FIXME

class History:
    '''
    Container class for `HistoryEntry` objects, with methods to interate, add, remove entries
    '''
    def __init__(self, filename='') -> None:
        self._id_counter = 1

        if filename == '':
            self.entries: List[HistoryEntry] = []
            return

        df = pd.read_excel(filename)
        self.entries: List[HistoryEntry] = [HistoryEntry(row) for row in df.itertuples()]
        for entry in self.entries:
            self._set_int_id(entry)
    def __iter__(self):
        return iter(self.entries)
    def _set_int_id(self, entry: HistoryEntry):
        '''
        Attach an internal id for each entry to keep track and to simplify history managment
        '''
        entry.set_id(self._id_counter)
        self._id_counter += 1
    def __iadd__(self, other):
        # The user should try to avoid having identical entries
        self.entries += other.entries
        for entry in other.entries:
           self._set_int_id(entry)
        return self
    def add_entry(self, entry: HistoryEntry):
        self._set_int_id(entry)
        self.entries.append(entry)
    def _get_index(self, entry_id):
        entry_id = int(entry_id) # cast string to int if needed
        return next(i for i, entry in enumerate(self.entries) if entry.id == entry_id)
    def remove_entry(self, entry_id):
        self.entries.pop(self._get_index(entry_id))
    def __getitem__(self, entry_id):
        return self.entries[self._get_index(entry_id)]

HISTORY_PATH = 'data/history.pkl'
HISTORY_FOLDER = 'data'

class HistoryWindow(QDialog):
    '''
    History managment window
    '''
    def __init__(self, parent):
        super(HistoryWindow, self).__init__(parent)
        self.parent = parent
        self.load_ui()
        # Load and set history data
        try:
            self.history: History = load(HISTORY_PATH)
        except:
            self.history: History = None
        self.partnums = set()
        self.selected_entries: List[HistoryEntry] = []

        # Set up push buttons
        self.closeButton.clicked.connect(self.close_history)
        self.selectButton.clicked.connect(self.part_selected)
        self.exportButton.clicked.connect(self.export)
        self.removeButton.clicked.connect(self.remove_entry)
        self.detailsButton.clicked.connect(self.details)

        # Set up the table widget behavior
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setColumnHidden(ENTRYID_COL, True)

    def load_ui(self):
        uic.loadUi(resource_path('history.ui'), self)

    def open(self):
        if self.history is not None and len(self.partnums) == 0:
            for entry in self.history:
                self.partnums.add(entry.partnum)
            self.comboBox.addItems(sorted(self.partnums))
        self.part_selected()
        self.show()

    def part_selected(self):
        table: QTableWidget = self.tableWidget
        table.setRowCount(0) # Remove the other
        selected = self.comboBox.currentText()
        self.selected_entries = [entry for entry in self.history if entry.partnum == selected]
        for i, entry in enumerate(self.selected_entries):
            table.insertRow(i)
            table.setItem(i, DATE_COL, QTableWidgetItem(str(entry.date)))
            table.setItem(i, SAMPLEID_COL, QTableWidgetItem(str(entry.testnum)))
            table.setItem(i, TAILNO_COL, QTableWidgetItem(str(entry.tailnum)))
            table.setItem(i, FLIGHTHOURS_COL, QTableWidgetItem(str(entry.flighthours)))
            table.setItem(i, ANALYSIS_COL, QTableWidgetItem(str(entry.result)))
            table.setItem(i, ENTRYID_COL, QTableWidgetItem(str(entry.id)))

    def _get_selection(self):
        table: QTableWidget = self.tableWidget

        items = table.selectedIndexes()
        if len(items) < 1:
            return
        item = items[0]
        return table.item(item.row(), ENTRYID_COL).text()

    def remove_entry(self):
        self.history.remove_entry(self._get_selection())
        self.part_selected()
        self._save_history()

    def details(self):
        entry = self.history[self._get_selection()]
        
        if entry.extra_data is None:
            msgbox = QMessageBox(self)
            msgbox.setWindowTitle('DigiFerro')
            msgbox.setText('There are no more details to be displayed')
            return msgbox.exec()

        # FIXME implement showing of extra_data   

    def _save_history(self):
        os.makedirs(HISTORY_FOLDER, exist_ok=True)
        dump(self.history, HISTORY_PATH)

    def set_history(self, history: History):
        if self.history is None:
            self.history = history
        else:
            self.history += history
        self._save_history()

    def close_history(self):
        self.hide()
    
    def export(self):
        save_dir = self.parent.get_setting('excel_save_dir', '.')
        current_selection = self.comboBox.currentText()
        file_path, _ = QFileDialog.getSaveFileName(self, directory=f'{save_dir}/{current_selection}.xlsx', filter='Excel files (*.xlsx)')

        if file_path == '':
            return

        self.parent.set_setting('excel_save_dir', extract_dir(file_path))

        table: QTableWidget = self.tableWidget

        headers = []
        for i in range(table.columnCount()):
            header = table.horizontalHeaderItem(i).text()
            if 'Hidden' in header:
                continue
            headers.append(header)
        
        rows = []
        for entry in self.selected_entries:
            row = []
            for header in headers:
                row.append(entry[header])
            rows.append(row)
        
        df = pd.DataFrame(data=rows, columns=headers)
        df.to_excel(file_path, encoding="utf-8", engine='openpyxl')
