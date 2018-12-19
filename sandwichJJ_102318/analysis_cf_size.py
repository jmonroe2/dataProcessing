#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 11:05:27 2018

@author: jmonroe

This script exists to investigate how resistance varies across position within a chip.
"""
import sys, time, os
import numpy as np
import matplotlib.pyplot as plt
from probing_util import voltage_to_resistance_critCurr, parse_input
import matplotlib
matplotlib.style.use("ggplot")

def sem_image_data():
    ## width, length of device 1,2,3 (single JJ) for each column
    col1 = [(None, None),(None, None),(None, None),(None, None)] ## data too messy
    col2 = [(65 , 95), (72 , 96), (63 , 95)] ## device 1,2,3
    col3 = [(65 , 86), (73 , 94), (70 , 92)]
    col4 = [(72 , 94), (72 , 93), (78 , 93)]
    col5 = [(40 , 68), (34 , 56), (32 , 52)]
    return [col1, col2, col3, col4, col5]
##END sem_image_data


def plot_res_area(plot_var=True):
    dataFile = "sandwichJJ_102318_sub_q4.dat" ## we collected SEM images of these
    ## load file 
    with open(dataFile) as open_file:
        read = open_file.readlines()
        open_file.close()
    all_dimensions = sem_image_data()
    area_err = 6*6 ## estimated error in pixels (see oneNote)
    scale_pix_to_um = 3/122.

    ## use regular expressions to extract 2 numbers 
    re_template = "((\d+\.?\d*)\suV)" # decimal number, then space then 'uV'
    num_blocks = 5
    voltage_list = parse_input(read, re_template, num_blocks=num_blocks,num_cols=4)
    res, current = voltage_to_resistance_critCurr(voltage_list,bias_r=1E6)

    ## plot single squids as a function of chip position
    for i,single_column in enumerate(res):
        if i==0: continue
        singleJJ_res = single_column[0, :-1] ## columns are 4 wide, but only 3 devices here
        singleJJ_res /= 1E3   ## convert to kOhms
        chip_dimensions = all_dimensions[i]
        for j,res in enumerate(singleJJ_res):
            area = chip_dimensions[j][0] * chip_dimensions[j][1] *scale_pix_to_um**2
            err = area_err* scale_pix_to_um**2
            plt.plot(area, res,'ok') 

    ## add a "line to guide the eye"
    ts = np.linspace(1,4.5,100)
    plt.plot(ts, 70/ts,'k--', label=r'$\frac{70}{A}$')
    plt.legend(fontsize=20)
        
    plt.xlabel("Area [$\mu m^2$]")
    plt.ylabel("Resistance [$k\Omega$]")
    plt.title("Sandwich JJ 10/23/18 Sub Q4")
    plt.show()
    
##END plot_res_area


def main():
    plot_res_area()
    
##END main
    
if __name__ == '__main__':
    main()


