import cv2
import numpy as np
import os
from typing import Dict
from mashcima.Model import Model


_IMAGES: Dict[int, np.ndarray] = {}


def _load_images():
    ITEMS = 16
    DIGITS = 10
    img = cv2.imread(
        os.path.join(os.path.dirname(__file__), "mnist.png"),
        cv2.IMREAD_GRAYSCALE
    )
    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    # for col in range(ITEMS):
    #     for row in range(DIGITS):
    #         _IMAGES[row] = []
    #         _IMAGES[row].append(
    #             img[col * 28]
    #         )

    print(img[16, :])


_load_images()


class MnistDigitModel(Model):
    def call(self):
        pass
