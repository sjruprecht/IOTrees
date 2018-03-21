"""Trains a CNN to detect EABs"""

import numpy as np
import cv2

with open('train.npz', 'rb') as f:
    data = np.load(f)
    images = data['images']
    labels = data['labels']

print(images.shape)
print(labels.shape)

for i in range(images.shape[0]):
    cv2.imwrite(f'temp/test-{i}.png', images[i, :, :, :])
