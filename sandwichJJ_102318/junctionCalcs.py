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
    
    measurement_list = [ [] ] # intialize to a list of one empty list
    block_index = 0
    for target_str in input_list:
        #print(len(measurement_list)); return 0;
        if "#" in target_str: # comment line
            if len(measurement_list[0]): ## not the first lines of the file
                measurement_list.append([])
                block_index += 1
            continue
        ## findall returns any match
        found = re.findall(regex_template, target_str) 
        if len(found):
            new_row = []
            for group,addition in found:
                new_row.append( float(addition) )
            measurement_list[block_index].append(new_row)
        else:
            #print(target_str,"has no template matches")
            measurement_list[block_index].append([])
    ##END loop through measurements
    
    ## np arrays should have equal length vectors to make matrix
    if num_cols:
        size_array = (block_index+1,len(measurement_list[0]), num_cols)
        output = np.zeros(size_array)
        for i in range(size_array[0]):
            for j in range(size_array[1]):
                k=0
                while k < size_array[2]:
                    try:
                        output[i,j,k] = measurement_list[i][j][k]
                    except IndexError:
                        output[i,j,k] = np.nan
                    k += 1
    else:
        return measurement_list
    return output
                    
    '''
    for i,measure_block in enumerate(measurement_list):
        for j,row in enumerate(measure_block):
            while(len(row) < num_cols):
                row.append(np.nan)
            measure_block[j] = np.array(row)
        measurement_list[i] = np.array(measure_block)
    return measurement_list
    print(measurement_list); return measurement_list;
    '''
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
    dataFile = "sandwichJJ_102318_blt_q3Only.dat"
    with open(dataFile) as open_file:
        read = open_file.readlines()
        open_file.close()

    ## use regular expressions to extract 2 numbers (ints)
    re_template = "((\d+\.?\d*)\suV)" # decimal number, then space then 'uV'
    num_blocks = 5
    voltage_list = parse_input(read, re_template, num_blocks=num_blocks,num_cols=4)
    return voltage_list;
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
    ms = main()
