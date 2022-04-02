import os
import sys

import numpy as np
#from model import get_model
from joblib import dump
import cv2
import shutil

from constants import SPLIT_SIZE
from encoder import json_to_img
from transform import augmentation

old_cwd = os.getcwd()

def create_data(label_path, dest_path=None):
    os.chdir(label_path)
    dataset = [json_to_img(entry) for entry in os.listdir('.') if '.json' in entry]
    augmented = [augmentation(entry) for entry in dataset]
    dataset += augmented

    X = []
    Y = []
    #model = get_model()

    input_shape  = SPLIT_SIZE
    #output_shape = (760, 568)

    #os.makedirs('blocks/x', exist_ok=True)
    #os.makedirs('blocks/y', exist_ok=True)

    for entry in dataset:
        x_img = entry.source
        y_img = entry.target
        s_height, s_width = x_img.shape[:2]
        d_height, d_width = input_shape
        
        prev_a, prev_b = 0, 0
        for a in range(d_height, s_height, d_height):
            for b in range(d_width, s_width, d_width):
                x = x_img[prev_a:a, prev_b:b]
                y = y_img[prev_a:a, prev_b:b]
                prev_b = b
                if y.shape != input_shape:
                    continue
                X.append(x)
                #y = cv2.resize(y, tuple(reversed(output_shape)))
                #y = np.reshape(y, model.output_shape[1:])
                Y.append(y)
                #cv2.imwrite(f'blocks/x/{c}.png', x)
                #cv2.imwrite(f'blocks/y/{c}.png', y)
            prev_a = a

    X = np.array(X)
    Y = np.array(Y)
    os.chdir(old_cwd)
    shutil.rmtree(dest_path, ignore_errors=True)
    os.makedirs('data')
    dump((X, Y), "data/data.pkl", compress=3)

    os.makedirs(f'{dest_path}/transformed')
    for i, (image, _) in enumerate(dataset):
        cv2.imwrite(f'{dest_path}/transformed/{i}.jpg', image)

    if dest_path is not None:
        os.makedirs(f'{dest_path}/images')
        os.makedirs(f'{dest_path}/masks')
        for i, (image, mask) in enumerate(zip(X, Y)):
            cv2.imwrite(f'{dest_path}/images/{i}.png', image)
            cv2.imwrite(f'{dest_path}/masks/{i}.png', mask)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        create_data(sys.argv[1], sys.argv[2])
    else:
        create_data(sys.argv[1])
