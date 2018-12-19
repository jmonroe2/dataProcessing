#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 11:13:31 2018

@author: jmonroe

This utility script exists to organize 
"""
import numpy as np
import re

def voltage_to_resistance_critCurr(v_obs_uv,bias_r=1E6):
    '''
    DESC: this function converts output of the 
    INPUT: 
        v_obs_uv: the measured voltage from the probe statation, units uV
        bias_   : bias resistor used in resistance measurement
    '''
    v_mon = 0.939E-3 # volts
    v = np.array(v_obs_uv)*1E-6/v_mon
    res = bias_r/(1/v-1) ## from solving for Rs in voltage divider
    i_c = 270.0/res ## magic number from paramp 09/12/18 lookup table
    ## 270 ~ delta/(pi/2) for a superconducting gap of Al
    
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
##END parse_input
    