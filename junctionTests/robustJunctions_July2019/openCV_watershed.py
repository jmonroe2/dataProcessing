#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 17:19:42 2018

@author: jmonroe

This script exists to count area of JJ from SEM images
"""


'''
Open CV's modified watershed algorithm: 
        Watershed: given a potential landscape one slowly increases a height threshold.
                As different local minima are surpassed, area on either side is combined.
                Continuing gives a segmentation hierarchy
        CV's modification:
                Do a bit of filtering for "definite signal" and "definite background"
                Enables smoother watershedding (one "flooding event")
'''

#import PIL
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import cv2 as cv

# string of 4 paramp junctions
#data_dir = "/Users/jmonroe/Projects/machineLearning/areaCounting/data/091718_paramp/"
#data_name = "deviceC_JJ10,12.tif"

# single quarter
data_dir = "/Users/jmonroe/Google Drive/research/cleanRoom_data/072419_developTest/die_row2col1_SEM/chip_evap_0deg_row2Col3/tilt0_rot0/"
data_name = "row2Col3_brJJ_quarter4.jpg"

def my_data(show=False, return_stamp=False):
    ## load data
    raw_image = cv.imread(data_dir+data_name)

    ## cut off SEM label
    ## transform RGB image to single grayscale
    label_width = 64
    image_noLabel= raw_image[:-label_width]
   
    ## extract a single junction
    left,right = 370, 570
    up, down = 800, 880
    single_JJ = image_noLabel[up:down, left:right]
    
    if show:
        plt.figure()
        plt.title("Without SEM label")
        plt.imshow(image_noLabel, cmap='gray')
        plt.figure()
        plt.title("Single JJ")
        plt.imshow(single_JJ,cmap='gray')

    if return_stamp:
        return image_noLabel, single_JJ
    else:
        return image_noLabel
##END my_data
    

def main():
    ## load datqa
    #img = cv.imread("water_coins.jpg")
    img,singleJJ = my_data(show=False, return_stamp=True)

    # let's look at a small part
    '''
    ## try 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xs = np.linspace(0,1,200)
    ys = np.linspace(0,1,80)
    xy = np.array( np.meshgrid(xs,ys)[0] )
    ax.plot_surface(xy,xy,singleJJ)
    plt.title("Cut")
    plt.show()
    return 0;
    #'''
    
    ## convert to openCV's favorite version 
    gray =  cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    plt.figure()
    plt.title("Gray")
    plt.imshow(gray, cmap='gray')


    ## threshold the devices to find only exposed region:
    ## short story: Gaussian blur then filter gives clean-looking segmentation
    ##              the true magic, is the OTSU method
    blur = cv.GaussianBlur(gray,(5,5),0)
    ret, thresh = cv.threshold(blur,0,255,type=cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
    plt.figure()
    plt.title("thresh")
    plt.imshow(thresh, cmap='gray') 
    return 0;
    '''
    #ret, thresh = cv.threshold(gray,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
    ret, thresh = cv.threshold(gray,0,255,type=cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
    plt.figure()
    plt.title("thresh")
    plt.imshow(thresh, cmap='gray') 

    ## try a Gaussian blur first
    blur = cv.GaussianBlur(gray,(5,5),0)
    ret, thresh_blur = cv.threshold(blur,0,255,type=cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
    plt.figure()
    plt.title("blur --> thresh")
    plt.imshow(thresh_blur, cmap='gray')

    ## or perhaps an adaptive thresholding
    th3 = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,11,2)
    plt.figure()
    plt.title("Adaptive")
    plt.imshow(th3, cmap='gray')
    '''
    
    
    ## first estimation of noise
    '''
    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv.morphologyEx(thresh,cv.MORPH_OPEN,kernel, iterations = 2)
    plt.figure()
    plt.imshow(opening, cmap='gray')
    plt.title("Opening")
    # sure background area
    sure_bg = cv.dilate(opening,kernel,iterations=3)
    plt.figure()
    plt.imshow(sure_bg, cmap='gray')
    plt.title("sure_bg")
    '''
    # Finding sure foreground area
    dist_transform = cv.distanceTransform(opening,cv.DIST_L2,5)
    ret, sure_fg = cv.threshold(dist_transform,0.7*dist_transform.max(),255,0)
    plt.figure()
    plt.imshow(sure_fg, cmap='gray')
    plt.title("sure_fg")
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv.subtract(sure_bg,sure_fg)
    
    # Marker labelling
    ret, markers = cv.connectedComponents(sure_fg)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1
    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0
    
    markers = cv.watershed(img,markers)
    img[markers == -1] = [255,0,0]
    
    plt.figure()
    plt.imshow(markers, cmap='gray')
    plt.title("Markers")
##
    
if __name__ == '__main__':
    #my_data(True)
    main()
    plt.show()

