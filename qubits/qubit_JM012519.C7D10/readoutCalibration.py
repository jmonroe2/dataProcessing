#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 21:48:26 2019

@author: jonathan

This script exists to 
"""
import sys, time, os
import numpy as np
import matplotlib.pyplot as plt


def main():
    data_path = "Z:\jmonroe\qubit_jm012519.C7D10\cavitySpec"
    qubitGnd_filename = "\powerSweep_-30,20dBm_vna_5.855,5.858GHz_bnc_off_bias_3mA_v2"
    qubitEx_filename = "\powerSweep_-30,20dBm_vna_5.855,5.858GHz_bnc_-38dBm_4.980GHz_bias_3mA_v2"
    
    power_min, power_max = -30,20
    freq_min, freq_max = 5.855, 5.858

    data_qubitGnd = np.loadtxt(data_path+qubitGnd_filename)
    data_qubitEx = np.loadtxt(data_path+qubitEx_filename )
    fs = np.linspace(freq_min, freq_max, data_qubitGnd.shape[0]//2)
    fs = np.round(fs, 6)
    power = np.linspace(power_min, power_max, data_qubitGnd.shape[1]) 

    re = data_qubitGnd[::2, :]
    im = data_qubitGnd[1::2, :]
    cavity_qubitGnd = np.sqrt(im**2+re**2)
    re = data_qubitEx[::2, :]
    im = data_qubitEx[1::2, :]
    cavity_qubitEx = np.sqrt(im**2+re**2)
    
        #print(fs[150]); return 0;

    ## full sweep    
    fig = plt.figure()
    #plt.imshow(cavity_qubitGnd, extent=[power_min, power_max,freq_min, freq_max]\
    plt.imshow(cavity_qubitGnd.T \
               ,cmap='bwr', aspect='auto', origin="lower")
    plt.xlabel("Freq [GHz]")
    plt.ylabel("VNA Power [dBm-30 dB]")
    fig = plt.figure()
    plt.imshow(cavity_qubitEx.T, extent=[freq_min, freq_max,power_min, power_max]\
               ,cmap='bwr', aspect='auto', origin="lower")
    plt.xlabel("Freq [GHz]")
    plt.ylabel("VNA Power [dBm-30 dB]")
    
    ## frequency shift
    fig = plt.figure()
    print( "Powers", power[0], power[20])
    plt.plot(fs, cavity_qubitGnd[:,0])
    plt.plot(fs, cavity_qubitGnd[:, 20])
    plt.xlabel("Freq [Ghz]")
    plt.ylabel("Lin mag [$S_{11}$]")
        
    fig = plt.figure()
    flux_choice1 = 103
    flux_choice2 = 300
    print( "Frequencies", fs[flux_choice1], fs[flux_choice2])
    plt.plot(power, cavity_qubitGnd[flux_choice1, :], 'b--')
    plt.plot(power, cavity_qubitEx[flux_choice1, :], 'b-', label=f'{fs[flux_choice1]} GHz')
    plt.plot(power, cavity_qubitGnd[flux_choice2, :], 'r--')
    plt.plot(power, cavity_qubitEx[flux_choice2, :], 'r-', label =f'{fs[flux_choice2]} GHz')
    plt.legend(title="Dash:gnd, Solid:ex")
    plt.xlabel("VNA Power [dBm-30dB]")
    plt.ylabel("Lin mag [$S_{11}$]")
    plt.show()
    
##END main
    
if __name__ == '__main__':
    main()

