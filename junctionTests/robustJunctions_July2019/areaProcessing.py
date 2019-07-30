#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(username)s

This script exists to 
"""
import sys, time, os
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

def main_old():
    ## a 'good' junction image from the paramp study
    data_file = "/Users/jmonroe/Projects/machineLearning/areaCounting/data/josephsonJunction_subQ4_C3D2.png"

    data = cv.imread(data_file)
    #plt.imshow(data[:,:,0],cmap='gray')

    dx = 200
    dy = 250
    x0 = 610
    y0 = 200
    clip = data[y0:y0+dy, x0:x0+dx, 0]
    plt.imshow(clip, cmap='gray')
  
    plt.figure() 
    plt.hist(clip.flatten(), bins=50)
    plt.show() 
##END main_old


def main():
    ## a junction robustness test image of one quarter;
    ##    is this mag high enough to count variation of one junction?
    data_file = "/Users/jmonroe/Google Drive/research/cleanRoom_data/072419_developTest/die_row2col1_SEM/chip_evap_0deg_row2Col3/tilt0_rot0/row2Col3_brJJ_quarter1.jpg"
    
    print(data_file)
    data =  cv.imread(data_file)
    #plt.imshow(data[:,:,0],cmap='gray')

    dx = 250
    dy = 250
    x0 = 275
    y0 = 700
    clip = data[y0:y0+dy, x0:x0+dx, 0]
    #plt.imshow(clip, cmap='gray')
   
    #plt.hist(clip.flatten(), bins=50)
    thresh = 130

    filtered = clip
    filtered[ np.where(clip > thresh)] = 0.
    plt.imshow(filtered,cmap='gray')
    plt.show()
    
##END main
    

if __name__ == '__main__':
    main()
