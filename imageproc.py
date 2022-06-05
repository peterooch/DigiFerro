from os import path
from typing import List

import cv2
import numpy as np
from joblib import Parallel, delayed

from preprocess.hsv_pipeline import apply_clahe, contour_dims, create_masks, equalize_img, get_rects
from util import gen_graph, get_distribution

BLACK_PIXEL = np.uint8([0, 0, 0])

class image:
    '''
    Image Class
    -----------
    Contains data and methods to retreive data related to single image.

    This class contains image data such as:
      0. The actual image
      1. Spalling and Rubbing binary masks
      2. Annotated contour boxplots for spalling fragments
      3. Fragment bin limits and distribution
      4. Filename (used for sorting/identification)
    
    In addition the class has methods for:
      1. Generation of graph using fragment distribution
      2. Overlay boxplots on the fragment mask or the image
      3. Saving graph/mask/original image to disk
    '''

    __slots__ = ("scale", "filename", "img", "mask", "show_mode",
                 "drawed_image", "dims", "dist", "bins", "box_plots", "rubbing")

    def __init__(self, image_path, scale):
        with open(image_path, 'rb') as file:
            image_bytes = file.read()
        
        self.scale = scale
        _, self.filename = path.split(image_path)
        self.img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        self.mask, self.rubbing = create_masks(self.img)
        self.show_mode = image.SHOW_ORIGINAL
        self.drawed_image = None

        self.dims = contour_dims(self.mask)
        self.dist, self.bins = get_distribution(self.dims, self.scale)
        self.box_plots = get_rects(self.mask, self.scale)

    @property
    def graph_data(self):
        return self.dist, self.bins[1:]

    def __str__(self):
        return self.filename
    
    @property
    def sort_key(self):
        return int("".join(c for c in self.filename if c.isnumeric()))     

    def save_image(self, filename):
        if self.drawed_image is None:
            return

        cv2.imwrite(filename, self.drawed_image)

    # Flags for use with get_image
    SHOW_ORIGINAL  = (1 << 0)
    SHOW_MASK      = (1 << 1)
    SHOW_GRAPH     = (1 << 2)
    SHOW_BOX_PLOTS = (1 << 3)
    SHOW_HSV       = (1 << 4)

    def get_image(self, option=None):
        if option is None:
            option = image.SHOW_ORIGINAL
        self.show_mode = option

        if option & image.SHOW_GRAPH:
            img = self.create_graph()
            self.drawed_image = img
            return img

        if option & image.SHOW_MASK:
            combined_mask = self.mask | (self.rubbing // 2)
            img = cv2.cvtColor(combined_mask, cv2.COLOR_GRAY2BGR)
        else:
            img = self.img

        if option & image.SHOW_BOX_PLOTS:
            img = self.apply_box_plots(img)

        if option & image.SHOW_HSV:
            # For the HSV Debug option
            img = apply_clahe(cv2.cvtColor(equalize_img(self.img), cv2.COLOR_BGR2HSV))

        self.drawed_image = img
        # img should be in BGR format
        return img

    def apply_box_plots(self, image):
        # Make plots a text clearer using a mask
        mask = cv2.cvtColor(cv2.inRange(self.box_plots, BLACK_PIXEL, BLACK_PIXEL), cv2.COLOR_GRAY2BGR)
        return (image & mask) | self.box_plots

    def get_dims(self):
        return self.dims

    def create_graph(self):
        return gen_graph(self.dist, self.bins)

def paths_to_imgs(paths, scale) -> List[image]:
    # Use all but 1 core for image processing
    return Parallel(n_jobs=-2, verbose=0, prefer='threads')(delayed(image)(path, scale) for path in paths)
