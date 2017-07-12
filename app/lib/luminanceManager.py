import os
import cv2          # import the OpenCV module
import numpy as np  # import the numpy module using the name 'np'.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


class luminanceManager(object):
    
    def __init__(self):
        self
    
    def addLuminance(self, img, luninanceAdd):
    
        # cambio in YUV per poter maneggiare la luminosita'
        yuv = cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
    
        t = 0 # per prendere in considerazione la luninosita'
        yuv = yuv.astype(float) #trasformo gli elementi della matrice da uint8 a float per poter aggiungere il valore di aumento
      
        # aggiungo la luminosita'
        yuv[..., t] = yuv[..., t] + luninanceAdd
       
        # faccio la normalizzazione
        m = np.amax(yuv[..., t])
        yuv[..., t] = yuv[..., t] * 255 / m
        
        #ritrasformo in unit8
        yuv = yuv.astype(np.uint8)
    
        #ritrasformo in BRG poiche' e' l'unico modo di salvare correttamente le immagini
        bgr = cv2.cvtColor(yuv,cv2.COLOR_YUV2BGR)
        
        return bgr
    
    def negative(self, img):
        result = 255-img
        return result

