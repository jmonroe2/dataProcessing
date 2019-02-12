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
    #data_dir = "C:/Users/jonathan/Downloads"
    data_dir = "/Users/jmonroe/Projects/fabrication/dataProcessing/qubits/qubit_JM012519.C7D10/data"

    ## load data
    # -12 to -2 mA bias sweep
    '''
    data_dir += "/T1_fluxSweep_-12,-2_ampSweep_0,1_t1_25us_v2"
    flux_min, flux_max = -12,-2
    num_fluxes = 41
    num_files= 14
    num_measurements = 10
    '''
    # -2.5 to +4 mA bias sweep
    data_dir += "/T1_fluxSweep_-2.5,4mA_amp_0,1_25us_t1"
    flux_min, flux_max = -2.5,4
    num_fluxes = 66
    num_files = 17
    num_measurements = 10
    #'''

    num_seq_steps = 202
    t1_time = 25
    
    fig, axis = plt.subplots()
    for index in np.arange(num_files):
        file_name = f"/bar_{1000*index}"
        fluxes = np.linspace(flux_min, flux_max, num_fluxes) #+ 0.25*0.35/14*index
        fit_t1_repeatedSequence(data_dir+file_name, axis, fluxes, num_seq_steps,
                        num_measurements, t1_time)

    plt.show()
##END main
        
    
def fit_t1_repeatedSequence(file_path,axis=None, fluxes=None,num_seq_steps=0,num_measurements=0, t1_time=0):
    '''
    ## DESC: extracts T1 portion of repeated sweeps
    ## INPUT:
            "file_path": full path to 2D matrix of ["num_measurements"*2part sequence length, number flux points)
    '''
    
    data = np.loadtxt(file_path)
    seq_parts = 2
    print(len(fluxes), data.shape,"index 1?")
    num_fluxes = len(fluxes)
    ts = np.linspace(0,t1_time,num_seq_steps//seq_parts)
        
    if not axis:
        fig, axis = plt.subplots()
    
    def my_exp(x,a,b,c):
        return a*np.exp(-b*x) + c
    
    gamma_table = np.zeros((num_fluxes,num_measurements))
    for i in range(num_fluxes):
        for j in range(num_measurements):
            ## separate T1 sequence from everything else.
            initial_index = num_seq_steps//seq_parts + j*num_seq_steps
            final_index = (j+1)*num_seq_steps
            single_t1 = data[i, initial_index:final_index]
            
            ## T1 fit
            initial_guess = (0.5, 0.5, 0.1)
            try:
                param, covariance = scipy.optimize.curve_fit(my_exp, ts, single_t1,
                                                         p0=initial_guess)
                gamma = param[1] 
                #gamma_stdErr = np.sqrt(covariance[1,1])
                #t1_err = gamma_stdErr/gamma**2
            except RuntimeError:
                print(f"Bad fit @{np.round(fluxes[i],1)} mA, fit #{j+1}")
                gamma = np.nan
                ## store fit results
            gamma_table[i,j] = gamma
            #axis.errorbar(fluxes[i], 1./gamma, yerr=t1_err)
    ## statistics on repeated measurements
    t1_list =  1./np.mean(gamma_table,axis=1)
    
    dGamma = np.std(gamma_table,axis=1) /np.sqrt(num_measurements)
    t1_std  = dGamma/gamma**2
    axis.errorbar(fluxes, t1_list, yerr=t1_std,fmt='o')

    axis.set_ylim(0,30)
    axis.set_xlabel("Flux bias [mA]")
    axis.set_ylabel("1/$\Gamma$ [us]")
    axis.plot(fluxes,25*np.ones(len(fluxes)), 'k--')
    axis.annotate("Seq. Length", (0,25))
##END plot_t1_vs_flux    
##END main
    
    
if __name__ == '__main__':
    main()

