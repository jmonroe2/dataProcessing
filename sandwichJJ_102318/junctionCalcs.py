# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 08:21:24 2018

@author: jonathan
"""

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import re

def voltage_to_resistance_critCurr(v_obs_uv,bias_r=1E6):
    v_mon = 0.939E-3 # volts
    v = np.array(v_obs_uv)*1E-6/v_mon
    res = bias_r/(1/v-1) ## from solving for Rs in voltage divider
    i_c = 270.0/res ## magic number from paramp 09/12/18 lookup table
    
    
    return res, i_c 
##END resistance_to_voltage
    

def parse_input(input_list, regex_template, num_blocks,num_cols=None):
    '''
    A function to extract all voltage measurements from a list of .dat file lines
    input_list: string list of rows of .dat file
    regex_template: template to search for
    num_blocks: how many comments to expect
    (num_cols): if you'd like a matrix, this parameter will pad cols with nan
    
    return
    3D matrix where each "block" (first index) contains a matrix structured
        in the same way as the input .dat file (second index is line #, third
        index is inter-row number)
    '''
    measure_list = [ [] for i in range(num_blocks) ]
    block_index = 0
    
    for target_str in input_list:
        ## comment lines after initial comment header:
        if "#" in target_str and len(measure_list):
            block_index += 1
            continue
        ## findall returns any match
        found = re.findall(regex_template, target_str) 
        if len(found):
            new_row = []
            for group,addition in found:
                new_row.append( float(addition) )
            measure_list[block_index].append(new_row)
        else:
            print(target_str,"has no template matches")
    ##END loop through measurements
    
    ## np arrays should have equal length vectors to make matrix
    if num_cols:
        for i,measured in enumerate(measure_list):
            for j,row in enumerate(measured):
                while(len(row) < num_cols):
                    row.append(np.nan)
                measured[j] = np.array(row)
            measure_list[i] = np.array(measured)
            
    return  np.array(measure_list)
##END parse_input
    
    
def make_plot(data, num_chips, ic_fun=None,x_labels=None):
    '''
    data: matrix of points to plot with index 0 is repe
    '''
    num_device_perChip = len(data[0])
    avg = np.nanmean(data, axis=0)
    var = np.nanvar(data, axis=0)
    std = np.sqrt(var/num_device_perChip)
    
    for i,devices in enumerate(data):
        indices = (i+1)*np.ones(num_device_perChip)
        plt.plot(indices,devices, 'ko', alpha=0.2)
    xs = np.arange(1,num_chips+1)
    plt.errorbar(xs,avg, yerr=std, alpha=0.8,fmt='o',ms=15)
    
    ## legend
    plt.title("Single SQuID")
    if x_labels:
        plt.xticks(xs,x_labels)
    ax = plt.gca()
    #ax.set_yscale('log')
    ax.set_ylabel("$I_c$ [$\mu$ A]")
    plt.show()  
##END make_plot

def main():
    ## load data
    dataFile = "blt_column1.dat"
    with open(dataFile) as open_file:
        read = open_file.readlines()
        open_file.close()

    ## use regular expressions to extract 2 numbers (ints)
    re_template = "((\d+\.?\d*)\suV)" # decimal number, then space then 'uV'
    num_blocks = 2
    voltage_list = parse_input(read, re_template, num_blocks=1,num_cols=3)
    res, current = voltage_to_resistance_critCurr(voltage_list[0],bias_r=1E6)
    
    ## parse into dict
    numJJ_template = np.array([[1, 1, 1, 0],
                               [2, 2, 2, 0],
                               [4, 4, 0, 0],
                               [8, 8, 0, 0],
                               [8, 4, 2, 1],
                               [1, 0, 0, 0]])
    
    numJunctions_dict = {}
    
    ## plots
    make_plot(current, num_blocks)
    #make_plot(jj_list, num_chips)    
    plt.title("Single (blue), Array (red)")
##END main()
    
    
if __name__ == '__main__':
    main()
