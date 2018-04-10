import yaml
import cv2
from pathlib import Path
from textwrap import dedent

with open('boxes.yml') as f:
    boxes = yaml.load(f)

folder = Path('data/custom/')

for box in boxes:
    image = cv2.imread(str(folder / box['name']))

    with open((folder / 'annotations' / box['name']).with_suffix('.xml'), 'w') as f:
        f.write(dedent(f'''
        <annotation>
            <folder>eab</folder>
            <filename>{box["name"]}</filename>
            <size>
                <width>{image.shape[1]}</width>
                <height>{image.shape[0]}</height>
                <depth>{image.shape[2]}</depth>
            </size>
            <segmented>0</segmented>
            <object>
                <name>eab</name>
                <pose>Unspecified</pose>
                <truncated>0</truncated>
                <difficult>0</difficult>
                <bndbox>
                    <xmin>{box["xmin"]}</xmin>
                    <ymin>{box["ymin"]}</ymin>
                    <xmax>{box["xmax"]}</xmax>
                    <ymax>{box["ymax"]}</ymax>
                </bndbox>
            </object>
        </annotation>
        ''').strip())
