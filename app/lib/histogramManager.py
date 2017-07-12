import os
import cv2          # import the OpenCV module
import numpy as np  # import the numpy module using the name 'np'.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


class histogramManager(object):
    
    def __init__(self):
        self
        
    def buildCDF(self, img, cIndex, title):
        hist= cv2.calcHist([img], [cIndex], None, [256], [0, 256])
        cdf = hist.cumsum()
        cdf_normalized = cdf * hist.max()/ cdf.max()
        
        fig = plt.figure()
        
        plt.plot(cdf_normalized, color = 'b')
        plt.hist(img.flatten(),256,[0,256], color = 'r')
        plt.xlim([0,256])
        plt.legend(('cdf','histogram'), loc = 'upper left')
        plt.title(title) 
        canvas = FigureCanvas(fig)
        return canvas

    """
    http://docs.opencv.org/trunk/d7/d4d/tutorial_py_thresholding.html
    http://www.learnopencv.com/opencv-threshold-python-cpp/
    
    """ 
    def getThresholdMask(self, img1, thresh):
        #img1 = cv2.imread('img/coin.jpg')
    
        img1b = cv2.medianBlur(img1,5)
        img1b = cv2.GaussianBlur(img1b,(5,5),0)
        
        maxValue = 255
        
        # Apply thresholding on the background and display the resulting mask
        ret, mask = cv2.threshold(img1b, thresh, maxValue, cv2.THRESH_BINARY)
        return mask
        
    def getThresholdCanvas(self, img, thresh):
        ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        ret,thresh2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
        ret,thresh3 = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
        ret,thresh4 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
        ret,thresh5 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)
        
        titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
        images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
        
        fig = plt.figure()
        for i in xrange(6):
            plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
            plt.title(titles[i])
            plt.xticks([]),plt.yticks([])
        #canvas = FigureCanvas(fig)
        return fig
        