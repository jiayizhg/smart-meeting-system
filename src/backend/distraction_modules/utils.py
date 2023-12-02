import numpy as np
import cv2

def dist(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def binary(image):
    _, bin_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    return bin_image
