"""Generates a training dataset of EAB images"""

from glob import glob

import cv2
from keras.datasets import cifar100
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras import backend as K


def main():
    K.set_image_data_format('channels_last')

    num_pos = 560
    num_neg = 1000

    # Build positive examples
    files = glob('data/custom/cropped/*.jpg')
    input_files = np.zeros((len(files), 32, 32, 3))

    for i, file in enumerate(files):
        image = cv2.imread(file)
        resized = cv2.resize(image, (32, 32))
        input_files[i, :, :, :] = resized

    datagen = ImageDataGenerator(
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest',
        data_format='channels_last',
    )

    datagen.fit(input_files)

    positive = np.zeros((num_pos, 32, 32, 3), dtype=int)
    generator = datagen.flow(input_files, batch_size=1)

    for i in range(num_pos):
        positive[i, :, :, :] = next(generator)

    # Build negative examples
    (cifar, _), _ = cifar100.load_data(label_mode='fine')
    rand_idx = np.random.randint(cifar.shape[0], size=num_neg)
    negative = cifar[rand_idx, :, :, :]

    # negative[:, :, :, [0, 1, 2]] = negative[:, :, :, [2, 0, 1]]

    # Join positive and negative examples and make labels
    images = np.vstack((positive, negative))
    labels = np.hstack((
        np.ones((num_pos,)),
        np.zeros((num_neg,)),
    ))

    # Save for training
    np.savez('train.npz', images=images, labels=labels)


if __name__ == '__main__':
    main()
