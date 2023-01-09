import json
from pathlib import Path
from typing import Dict

import numpy as np

import click
import cv2 as cv
from tqdm import tqdm


def detect(img_path: str) -> Dict[str, int]:
    """Object detection function, according to the project description, to implement.

    Parameters
    ----------
    img_path : str
        Path to processed image.

    Returns
    -------
    Dict[str, int]
        Dictionary with quantity of each object.
    """
    wartKolor = [0,0,0,0]

    arr_low_h = [31, 20, 162, 174]
    arr_high_h = [56, 26, 176, 179]

    arr_low_s = [85, 153, 82, 174]
    arr_high_s = [255, 255, 235, 226]

    arr_low_v = [17, 100, 0, 108]
    arr_high_v = [175, 255, 121, 215]

    arr_dilation = [4, 3, 12, 10]
    arr_erosion = [5, 6, 4, 2]

    # Pobieranie zdjęcia
    img = cv.imread(img_path, cv.IMREAD_COLOR)
    imgR = cv.resize(img, (0, 0), fx=0.25, fy=0.25, interpolation=cv.INTER_AREA)

    imgB = cv.blur(imgR, (5, 5), cv.BORDER_DEFAULT)

    frame_HSV = cv.cvtColor(imgB, cv.COLOR_BGR2HSV)

    for i in range(4):
        kernelE = np.ones((arr_erosion[i], arr_erosion[i]), np.uint8)
        kernelD = np.ones((arr_dilation[i], arr_dilation[i]), np.uint8)

        frame_threshold = cv.inRange(frame_HSV, (arr_low_h[i], arr_low_s[i], arr_low_v[i]),
                                     (arr_high_h[i], arr_high_s[i], arr_high_v[i]))

        erosion = cv.erode(frame_threshold, kernelE, iterations=1)
        dilation = cv.dilate(erosion, kernelD, iterations=1)

        contours, _ = cv.findContours(dilation, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

        if i == 0: green = len(contours)
        if i == 1: yellow = len(contours)
        if i == 2: purple = len(contours)
        if i == 3: red = len(contours)



    #TODO: Implement detection method.
    
    # red = 0
    # yellow = 0
    # green = 0
    # purple = 0

    return {'red': red, 'yellow': yellow, 'green': green, 'purple': purple}


@click.command()
@click.option('-p', '--data_path', help='Path to data directory', type=click.Path(exists=True, file_okay=False, path_type=Path), required=True)
@click.option('-o', '--output_file_path', help='Path to output file', type=click.Path(dir_okay=False, path_type=Path), required=True)
def main(data_path: Path, output_file_path: Path):
    img_list = data_path.glob('*.jpg')

    results = {}

    for img_path in tqdm(sorted(img_list)):
        fruits = detect(str(img_path))
        results[img_path.name] = fruits

    with open(output_file_path, 'w') as ofp:
        json.dump(results, ofp)


if __name__ == '__main__':
    main()
