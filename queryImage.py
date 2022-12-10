import cv2
import numpy
import random

SCALE_MULTIPLIER = 30

class QueryImage:
    __original = None
    __imageResized = None

    def __init__(self, image):
        self.__original = image.astype(numpy.float32) / 255
        imageResized = cv2.resize(image, (image.shape[0] * 30, image.shape[1] * 30), interpolation=cv2.INTER_NEAREST)

        cv2.imshow('imageResized', imageResized)

        self.__imageResized = numpy.zeros([imageResized.shape[0] * 2, imageResized.shape[1] * 2, 3], dtype=numpy.uint8)

        h = self.__imageResized.shape[0]
        w = self.__imageResized.shape[1]

        for y in range(0, h):
            for x in range(0, w):
                if (1/4) * h < y < (3 / 4) * h and (1 / 4) * w < x < (3 / 4) * w:
                    self.__imageResized[y][x] = imageResized[int(numpy.floor(y - (1/4) * h))][int(numpy.floor(x - (1/4) * w))]
                else:
                    self.__imageResized[y][x] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]


    def getOriginalImage(self):
        return self.__original

    def getImage(self):
        return self.__imageResized

