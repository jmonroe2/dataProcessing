# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 08:21:24 2018

@author: jonathan
"""

import numpy as np
import matplotlib.pyplot as plt
import re

def voltage_to_resistance(v_obs_uv,bias_r=1E9):
    v_mon = 0.939E-3 # volts
    v = np.array(v_obs_uv)*1E-6/v_mon
    
    return bias_r/(1/v-1) ## from solving for Rs in voltage divider
##END resistance_to_voltage


def main():
    ## load data
    dataFile = "data_hotJJ_101918.dat"
    with open(dataFile) as open_file:
        read = open_file.readlines()
        open_file.close()
    paramp_str = read[3:36]
    jj_str = read[44:-1]
    
    ## use regular expressions to extract numbers
    re_template_paramp = "(\d{2,3})\D+(\d{2,3})"
    re_template_jj= "(\d{2,3})\D+(\d{2,3})\D+(\d{2,3})"    
    
    num_chips = 5
    paramp_list = [ [] for i in range(num_chips) ]
    
    chip_index = 0
    for target_str in paramp_str:
        if target_str[0] == "#":
            print chip_index, paramp_list            
            chip_index += 1
            continue
        found = re.findall(re_template_paramp, target_str) 
        if len(found):
            for add in found[0]:
                paramp_list[chip_index].append(float(add))
        else:
            ##@@ HACK INCOMING
            paramp_list[chip_index].append(-1)            
            paramp_list[chip_index].append(-1)
            continue
    ##END loop through paramp measurements
    ## convert to np array
    paramp_list = np.array([ np.array(l) for l in paramp_list])

    ## convert to real values    
    #paramp_list[np.where(paramp_list<0)] = np.nan
    resistance = voltage_to_resistance(paramp_list)
    crit_curr = 270.0/resistance ## magic number from paramp 09/12/18 lookup table
    
    print crit_curr
    ## plots
    avg = np.nanmean(crit_curr, axis=0)
    device_perChip = len(paramp_list[0])
    indices = np.arange(1,1+num_chips)*device_perChip
    
    print(avg)
    
    
##END main()
    
    
if __name__ == '__main__':
    main()
