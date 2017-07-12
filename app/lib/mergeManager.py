import os
import cv2          # import the OpenCV module
import numpy as np  # import the numpy module using the name 'np'.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure





class mergeManager(object):
    
    def __init__(self):
        self
        
    def addWeighted(self, img1, img2, outputFileName, a):
        img = cv2.addWeighted(img1,a,img2,1-a,0)
        cv2.imwrite(outputFileName,img)
        return img
  

