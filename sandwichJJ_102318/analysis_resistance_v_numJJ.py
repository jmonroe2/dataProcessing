# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 08:21:24 2018

@author: jonathan
"""

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import re
from probing_util import voltage_to_resistance_critCurr, parse_input

    
def addToPlot_res_numJJ(resistance,style_dict=None):
    ## convert to k Ohms
    res = resistance/1E3
    
    ## parse into dict
    numJJ_template = np.array([[1, 1, 1, 0],
                               [2, 2, 2, 0],
                               [4, 4, 0, 0],
                               [8, 8, 0, 0],
                               [15, 7, 3, 1],
                               [1, 0, 0, 0]])
    
    ## separate all measurements by number of junctions
    sorted_byNumJJ_dict = {} # key,value is num JJ, list of resistances
    for chip_column in res:
        num_rows = chip_column.shape[0]
        num_cols = chip_column.shape[1]
        for i in range(num_rows):
            for j in range(num_cols):
                num_jj = numJJ_template[i,j]
                if not num_jj in sorted_byNumJJ_dict.keys():
                    sorted_byNumJJ_dict[num_jj] = []
                sorted_byNumJJ_dict[num_jj].append(chip_column[i,j])
        ##END loop through single block
    ##END loop through all chip columns
    
    for num_jj in sorted_byNumJJ_dict.keys():
        resistance_list = sorted_byNumJJ_dict[num_jj]
        xs = num_jj*np.ones(len(resistance_list),dtype='int')
        plt.scatter(xs,resistance_list,c='black',alpha=0.6,s=9)
        
        ## plot average
        avg = np.nanmean(resistance_list)        
        std = np.nanstd(resistance_list)
        plt.errorbar(num_jj,avg, yerr=std, **style_dict)
    ##END loop through number of junctions
    plt.xlabel("Number of SQuIDs")
    plt.ylabel("RT Resistance [k$\Omega$]")
##END plot_resistance_vs_numJunctions
    
    
def plot_resistance_vs_numJunctions():
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
    
    for i,dataFile in enumerate(dataFile_list):
        # setup formating
        data_color = color_list[i%4]
        codename = codename_list[i%4]
        outline = [0, 1.5][(i//4)%2] ## Q3 is empty, Q4 gets thick outline
        
        # load file
        with open(dataFile) as open_file:
            read = open_file.readlines()
            open_file.close()
    
        ## use regular expressions to extract 2 numbers (ints)
        re_template = "((\d+\.?\d*)\suV)" # decimal number, then space then 'uV'
        num_blocks = 5
        voltage_list = parse_input(read, re_template, num_blocks=num_blocks,num_cols=4)
        res, current = voltage_to_resistance_critCurr(voltage_list,bias_r=1E6)
        
        ## do specific analysis
        style_dict = dict(color=data_color, markeredgewidth=outline, ms=15,
                      alpha=0.8, fmt='o',markeredgecolor='k')
        addToPlot_res_numJJ(res,style_dict=style_dict)
    ##END loop through files
    
    ## make a custom legend
    label_list = ["PBJ Q4\n($30^\circ$ evap, Std $O_2$)", 
                  "BLT Q4\n($30^\circ$ evap, 0.5 nm Al$O_x$)",
                  "SUB Q4\n($45^\circ$ evap, 0.5 nm Al$O_x$)",
                  "LOAF Q4\n($45^\circ$ evap, Std $O_2$)"]
    box_outline = dict(facecolor='white', alpha=0.8, boxstyle='round')
    x_pos,y_pos = 0.5,0.9 ## axis coordinates
    gap = 0.1
    ax = plt.gca()
    for i,label in enumerate(label_list):
        c = color_list[i%4]
        plt.text(x_pos,y_pos-i*gap,label, color=c,bbox=box_outline, transform=ax.transAxes)  
        
    ## more labels
    plt.title("Sandwich Junction test 10/23/18")
    plt.xlabel("Number of SQuIDs")
    plt.ylabel("RT Resistance [k$\Omega$]")
    plt.xlim(0,9)
    plt.ylim(-10,300)
##END plot_resistance_vs_numJunctions

    
def main():
    plot_resistance_vs_numJunctions()
##END main()
    
    
if __name__ == '__main__':
    main()