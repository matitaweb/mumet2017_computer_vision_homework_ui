import os
import cv2          # import the OpenCV module
import numpy as np  # import the numpy module using the name 'np'.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


class noisefilterManager(object):
    
    def __init__(self):
        self
        
    def median(self, img):
        thMedianBlur = cv2.medianBlur(img,7)
        double = np.hstack((img,thMedianBlur)) #stacking images side-by-sid
        return double

    def mean(self, img):
        blur = cv2.blur(img,(5,5))
        double = np.hstack((img,blur)) #stacking images side-by-sid
        return double
        
    # Applying a threshold on an image like OTSU
    def otsuFilter(self, img):
        thresh = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)[1]
        double = np.hstack((img,thresh)) #stacking images side-by-side
        return double
        
        
        # Gaussian Filter
    def gaussianFilter(self, img):
        filtered = cv2.GaussianBlur(img, (1, 1), 1.0)
        double = np.hstack((img,filtered)) #stacking images side-by-side
        return double
        
        
        # adaptive
    def adaptiveMeanFilter(self, img):
        th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,15,10) 
        double = np.hstack((img,th2)) #stacking images side-by-side
        return double
        
    def adaptiveGaussianFilter(self, img):   
        th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,15,10)
        double = np.hstack((img,th3)) #stacking images side-by-side
        return double
        
    def bilateralFilter(self, img):    
        bilateral = cv2.bilateralFilter(img, 10, 15, 15)
        double = np.hstack((img,bilateral)) #stacking images side-by-side
        return double
  

