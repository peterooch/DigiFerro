from datetime import date, datetime
from distutils.log import warn
import os
from typing import List

from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QFileDialog, QHeaderView, QAbstractItemView, QMessageBox, QDateEdit, QCalendarWidget, QPushButton
from PyQt5 import uic
from PyQt5.QtCore import QDate
import pandas as pd
from joblib import load, dump
from Report import Report

from util import extract_dir, qdate_to_date, resource_path

# DigiFerro
# Programmers:
# Baruch Rutman
# Roi Amzallag

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

            if type(row[1]) == datetime:
                self.date = row[1].date()
            elif type(row[1]) == str and row[1].count('.') == 2:
                day, month, year = row[1].split('.')
                self.date = date(int(year)+2000, int(month), int(day))
            else:
                self.date = row[1] # Faulty value

            self.tailnum = row[2]
            self.partnum = row[3]
            self.testnum = row[4]

            hours = -1
            if type(row[5]) == datetime:
                initial_time = datetime(1900, 1, 1)
                date_: datetime = row[5]
                delta = date_ - initial_time
                hours = delta.days * 24
                hours += delta.seconds // 3600
                hours += 48 # HACK Why though
                minutes = delta.seconds // 60 % 60
            elif type(row[5]) == str:
                s = row[5].replace(';', ':').replace('.', ':')
                if ':' in s:
                    hours, minutes = s.split(':')[:2]
                elif s.isnumeric():
                    hours, minutes = s, 0
            if hours != -1:
                self.flighthours = f'{hours}:{minutes}'
            else:
                self.flighthours = row[5] # Faulty value

            self.result = row[6]
            self.extra_data = None
        else:
            report: Report = obj
            self.date = report.sampleDate
            self.tailnum = report.tailNumber
            self.partnum = report.partNumber
            self.testnum = report.testNumber
            self.flighthours = report.timeSinceOverhaul
            self.result = report.conclusion
            self.extra_data = report

        # FIXME Should be filled
        self.spec_result = ''
        self.conclusion = ''
        self.sample_date: date = None

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
        if label == "Time since overhaul":
            return self.flighthours
        if label == "Analysis Result":
            return self.result
        if label == "Sample ID":
            return self.testnum
        if label not in HistoryEntry.fixme_once:
            warn(f'FIXME: Requested Label "{label}" is not implemented')
            HistoryEntry.fixme_once.add(label)
        return "" # FIXME

    def create_report(self) -> Report:
        if self.extra_data is not None:
            return self.extra_data
        #FIXME
        return Report(
            '',
            '',
            self.date,
            self.flighthours,
            0,
            0,
            '',
            '',
            self.testnum,
            self.tailnum,
            self.partnum,
            self.conclusion
        )

class History:
    '''
    Container class for `HistoryEntry` objects, with methods to interate, add, remove entries
    '''
    def __init__(self, filename='') -> None:
        self._id_counter = 1

        self.entries: List[HistoryEntry] = []
        if filename == '':
            return

        df = pd.read_excel(filename)
        for idx, row in enumerate(df.itertuples()):
            try:
                self.entries.append(HistoryEntry(row))
            except ValueError:
                print(f'Error with row {idx+1}, row values={row}')

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
        if entry_id is None:
            return None
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
            self.history: History = History('')
        self.partnums = set()
        self.selected_entries: List[HistoryEntry] = []

        # Set up push buttons
        self.closeButton.clicked.connect(self.close_history)
        self.selectButton.clicked.connect(self.part_selected)
        self.exportButton.clicked.connect(self.export)
        self.removeButton.clicked.connect(self.remove_entry)
        self.detailsButton.clicked.connect(self.details)
        self.editButton.clicked.connect(self.edit)
        self.reportButton.clicked.connect(self.gen_report)

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
        self.selected_entries = sorted([entry for entry in self.history if entry.partnum == selected], key=lambda e: e.testnum)
        for i, entry in enumerate(self.selected_entries):
            table.insertRow(i)
            table.setItem(i, DATE_COL, QTableWidgetItem(str(entry.date)))
            table.setItem(i, SAMPLEID_COL, QTableWidgetItem(str(entry.testnum)))
            table.setItem(i, TAILNO_COL, QTableWidgetItem(str(entry.tailnum)))
            table.setItem(i, FLIGHTHOURS_COL, QTableWidgetItem(str(entry.flighthours)))
            table.setItem(i, ANALYSIS_COL, QTableWidgetItem(str(entry.result)))
            table.setItem(i, ENTRYID_COL, QTableWidgetItem(str(entry.id)))
            table.setItem(i, CONCLUSION_COL, QTableWidgetItem(str(entry.conclusion)))
            table.setItem(i, SPECRESULT_COL, QTableWidgetItem(str(entry.spec_result)))
            table.setItem(i, SAMPLEDATE_COL, QTableWidgetItem(str(entry.sample_date)))

    def _get_selection(self):
        table: QTableWidget = self.tableWidget

        items = table.selectedIndexes()
        if len(items) < 1:
            return
        item = items[0]
        return table.item(item.row(), ENTRYID_COL).text()

    def remove_entry(self):
        idx = self._get_selection()
        if idx is None:
            return
        self.history.remove_entry(idx)
        self.part_selected()
        self._save_history()

    def details(self):
        idx = self._get_selection()
        if idx is None:
            return
        entry = self.history[idx]

        if entry.extra_data is None:
            msgbox = QMessageBox(self)
            msgbox.setWindowTitle('DigiFerro')
            msgbox.setText('There are no more details to be displayed')
            return msgbox.exec()

        # FIXME implement showing of extra_data   

    def edit(self):
        idx = self._get_selection()
        if idx is None:
            return
        entry = self.history[idx]
        editwindow = EditEntryWindow(self, entry)
        editwindow.exec()
        self._save_history()
        self.part_selected()

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

    def gen_report(self):
        idx = self._get_selection()
        if idx is None:
            return
        entry = self.history[idx]
        entry.create_report().generateHtml().htmlTopdf().show_pdf()

