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

def get_data(verbose):
    data_dir = "C:/Users/jonathan/Downloads"
    #data_dir = "/Users/jmonroe/Projects/fabrication/dataProcessing/qubits/qubit_JM012519.C7D10/data"

    ## load data
    # -12 to -2 mA bias sweep
    #'''
    data_dir += "/T1_fluxSweep_-12,-2_ampSweep_0,1_t1_25us_v2"
    flux_min, flux_max = -12,-2
    num_fluxes = 41
    num_files= 14
    '''
    # -2.5 to +4 mA bias sweep
    data_dir += "/T1_fluxSweep_-2.5,4mA_amp_0,1_25us_t1"
    flux_min, flux_max = -2.5,4
    num_fluxes = 66
    num_files = 17
    #'''

    num_seq_steps = 202
    t1_time = 25
    fluxes = np.linspace(flux_min, flux_max, num_fluxes) 
    gamma_longRepeats= []
    gammaErr_longRepeats= []
    
    for index in np.arange(num_files):
        file_name = f"/bar_{1000*index}"
        ## get table of (repeated) gamma vs (single) flux
        gamma, gammaErr = fit_gamma_repeatedSequence(data_dir+file_name, num_seq_steps, t1_time, verbose=verbose)
        gamma_longRepeats.append(gamma)
        gammaErr_longRepeats.append(gammaErr)

    return fluxes, gamma_longRepeats, gammaErr_longRepeats
##END get_data

 
def make_plot_of_averages(fluxes,gamma_list):
    fig, flux_axis = plt.subplots()
    fig, time_axis = plt.subplots()
    
    num_measurements = gamma_list[0].shape[1]

    for index,gamma in enumerate(gamma_list):
        ## statistics
        avg_gamma = np.mean(gamma,axis=1)
        avg_t1 = 1./avg_gamma
        dGamma = np.std(gamma,axis=1) /np.sqrt(num_measurements)
        t1_std  = dGamma/avg_gamma**2
    
        ## add to plot
        flux_axis.errorbar(fluxes, avg_t1, yerr=t1_std,fmt='o')
        flux_index = 8
        time_axis.errorbar(index*1.5, avg_t1[flux_index], yerr=t1_std[flux_index], fmt='o')

    ## plot formatting
    flux_axis.set_ylim(0,30)
    flux_axis.set_xlabel("Flux bias [mA]")
    flux_axis.set_ylabel("$T_1 [\mu s]$")
    flux_axis.plot(fluxes,25*np.ones(len(fluxes)), 'k--')
    flux_axis.annotate("Seq. Length", (0,25))

    time_axis.set_ylim(0,30)
    time_axis.set_xlabel("Sample time [hours]")
    time_axis.set_ylabel("$T_1 [\mu s]$")
    time_axis.set_title(f"$T_1$ @ {fluxes[flux_index]} mA")
    plt.show()
##END make_plot_of_averages
        
    
def fit_gamma_repeatedSequence(file_path, num_seq_steps=101, t1_time=0,verbose=True):
    '''
    DESC: extracts T1 portion of repeated sweeps
    INPUT:
            "file_path": full path to 2D matrix of ["num_measurements"*2 part sequence length, number flux points)
    OUTPUT:
        gamma_list: 2D array of (repeated) decay rates vs flux [num_flux, num_seq_repeats]
        gammaErr_list: SciPy reported error in fit
    '''
    
    ## load data and get shapes    
    data = np.loadtxt(file_path)
    seq_parts = 2
    num_fluxes = data.shape[0]
    num_repeats = data.shape[1]//num_seq_steps
    ts = np.linspace(0,t1_time,num_seq_steps//seq_parts)
        
    def my_exp(x,a,b,c):
        return a*np.exp(-b*x) + c
    
    gamma_array = np.zeros((num_fluxes,num_repeats))
    gammaErr_array= np.zeros((num_fluxes,num_repeats))
    for i in range(num_fluxes):
        for j in range(num_repeats):
            ## separate T1 sequence from everything else.
            initial_index = num_seq_steps//seq_parts + j*num_seq_steps
            final_index = (j+1)*num_seq_steps
            single_t1 = data[i, initial_index:final_index]
            
            ## fit exponentials
            initial_guess = (0.5, 0.5, 0.1)
            try:
                fit_param, covariance = scipy.optimize.curve_fit(my_exp, ts, single_t1,
                                                         p0=initial_guess)
                gamma = fit_param[1] 
                gamma_stdErr = np.sqrt(covariance[1,1])
            except RuntimeError:
                if verbose: print(f"Bad fit @flux #{i+1}, fit #{j+1}")
                gamma = np.nan
                gamma_stdErr = np.nan

            ## store fit results
            gamma_array[i,j] = gamma
            gammaErr_array[i,j] = gamma_stdErr
    return gamma_array, gammaErr_array
##END fit_gamma_repeatedSequences


def fourier_analysis(fluxes, gamma_vs_flux_longRepeats):

    num_fluxes = gamma_vs_flux_longRepeats[0].shape[0]
    num_sweep_repeats = gamma_vs_flux_longRepeats[0].shape[1]
    time_between_flux_repeats = 1.7 ## units: hours
    time_between_seq_repeats = 1.7/44/10

    for target_flux_index in range(num_fluxes//4):
        fig, axes = plt.subplots()
        for long_time_index, gamma_flux in enumerate(gamma_vs_flux_longRepeats):
            gamma_repeated = gamma_flux[target_flux_index]
            num_seq_repeats = len(gamma_repeated)
            start_time = long_time_index*time_between_flux_repeats
            end_time = start_time + num_sweep_repeats*time_between_seq_repeats
            time_window = np.linspace(start_time, end_time, num_seq_repeats)
            axes.plot(time_window, 1./gamma_repeated, '.k')
        
        #plt.imshow(gamma_vs_flux_longRepeats[0], vmax=0.7, extent=[1,num_repeats,min(fluxes),max(fluxes)])
        axes.set_title(f"Biased with {fluxes[target_flux_index]} mA")
        axes.set_ylabel("$T_1$ [$\mu s$]")
        axes.set_xlabel("Time [hours]")
    plt.show()

##END fourier_analysis


def main():
    fluxes, gamma_longRepeats, gammaErr_longRepeats = get_data(False)
    make_plot_of_averages(fluxes, gamma_longRepeats)
    fourier_analysis(fluxes, gamma_longRepeats)
##END main
    
    
if __name__ == '__main__':
    main()

