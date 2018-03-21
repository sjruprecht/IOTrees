"""Builds a numpy array suitable for training

"""

import argparse
import re
from glob import glob
from pathlib import Path
import cv2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--images', required=True, help='Path to input images')

    args = ap.parse_args()

    images_path = Path(args.images)

    box_files = sorted(
        glob(str(images_path / 'boxes' / '*.xml')),
        key=lambda bf: int(bf.split('_')[-1].split('.')[0]))

    not_found = 0
    loaded = 0

    for box_file in box_files:
        with open(box_file) as bf:
            bf_contents = bf.read()

        image_path = images_path / Path(box_file).with_suffix('.JPEG').name

        image_contents = cv2.imread(str(image_path))

        if image_contents is None:
            not_found += 1
            continue

        loaded += 1

        xmin = int(re.findall('<xmin>(\d+)</xmin>', bf_contents)[0])
        xmax = int(re.findall('<xmax>(\d+)</xmax>', bf_contents)[0])
        ymin = int(re.findall('<ymin>(\d+)</ymin>', bf_contents)[0])
        ymax = int(re.findall('<ymax>(\d+)</ymax>', bf_contents)[0])

        cropped = image_contents[ymin:ymax, xmin:xmax, :]

        cv2.imwrite(
            str(images_path / 'cropped' / Path(box_file).with_suffix('.jpg').name),
            cropped
        )

    print(f'Loaded {loaded} images.')
    print(f'{not_found} images could not be loaded.')


if __name__ == '__main__':
    main()
