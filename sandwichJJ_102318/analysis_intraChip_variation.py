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


def get_singleJunc_devices(device_block):
    ## parse into dict
    numJJ_template = np.array([[1, 1, 1, 0],
                               [2, 2, 2, 0],
                               [4, 4, 0, 0],
                               [8, 8, 0, 0],
                               [15, 7, 3, 1],
                               [1, 0, 0, 0]])
    
    ## separate all measurements by number of junctions
    sorted_byNumJJ_dict = {} # key,value is num JJ, list of resistances
    num_rows = device_block.shape[0]
    num_cols = device_block.shape[1]
    for i in range(num_rows):
        for j in range(num_cols):
            num_jj = numJJ_template[i,j]
            if not num_jj in sorted_byNumJJ_dict.keys():
                sorted_byNumJJ_dict[num_jj] = []
            sorted_byNumJJ_dict[num_jj].append(device_block[i,j])
    ##END loop through single block
    
    ## only interested in single junction devices
    return np.array(sorted_byNumJJ_dict[1])
##END get_singleJunc_devices


def plot_chip_variation():
    ## load data
    dataFile_list = []
    base_name = "sandwichJJ_102318"
    codename_list = ["pbj","blt","sub","loaf"]
    color_list = ['red', 'purple', 'cyan', 'orange']
    quarterIndex_list = [3,4]
    for q in quarterIndex_list:
        for codename in codename_list:
            next_file = base_name+f"_{codename}_q{q}.dat"
            dataFile_list.append(next_file)
    ##END loop through codenames    
    
    ## load each file and convert to resistance
    for i,dataFile in enumerate(dataFile_list):
        # setup formating
        data_color = color_list[i%4]
        codename = codename_list[i%4]
        mark_forQuarter = ['*','x'][(i//4)%2]  # Q3 and Q4 respectively
        if mark_forQuarter == '*': continue # skip Q3 for now, too high variance from opens
        
        ## based on chip number, is exterior the first or last column?
        # on Q3 increasing column number corresponds to moving towards interior
        # on Q4 '  ' moving towards exterior
        # Q1 ~ Q3 and Q2~Q4 but we're not using either of those (bad liftoff)
        is_radial_ordering = [False, True][(i//4)%2]  # Q3 and Q4 respectively
        
        # load file
        with open(dataFile) as open_file:
            read = open_file.readlines()
            open_file.close()
    
        ## use regular expressions to extract 2 numbers (ints)
        re_template = "((\d+\.?\d*)\suV)" # decimal number, then space then 'uV'
        num_blocks = 5
        voltage_list = parse_input(read, re_template, num_blocks=num_blocks,num_cols=4)
        res, current = voltage_to_resistance_critCurr(voltage_list,bias_r=1E6)
        
        ## get single junction devices ordered by distance from center of chip
        # ie reverse Q3
        if is_radial_ordering:
            iter_res = iter(res) 
        else:
            iter_res = reversed(res)
            
        
        ## plot single squids as a function of chip position
        for i,single_column in enumerate(iter_res):
            singleJJ_res = get_singleJunc_devices(single_column)
            singleJJ_res /= 1E3 
            avg = np.nanmean(singleJJ_res)
            var = np.nanvar(singleJJ_res)
            plt.plot(i,var,marker=mark_forQuarter,ms=9,color=data_color)
            
        plt.xlabel("Radial position [from center]")
        plt.ylabel("Variance in Res. of Single SQuID [kOhms^2]")
    ##END loop through data files
    
    ## make a custom legend
    label_list = ["PBJ Q4\n($30^\circ$ evap, Std $O_2$)", 
                  "BLT Q4\n($30^\circ$ evap, 0.5 nm Al$O_x$)",
                  "SUB Q4\n($45^\circ$ evap, 0.5 nm Al$O_x$)",
                  "LOAF Q4\n($45^\circ$ evap, Std $O_2$)"]
    box_outline = dict(facecolor='white', alpha=0.8, boxstyle='round')
    x_pos,y_pos = 0.5,0.9 ## axis coordinates
    gap = 0.105
    ax = plt.gca()
    for i,label in enumerate(label_list):
        c = color_list[i%4]
        plt.text(x_pos,y_pos-i*gap,label, color=c,bbox=box_outline, transform=ax.transAxes)  
##END plot_chip_variation


def main():
    plot_chip_variation()
    
##END main
    
if __name__ == '__main__':
    main()


