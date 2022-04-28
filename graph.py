import io

from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
import matplotlib.pyplot as plt
import numpy as np

class GraphWindow(QDialog):
    def __init__(self, parent, graph=None):
        super(GraphWindow, self).__init__(parent)
        self.parent = parent
        self.load_ui()

        ## THIS IS DUMMY GRAPH FOR DEMO PURPOSES ##
        nums = np.arange(6)
        nums2 = np.flip(nums)
        width = 0.3

        plt.bar(nums, nums, width, label='Rubbing')
        plt.bar(nums + width, nums2, width, label='Spalling')
        plt.legend(loc='upper left')
        plt.xlabel('Fragment size')
        plt.ylabel('Fragment count')
        plt.xticks(nums + (width / 2), ['100', '150', '200', '250', '300', '350'])

        io_buf = io.BytesIO()
        io_buf.seek(0)
        plt.savefig(io_buf, format='raw', transparent=False)
        fig = plt.gcf()
        dim = (fig.get_size_inches() * fig.dpi).astype(int)
        img = np.reshape(np.frombuffer(io_buf.getvalue(), dtype=np.uint8), newshape=(dim[1], dim[0], -1))
        ## END OF DUMMY GRAPH CODE ##

        self.label.setGeometry(20, 20, img.shape[1], img.shape[0])
        qimg = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGBA8888)
        self.label.setPixmap(QPixmap.fromImage(qimg))

    def load_ui(self):
        uic.loadUi('graph.ui', self)
    
    def open(self):
        self.show()