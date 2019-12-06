#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 14:30:38 2019

@author: jmonroe

This script exists to parse and analyze data from the "Transmon test 01/19/19"
fab run.
"""
import sys, time, os
import numpy as np
import matplotlib.pyplot as plt
e = enumerate 

def some_Fun():
	'''
	DESCRIPTION: 
	INPUT:
	OUTPUT:
	TODO:
	'''
	pass
##END 
    

def parse_data_file(data_file):
    
    
    with open(data_file,'r') as open_file:
        read_lines = open_file.readlines()

    res_list  = []        
    row_index = -1
    for line in read_lines:
        if "Ohms" not in line:  continue
            
        tab_split = line[:-1].split("\t") ## cutoff '\n'

        ## remove ' Ohms' from each column entry
        row_measurements = [float(r[:-4]) for r in tab_split if len(r)]
        res_list.append(row_measurements)
        
    return res_list
##END parse_data_file
    

def spatial_plot(resistance_array, matrix_shape, open_resistance=np.nan):
    fig, spatial_ax = plt.subplots()
    for i,row in enumerate(resistance_array):
        for j,resistance in enumerate(row): 
            ms = resistance_to_markersize(resistance)
            if resistance and resistance > open_resistance: 
                spatial_ax.plot(j, i, 'o', ms=10, markerfacecolor='w', alpha=0.7,color='k')
                continue
            spatial_ax.plot(j, i, 'o', ms=ms,color='k', alpha=0.7)

    spatial_ax.invert_yaxis()
    spatial_ax.set_ylabel("Row Number", fontsize=20)
    spatial_ax.set_xticks(range(matrix_shape[0]))
    labels = ["Col "+str(i) for i in range(1,matrix_shape[0]+1) ]
    spatial_ax.set_xticklabels(labels, fontsize=14 )
    
    ## custom legend
    plt.text(0.15, -0.3, "Size $\propto$ Res. [Ohms]",fontsize=14)
##END spatial_plot

    
def resistance_to_markersize(resistance):
    ## let's make resistance in [0, 1200] make markers of [1,40]
    if not resistance:
        return 0.0
    
    max_res = 10000
    max_marker = 40
    return resistance/max_res *max_marker +1
##END resistance_to_markersize
    

def hist_plot(resistance_array, matrix_shape, open_resistance=20E3):
    min_res, max_res = 100,5E3

    ## remove nan and open circuits
    resistance_array = resistance_array[~np.isnan(resistance_array)]
    filtered_resistance = resistance_array[resistance_array<open_resistance]
  
    ## make plot 
    fig, hist_axes = plt.subplots()
    bins = np.linspace(min_res,max_res,30)
    hist_axes.hist(filtered_resistance, bins=bins)

    ## collect open resistance
    open_res = resistance_array[resistance_array > open_resistance]
    hist_axes.annotate(f'{open_res.size} open circuits',xy=(max_res, open_res.size), xycoords='data', 
            xytext=(bins[-15],open_res.size), size=14,va='center',
            arrowprops=dict(arrowstyle="->", linewidth=4))

    hist_axes.set_xlabel("Resistance [$\Omega$]")
    hist_axes.set_ylabel("Counts")
##END hist_plot
    

def main():
    data_dir = "/Users/jmonroe/Projects/fabrication/dataProcessing/junctionTests/transmonTest_011919/"
    data_file_name = "copiedData.txt"
    matrix_shape = 7,21
    
    ## get resistance data from 01/19/19 formatted data 
    resistance_array = parse_data_file(data_dir+data_file_name)
    
    ## reshape resistance array to match data: outermost die in matrix are None
    for i,row in e(resistance_array):
        num_blank_elem = matrix_shape[0] - len(row)
        if num_blank_elem: 
            for j in range(num_blank_elem):
                row.append(np.nan)
            n = num_blank_elem//2
            row = row[-n:] + row[:-n]
            
        resistance_array[i] = np.array(row)
    resistance_array = np.array(resistance_array)
    tmp = resistance_array[ np.where( resistance_array < 5E3) ]
    
    ## plots
    #spatial_plot(resistance_array, matrix_shape, open_resistance=20E3)
    hist_plot(resistance_array, matrix_shape, open_resistance=10E3)
    
    plt.show()
    
##END main
    

if __name__ == '__main__':
    main()

