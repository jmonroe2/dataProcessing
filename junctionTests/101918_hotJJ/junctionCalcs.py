# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 08:21:24 2018

@author: jonathan
"""

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import re

def voltage_to_resistance(v_obs_uv,bias_r=1E6):
    v_mon = 0.939E-3 # volts
    v = np.array(v_obs_uv)*1E-6/v_mon
    
    return bias_r/(1/v-1) ## from solving for Rs in voltage divider
##END resistance_to_voltage
    

def parse_input(input_list, regex_template, num_blocks,num_cols):
    measure_list = [ [] for i in range(num_blocks) ]
    chip_index = 0
    for target_str in input_list:
        if "#" in target_str:
            chip_index += 1
            continue
        found = re.findall(regex_template, target_str) 
        if len(found):
            for gp,add in found:
                measure_list[chip_index].append(float(add))
        else:
            print(target_str,"had no template matches")
    ##END loop through paramp measurements
    
    ## np arrays should have equal length vectors to make matrix
    for measured in measure_list:
        while(len(measured) < num_cols):
            measured.append(np.nan)
    ## convert to np array
    
    return  np.array([ np.array(l) for l in measure_list])
##END parse_input
    
    
def make_plot(data, num_chips, ic_fun=None):
    resistance = voltage_to_resistance(data)
    crit_curr = 270.0/resistance ## magic number from paramp 09/12/18 lookup table
    if ic_fun is not None:
        ic_fun(crit_curr)
    target = crit_curr ## what to plot
    target = resistance/1000
    
    ## plots
    label_list = ['Baseline 1/2', '50 C, 15 sec', '50 C, 2 min', \
                  '50 C, 5 min',  'Baseline 2/2']
    num_device_perChip = len(data[0])
    avg = np.nanmean(target, axis=1)
    var = np.nanvar(target, axis=1)
    std = np.sqrt(var/num_device_perChip)
    for i,devices in enumerate(target):
        indices = (i+1)*np.ones(num_device_perChip)
        plt.plot(indices,devices, 'ko', alpha=0.2)
    xs = np.arange(1,num_chips+1)
    plt.errorbar(xs,avg, yerr=std, alpha=0.8,fmt='o',ms=15)
    
    ## legend
    plt.title("Single SQuID")
    plt.xticks(xs,label_list)
    ax = plt.gca()
    #ax.set_yscale('log')
    #ax.set_ylabel("$i_c$ [$\mu$ a]")
    ax.set_ylabel("Resistance [k$\Omega$]")
    #plt.show()  
##END make_plot


def main():
    ## load data
    dataFile = "data_hotJJ_101918.dat"
    with open(dataFile) as open_file:
        read = open_file.readlines()
        open_file.close()
    paramp_str = read[2:36]
    jj_str = read[39:-1]
    
    ## use regular expressions to extract 2 numbers (ints)
    #re_template_paramp = "(\d{2,3})\D+(\d{2,3})"
    #re_template_jj = "(\d{2,3})\D+(\d{2,3})\D+(\d{2,3})"
    re_template = "((\d+\.?\d*)\suV)" 
    
    num_blocks = 5
    paramp_list = parse_input(paramp_str, re_template, num_blocks,num_cols=12)
    jj_list= parse_input(jj_str, re_template, num_blocks,num_cols=9)
    
    ## ad hoc processing
    paramp_list[0]  /= 10 ## probed with 100k bias resistor
    paramp_list[-1] /= 10 ## probed with 100k bias resistor
    jj_list[0] /= 10      ## probed with 100k bias resistor
    #paramp_list[np.where(paramp_list<0)] = np.nan
    #jj_list[np.where(jj_list<0)] = np.nan    
    def scale_ic(x): return 12*x ## for array of squids, Ic of device is Ic of single squid
    
    ## plots
    make_plot(paramp_list, num_blocks,scale_ic)
    make_plot(jj_list, num_blocks)    
    plt.title("Single (blue), Array (red)")
    plt.show()
##END main()
    
    
if __name__ == '__main__':
    main()