def date_to_qdate(d: date) -> QDate:
    return QDate(d.year, d.month, d.day)

class EditEntryWindow(QDialog):
    def __init__(self, parent, entry: HistoryEntry):
        '''
        `HistoryEntry` CRUD Window
        '''
        super().__init__(parent)
        self.parent = parent
        self.load_ui()

        self.updateButton.clicked.connect(self.update_entry)
        # To copy object or not?
        self.history_entry = entry

        self.sampleLabel.setText(str(entry.testnum))
        self.tailNumEdit.setText(str(entry.tailnum))
        self.partNumEdit.setText(str(entry.partnum))
        self.specEdit.setText(str(entry.spec_result))
        self.analysisEdit.setText(str(entry.result))
        self.concEdit.setText(str(entry.conclusion))

        try:
            self.dateEdit.setDate(date_to_qdate(entry.date.year))
        except AttributeError:
            self.dateEdit.setDate(QDate.currentDate())

        if entry.sample_date is None:
            self.sampleDateEdit.setDate(QDate.currentDate())
        else:
            self.sampleDateEdit.setDate(date_to_qdate(entry.sample_date))
        
        # Add calendars
        self.add_calendar(self.dateEdit, self.dateButton)
        self.add_calendar(self.sampleDateEdit, self.sampleDateButton)

        try:
            hours, minutes = entry.flighthours.split(':')
            self.overhaulTimeEdit.setValue(float(f'{hours}.{minutes}'))
        except:
            pass
    
    def update_entry(self):
        entry = self.history_entry
        if self.tailNumEdit.text() != '':
            entry.tailnum = self.tailNumEdit.text()
        if self.partNumEdit.text() != '':
            entry.partnum = self.partNumEdit.text()
        if self.specEdit.text() != '':
            entry.spec_result = self.specEdit.text()
        if self.analysisEdit.text() != '':
            entry.result = self.analysisEdit.text()
        if self.concEdit.text() != '':
            entry.conclusion = self.concEdit.text()

        entry.date = qdate_to_date(self.dateEdit.date())
        entry.sample_date = qdate_to_date(self.sampleDateEdit.date())

        hours, minutes = str(self.overhaulTimeEdit.value()).split('.')
        entry.flighthours = f'{hours}:{minutes}'

        self.close()

    def add_calendar(self, dateEdit: QDateEdit, button: QPushButton):
        # More generalized way to attach a calendar to a date field/button pair
        # Code taken from openfile.py
        calendar = QCalendarWidget(self)
        calendar.hide()
        rect = dateEdit.geometry()
        calendar.move(self.size().width() - calendar.sizeHint().width(), rect.y() + rect.height())
        calendar.selectionChanged.connect(lambda *args: dateEdit.setDate(calendar.selectedDate()))
        button.clicked.connect(lambda *args: EditEntryWindow.toggle_calendar(calendar, dateEdit, button))

    @staticmethod
    def toggle_calendar(calendar: QCalendarWidget, dateEdit: QDateEdit, button: QPushButton):
        if not calendar.isVisible():
            calendar.setSelectedDate(dateEdit.date())
            calendar.show()
            button.setText("Hide Calendar")
        else:
            calendar.hide()
            button.setText("Show Calendar")

    def load_ui(self):
        uic.loadUi(resource_path('history_edit.ui'), self)
