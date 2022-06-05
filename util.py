import sys
from os import path
import io

from matplotlib import pyplot as plt
import cv2
import numpy as np

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)

def extract_dir(filepath):
    return path.split(filepath)[0]

def gen_graph(dist, bins):
    plt.yscale('log')
    plt.bar(np.arange(len(dist)), dist)   
    plt.xticks(np.arange(len(bins[1:])), [f'{dim:.1f}' for dim in bins[1:]])
    plt.xlabel('Fragment size (upto)')
    plt.ylabel('Fragment count')
    plt.title('Fragment count by size in micrometers')
    io_buf = io.BytesIO()
    io_buf.seek(0)
    plt.savefig(io_buf, format='raw', transparent=False)
    fig = plt.gcf()
    dim = (fig.get_size_inches() * fig.dpi).astype(int)
    plt.clf()
    img = np.reshape(np.frombuffer(io_buf.getvalue(), dtype=np.uint8), newshape=(dim[1], dim[0], -1))
    # Convert to BGR to avoid special handling later on
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    return img

def get_distribution(dims, scale):
    '''
    `scale` is the pixel/micrometer ratio in the source image
    '''
    # Bin limits in micrometers
    BINS = np.array([0, 75, 105, 120, float('inf')])
    dist, _ = np.histogram(dims, bins=(BINS * scale))
    return dist, BINS

def rubbing_precent(rubbing_mask):
    all_ones = np.ones_like(rubbing_mask)
    rubbing_ones = rubbing_mask / 255
    return int((rubbing_ones.sum() / all_ones.sum()) * 100)
