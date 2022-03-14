import os

import numpy as np
import cv2
from encoder import DataEntry
import random

def rotation(img, angle):
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w >> 1, h >> 1), angle, 1)
    img = cv2.warpAffine(img, M, (w, h))
    return img

def flip(img, flag):
    image = cv2.flip(img, flag)
    return image

def augmentation(images):
    imgA, imgB = images
    angle = random.uniform(0, 360)
    flag = random.randint(-1, 1)
    imageA = rotation(flip(imgA, flag), angle)
    imageB = rotation(flip(imgB, flag), angle)
    return DataEntry(imageA, imageB)

