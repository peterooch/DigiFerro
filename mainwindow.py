# This Python file uses the following encoding: utf-8
import os
import sys
import json
from typing import List

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QListWidgetItem, QListWidget, QLabel, QMessageBox
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap, QImage, QDropEvent
import cv2
from matplotlib import pyplot as plt
import numpy as np
from Report import Report

from imageproc import image, paths_to_imgs
from openfile import OpenFileWindow
from history import HistoryEntry, HistoryWindow, History
from login import LoginWindow
from createAccount import CreateAccount
from usermanagement import ChangePassword, User, UserManagement
from util import extract_dir, gen_graph, get_distribution, resource_path, rubbing_precent
#from graph import GraphWindow
from decisions import fragment_decision

# DigiFerro
# Programmers:
# Baruch Rutman
# Roi Amzallag
# 
# With cooperation with IAF

SETTINGS_PATH = 'settings.json'

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.load_ui()

        try:
            with open(SETTINGS_PATH, 'r') as settings:
                self.settings = json.load(settings)
        except:
            self.settings = dict()
            with open(SETTINGS_PATH, 'w') as settings:
                json.dump(self.settings, settings)

        self.login = LoginWindow(self)
        self.openfile = OpenFileWindow(self)
        self.history = HistoryWindow(self)
        self.createnewaccount = CreateAccount(self)
        self.UserManagement = UserManagement(self)
        self.about = AboutWindow(self)
        #self.graph = GraphWindow(self)
        self.images: List[image] = []
        self.image_id = -1
        self.totals_on = False
        self.graph_img = None
        self.prev_param = None
        self.report = None
        # Menu Items
        self.actionUpload_file.triggered.connect(self.openfile.open)
        self.actionShow_History.triggered.connect(self.history.open)
        self.actionUpload_file_2.triggered.connect(self.load_history)
        self.create_new_account.triggered.connect(self.createnewaccount.open)
        self.user_management.triggered.connect(self.UserManagement.show)
        self.changePassword.triggered.connect(lambda *args: self.change_password(self.user))
        self.actionAbout.triggered.connect(lambda *args: self.about.show())
        #self.actionShow_Graph.triggered.connect(self.graph.open)
        if sys.platform == "win32":
            self.actionHelp.triggered.connect(lambda *args: os.startfile(resource_path('DigiFerro_Guide.pdf')))

        # Window Buttons
        self.analyzeButton.clicked.connect(self.openfile.open)
        self.fragmentButton.clicked.connect(lambda *args: self.show_image(image.SHOW_MASK))
        self.originalButton.clicked.connect(lambda *args: self.show_image(image.SHOW_ORIGINAL))
        self.graphButton.clicked.connect(lambda *args: self.show_image(image.SHOW_GRAPH))
        self.saveButton.clicked.connect(lambda *args: self.save_image())
        self.overallGraphButton.clicked.connect(lambda *args: self.show_totals())
        self.showReportButton.clicked.connect(lambda *args: self.generate_report())
        self.addToHistoryButton.clicked.connect(lambda *args: self.add_to_history())

        self.imageList.selectionChanged = self.list_selection
        # Set Drag n Drop
        # https://www.reddit.com/r/learnpython/comments/97z5dq/pyqt5_drag_and_drop_file_option/
        lw: QListWidget = self.imageList
        lw.setDragEnabled(True)
        lw.dragEnterEvent = lambda e: e.acceptProposedAction()
        lw.dragMoveEvent = lambda e: e.acceptProposedAction()
        lw.dropEvent = self.imagelist_drag_handler

        self.rectCBox.clicked.connect(lambda *args: self.show_image('refresh'))

        # DEBUG
        self.hsvDebugButton.clicked.connect(self.hsv_debug)
        self.hsvDebugButton.hide()

    def load_ui(self):
        uic.loadUi(resource_path('mainwindow.ui'), self)

    def imagelist_drag_handler(self, e: QDropEvent):
        if not self.openfile.ready:
            msgbox = QMessageBox(self)
            msgbox.setWindowTitle('Error')
            msgbox.setText('Please use "Analyze New Images" before attempting to drop new images')
            msgbox.exec()
        else:
            self.add_images(paths_to_imgs((url.path()[1:] for url in e.mimeData().urls()), self.openfile.scale))

    def list_selection(self, selected: QtCore.QItemSelection, deselected):
        self.image_id = selected.indexes()[0].row()
        self.show_image('refresh')
        self.update_counts()

    def add_images(self, images: List[image]):
        self.images += images

        for img in images:
            item = ImageListWidgetItem(str(img))
            item.attached_image = img
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Checked)
            self.imageList.addItem(item)

        # sort internal list and the image list
        self.images.sort(key=lambda i: i.sort_key)
        self.imageList.sortItems(QtCore.Qt.AscendingOrder)
        self.update_counts()
        self.show_image(image.SHOW_ORIGINAL, 0)

    def show_image(self, param, image_id=-1):
        if param == 'refresh' and self.totals_on:
            return
        if param == 'refresh':
            if self.prev_param is None:
                return
            param = self.prev_param
        else:
            self.prev_param = param
        self.totals_on = False
        if image_id == -1:
            image_id = self.image_id
        else:
            self.image_id = image_id
        if image_id == -1 or len(self.images) <= image_id:
            return

        if self.rectCBox.isChecked():
            img = self.images[image_id].get_image(param | image.SHOW_BOX_PLOTS)
        else:
            img = self.images[image_id].get_image(param)

        label: QLabel = self.label
        img_size = self.size()
        label_pos = label.pos()
        if param & image.SHOW_GRAPH:
            img_size.setHeight(img.shape[0])
            img_size.setWidth(img.shape[1])
        else:
            img_size.setHeight(img_size.height() - label_pos.y() - 10)
            img_size.setWidth(img_size.width() - label_pos.x() - 10)
        label.resize(img_size.width(), img_size.height())
        # resizing using QT instead of OpenCV
        img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_BGR888).scaledToHeight(img_size.height())
        label.setPixmap(QPixmap.fromImage(img))

    def resizeEvent(self, arg) -> None:
        self.show_image('refresh')
        return super().resizeEvent(arg)

    def show_totals(self):
        self.totals_on = True
        lw: QListWidget = self.imageList
        items = [lw.item(i) for i in range(lw.count())]
        dims = []
        for item in items:
            if item.checkState() == QtCore.Qt.Unchecked:
                continue
            dims.append(item.attached_image.get_dims())
        if len(dims) == 0:
            return
        dims = np.concatenate(dims)
        dist, bins = get_distribution(dims, self.openfile.scale)
        img = gen_graph(dist, bins)
        self.graph_img = img
        self.graph_data = dist, bins[1:]
        self.label.resize(img.shape[1], img.shape[0])
        img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_BGR888)
        self.label.setPixmap(QPixmap.fromImage(img))
        self.update_counts()

    def get_setting(self, key, default):
        try:
            return self.settings[key]
        except:
            return default

    def set_setting(self, key, value):
        self.settings[key] = value
        with open(SETTINGS_PATH, 'w') as settings:
            json.dump(self.settings, settings)

    def load_history(self):
        history_dir = self.get_setting('history_file_dir', '')
        fileName, _ = QFileDialog.getOpenFileName(self, directory=history_dir)
        
        if fileName == '':
            return

        self.set_setting('history_file_dir', extract_dir(fileName))
        self.history.set_history(History(fileName))
        self.history.open()
    
    def show(self):
        self.showMaximized()
        self.login.exec()
        # Test if a user got selected
        if getattr(self, 'user', None) is None:
            sys.exit()

    def save_image(self):
        if self.image_id == -1:
            return
        save_dir = self.get_setting('save_dir', '.')

        if self.totals_on:
            filename = "totals"
        else:
            filename = ".".join(str(self.images[self.image_id]).split('.')[:-1])

        file_path, _ = QFileDialog.getSaveFileName(self,
             directory=f'{save_dir}/{filename}.png',
             filter='PNG Image (*.png)')

        if file_path == '':
            return

        self.set_setting('save_dir', extract_dir(file_path))

        if self.totals_on is False:
            self.images[self.image_id].save_image(file_path)
        else:
            cv2.imwrite(file_path, self.graph_img)

    def update_counts(self):
        if self.totals_on and self.graph_img is not None:        
            dist, bins = self.graph_data
        else:
            dist, bins = self.images[self.image_id].graph_data

        counts = {str(b): str(d) for d, b in zip(dist, bins)}
        # Fancify in future
        label: QLabel = self.fragmentLabel
        labelText = f"Fragment counts: {', '.join(f'{k}: {v}' for k,v in counts.items())}"
        if not self.totals_on:
            labelText += f", Rubbing: {rubbing_precent(self.images[self.image_id].rubbing)}%"
        else:
            labelText += f", Ferrography conclusion: {fragment_decision(dist)} hrs"
        label.resize(label.fontMetrics().boundingRect(labelText).size())
        label.setText(labelText)

    def set_current_user(self, user: User):
        self.user = user
        if user.role & User.ROLE_CONFIRM:
            self.create_new_account.setVisible(True)
            self.user_management.setVisible(True)
        else:
            self.create_new_account.setVisible(False)
            self.user_management.setVisible(False)
    
    def change_password(self, user):
        cp = ChangePassword(self, user)
        cp.exec()
        cp.close()

    def hsv_debug(self):
        if self.image_id == -1:
            return
        img = self.images[self.image_id].get_image(image.SHOW_HSV)
        plt.imshow(img)
        plt.show()

    def set_report(self, report: Report):
        self.report = report

    def _get_dist(self):
        lw: QListWidget = self.imageList
        items = [lw.item(i) for i in range(lw.count())]
        dims = []
        for item in items:
            if item.checkState() == QtCore.Qt.Unchecked:
                continue
            dims.append(item.attached_image.get_dims())
        if len(dims) == 0:
            return
        dims = np.concatenate(dims)
        dist, _ = get_distribution(dims, self.openfile.scale)
        return dist

    def generate_report(self):
        if self.report is None:
            return
        dist = self._get_dist()
        self.report.conclusion = fragment_decision(dist)
        self.report.generateHtml().htmlTopdf().show_pdf()

    def add_to_history(self):
        if self.report is None:
            return
        dist = self._get_dist()
        self.report.conclusion = fragment_decision(dist)
        self.history.history.add_entry(HistoryEntry(self.report))

# Custom class to enable custom sorting
class ImageListWidgetItem(QListWidgetItem):
    @property
    def sort_key(self):
        return int("".join(c for c in self.text() if c.isnumeric()))
    def __lt__(self, other):
        try:
            return self.sort_key < other.sort_key
        except:
            return QListWidgetItem.__lt__(self, other)

class AboutWindow(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        uic.loadUi(resource_path('about.ui'), self)

        self.closeButton.clicked.connect(lambda *args: self.hide())

def main():
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication([])
    app.setWindowIcon(QIcon(resource_path('icon.png')))
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
