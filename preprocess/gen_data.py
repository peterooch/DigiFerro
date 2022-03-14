import os
import sys

import numpy as np
from encoder import json_to_img
from transform import augmentation
#from model import get_model
from joblib import dump

old_cwd = os.getcwd()

def create_data(label_path):
    os.chdir(label_path)
    dataset = [json_to_img(entry) for entry in os.listdir('.') if '.json' in entry]
    augmented = [augmentation(entry) for entry in dataset]
    dataset += augmented

    X = []
    Y = []
    #model = get_model()

    input_shape  = (512, 512)
    #output_shape = (760, 568)

    #os.makedirs('blocks/x', exist_ok=True)
    #os.makedirs('blocks/y', exist_ok=True)

    c = 0
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
                c += 1
            prev_a = a

    X = np.array(X)
    Y = np.array(Y)
    os.chdir(old_cwd)
    dump((X, Y), "data/data.pkl", compress=3)
    #model.fit(X, Y, batch_size=1)

if __name__ == "__main__":
    create_data(sys.argv[1])