#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 22:19:11 2019

@author: jonathan

This script exists to 
"""
import sys, time, os
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import optimize


def main():
    data_dir = "C:/Users/jonathan/Downloads"
    data = np.loadtxt(data_dir+"/T1_fluxSweep_-7,4mA_2PartSeq_ampSweep_25usT1_20times_v1/bar_0")
    num_fluxes = data.shape[0]
    fluxes = np.linspace(-7,4, num_fluxes)
    print(data.shape)
    num_measurements = 20
    num_steps = 202
    ts = np.linspace(0,25,101)
        
    #fig, ax_all = plt.subplots()
    #ax_all.imshow(data, aspect="auto")
        
    fig, ax_fluxTuned = plt.subplots()
    
    def my_fit(x,a,b):
        return a*np.exp(-b*x)
    
    for i in range(num_fluxes):
        for j in range(num_measurements):
            if j==0: continue
            initial_index = num_steps//2 + j*num_steps
            final_index = (j+1)*num_steps
            single_t1 = data[i, initial_index:final_index]
            param, covariance = scipy.optimize.curve_fit(my_fit, ts, single_t1,  p0=(0.8,0.1 ))
            std_err = np.sqrt(covariance[1,1])
            ax_fluxTuned.errorbar(fluxes[i], 1/param[1], yerr=std_err/param[1]**2)
    ax_fluxTuned.set_ylim(0,15)
    
    ax_fluxTuned.set_xlabel("Flux bias [mA]")
    ax_fluxTuned.set_ylabel("1/$\Gamma$ [us]")
    ax_fluxTuned.plot(fluxes,25*np.ones(len(fluxes)), 'k--')
    ax_fluxTuned.annotate("Seq. Length", (0,25))
    plt.show()
        
##END main
    
    
if __name__ == '__main__':
    main()

