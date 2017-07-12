import os
import cv2          # import the OpenCV module
import numpy as np  # import the numpy module using the name 'np'.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure





class isometricsManager(object):
    
    def __init__(self):
        self

        
    def translation(self, img, x, y):
        rows, cols, channels = img.shape
        M_trans = np.float32([[1, 0, x], [0, 1, y]])
        dst_trans = cv2.warpAffine(img, M_trans, (cols, rows))
        return dst_trans


    # ROTATION
    # Rotate the image by 45 degrees
    # params are center of rotation, angle and scale
    def rotation(self, img, degree):
        rows, cols, channels = img.shape
        M_rot = cv2.getRotationMatrix2D((cols/2, rows/2), degree, 1)
        dst_rot = cv2.warpAffine(img, M_rot, (cols, rows))
        return dst_rot

