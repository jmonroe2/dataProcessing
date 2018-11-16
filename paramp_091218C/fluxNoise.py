# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 13:31:56 2018

@author: JTM

This script exists to analyze phase noise in paramp 091218C
"""

import numpy as np
import matplotlib.pyplot as plt


def process_paramps():
    data_dir = r"C:\Data\2018\paramp_jm091218.1c_100918\noiseAt2GHz_BNC_2.0GHz_-20.60dBm_fluxUnknown"
    data_dir.replace("\\","/")
    file_name = "vna_1.95,2.05Ghz_-50dBm"
    fmin,fmax= 1.95,2.05
    
    ## load data
    data = np.loadtxt(data_dir + '/' + file_name)
    phase_fluxSweep = np.zeros((data.shape[0]//2, data.shape[1]))
    
    ## at each flux bias measure phase
    fs = np.linspace(fmin,fmax, data.shape[0]//2)
    for i in range(data.shape[1]):
        sweep = data[:,i]
        smith_dict = parse_smith(sweep,fs)
        phase = smith_dict["phase"] 
        phase_fluxSweep[:,i] = phase
    
    ## make plots
    phase = smith_dict["phase"]
    
    ax_left = plt.gca()
    plt.plot(fs, uwed, label="unwrapped")
#    ax_right = ax_left.twinx()
#    plt.plot(fs+0.01, ed,label="electrical delay", color='orange')
#    #plt.imshow(phase_fluxSweep, extent=[fmin,fmax,0,71],aspect='auto')
    plt.legend()
    
    plt.show()
##END process_paramps
    

def process_testData():
    data_dir = r"C:\Data\2018\101818_testData"
    data_dir.replace(r"\\","/")
    file_name = "trans_cavityTL092518_7.96,8.06GHz_0dBm_electricalDelay_0ns.dat"
    fmin,fmax= 7.96,8.06
    
    ## load data
    data = np.loadtxt(data_dir + '/' + file_name)   
    fs = np.linspace(fmin,fmax, len(data)//2)
    smith_dict = parse_smith(data,fs,electrical_delay=67)
    
    ## make plots
    phase = smith_dict["phase"]
    shifted_phase = smith_dict["shifted_phase"]
    
    ax_left = plt.gca()
    plt.plot(fs, shifted_phase)
#    ax_right = ax_left.twinx()
#    plt.plot(fs+0.01, ed,label="electrical delay", color='orange')
#    #plt.imshow(phase_fluxSweep, extent=[fmin,fmax,0,71],aspect='auto')
    plt.legend()
    
    plt.show()
##END process_testData
    
def main():
    #process_paramps()
    process_testData()
##END main

if __name__ == '__main__':
    phase = main()

