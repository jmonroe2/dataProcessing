# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 13:31:56 2018

@author: JTM

This script exists to analyze phase noise in paramp 091218C
"""

import numpy as np
import matplotlib.pyplot as plt



def parse_smith(data):
    real = data[0::2]
    imag = data[1::2]
    
    
    linmag = np.sqrt(real**2 + imag**2)
    logmag = 10*np.log10(linmag)
    phase = np.angle( real + 1j*imag)
    
    ## unwrap electrical delay
    ed = 67 ## units: nanoseconds
    fs = np.linspace(1.95, 2.05, 501) ## units: GHz
    
    ## test cases
    uw_phase,diff = unwrap_phase(phase)
    delayed = phase + ed*2*np.pi*fs 
    
    uw_delayed = uw_phase + ed*2*np.pi*fs
    delayed_uw,tmp = unwrap_phase(delayed)
    
    out_dict= {}
    out_dict["real"]= real
    out_dict["imag"]= imag
    out_dict["linmag"]= linmag
    out_dict["logmag"]= logmag
    out_dict["phase"]= phase
    
    out_dict["uw"] = uw_phase
    out_dict["ed"] = delayed
    out_dict["uwed"] = uw_delayed
    out_dict["eduw"] = delayed_uw
    return out_dict
##END parse_smith
    
def unwrap_phase(phase_rad):
    '''
    NOTE: np.unwrap exists, but this function provides explicit details
    Process:
        1. Find jumps
        2. Add +/- pi to eliminate jumps
    '''
    unwrapped = np.copy(phase_rad)
    diffs = []
    for i,p in enumerate(unwrapped):
        diff =  p-unwrapped[i-1]
        if diff > np.pi: # jump up
            unwrapped[i:] -= 2*np.pi
        elif diff < -1*np.pi: # jump down
            unwrapped[i:] += 2*np.pi
        diffs.append(diff)
    return unwrapped, np.array(diffs)
##END unwrap_phase

def main():
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
        smith_dict = parse_smith(sweep)
        phase = smith_dict["phase"] 
        phase_fluxSweep[:,i] = phase
    
    ## make plots
    phase = smith_dict["phase"]
    uwed = smith_dict["uwed"]
    eduw = smith_dict["eduw"]
    
    ax_left = plt.gca()
    plt.plot(fs, uwed, label="unwrapped")
    ax_right = ax_left.twinx()
    plt.plot(fs+0.01, eduw,label="electrical delay", color='orange')
    #plt.imshow(phase_fluxSweep, extent=[fmin,fmax,0,71],aspect='auto')
    
    plt.show()
    return phase
##END main

if __name__ == '__main__':
    foo = main()

