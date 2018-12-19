#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 13:57:05 2018

@author: jmonroe

This script exists to process spectroscopy data from qubit JM 102318.A
"""
import sys, time, os
import numpy as np
import matplotlib.pyplot as plt
import re

sys.path.append("..")
import vna_helper

def spectroscopy():
    data_base_dir = "/Users/jmonroe/Projects/fabrication/paramps/dataProcessing/qubit_JM102318A/twoTone_spectroscopy/"
    #for my_file in os.listdir(data_base_dir):
    if True:
        my_file = "vna_7.095775GHz_-55dBm_BNC_-25dBm_6.5,7.5_dwell_2s.data"
        fmin,fmax = 6.5,7.5
        smith_data = np.loadtxt(data_base_dir+my_file)
        fs = np.linspace(fmin,fmax,smith_data.size//2)
        
        smith_dict = vna_helper.parse_smith(smith_data,fs)
        logmag = smith_dict['real']
        plt.figure()
        plt.plot(fs, logmag)
    plt.show()    
##END spectroscopy
    
    
def power_sweep():
    base_dir = data_base_dir = "/Users/jmonroe/Projects/fabrication/paramps/dataProcessing/qubit_JM102318A/twoTone_spectroscopy/"
    file_name = "sweep_power_0,-50dBm_freq_7.0892,7.0992GHz_savePhase.data"
    
    sweep = np.loadtxt(base_dir+file_name)
    print(sweep.shape)
    f_min, f_max = 7.0892,7.0992
    p_min, p_max = 0,-50
    fs = np.linspace(f_min, f_max,sweep.shape[0])
    ps = np.linspace(p_min, p_max, sweep.shape[1])
    plt.imshow(sweep.T, aspect='auto', extent=[f_min,f_max, p_max,p_min],cmap='bwr_r')
    plt.xlabel("Freq [GHz]")
    plt.ylabel("VNA Power [dBm]")
    
    plt.figure()
    plt.plot(sweep[:,10])
    plt.show()
    
##END power_sweep()
    
def main():
    #spectroscopy() ## this turned out to be bad data
    power_sweep()
    
    
if __name__ == '__main__':
    main()

