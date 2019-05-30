#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(username)s

This script exists to process data taken of qubit JM012519.C7D10
"""
import sys, time, os
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import optimize


def some_Fun():
	'''
	DESCRIPTION: 
	INPUT:
	OUTPUT:
	TODO:
	'''
	pass
##END 


def exp(x,A,gamma,y0):
        return A*np.exp(-gamma*x) + y0
##END exp


def main(verbose=True):
    data_path = "/Users/jmonroe/Projects/fabrication/dataProcessing/qubits/qubit_JM012519.C7D10/data/t1_25us_repeat_3mA_10mK/"
    #data_path = "/Users/jmonroe/Projects/fabrication/dataProcessing/qubits/qubit_JM012519.C7D10/data/t1_25us_repeat_3mA_100mK/"
    
    t1_time = 25 ## units: us
    t1_seq_points = 101 ## how many points compose T1 seq.
    ts = np.linspace(0,t1_time, t1_seq_points)

    fig, repeated_ax = plt.subplots()
    T1_list = []

    first_file = True
    counter = 0
    for data_file in sorted(os.listdir(data_path)):
        ## track progress
        counter += 1
        #if counter > 10: break
        #if (counter % 10) != 1: continue

        ## parse files
        if "foo" not in data_file: continue
        file_timestamp = os.path.getmtime(data_path+data_file) ## m-time is "modified" which is same as creation 
        if first_file:
            first_file = False
            start_time = file_timestamp
                   
        ## get time stamp
        time_of_measurement = file_timestamp - start_time ## units: seconds
       
        ## load data 
        data = np.loadtxt(data_path+data_file)
        t1_seq = data[1*t1_seq_points:]

        ## fit T1
        initial_guess = (0.1, 0.2, 0.5) ## A, gamma, y0
        try:
            fit_param, covariance = scipy.optimize.curve_fit(exp, ts, t1_seq,
                                                     p0=initial_guess)
            gamma = fit_param[1] 
            gamma_fitErr = np.sqrt(covariance[1,1])
        except RuntimeError:
            if verbose: print(f"Runtime Error @{data_file}")
            gamma = np.nan
            gamma_fitErr = np.nan

        T1 = 1./gamma
        T1_err = gamma_fitErr/gamma**2
        if T1_err > 0.5*T1: print(f"High error (dT > T/2) in fit @{data_file}")

        ## plots
        if counter==0:
            fig, tmp_ax = plt.subplots() 
            tmp_ax.plot(ts, t1_seq)
            tmp_ax.plot(ts, exp(ts, *fit_param), 'k--')
            tmp_ax.annotate(s=f"$T_1$={np.round(T1,2)}$\pm${np.round(T1_err,4)} $\mu s$",\
                xy=(1,1), xycoords='axes fraction',va='top',ha='right',fontsize=14)
        #repeated_ax.errorbar(time_of_measurement/3600, T1,yerr=T1_err, fmt='.k')
        repeated_ax.plot(time_of_measurement/3600, T1,'.',color='steelblue')
        T1_list.append(T1)

    ##END loop through files
       
    repeated_ax.set_xlabel("Measurement Time [hours]")
    repeated_ax.set_ylabel("$T_1 [\mu s]$")

    ## try a PSD
    plt.figure()
    dt = 26 ## seconds
    t1bar = np.mean(T1_list)
    plt.psd(T1_list-t1bar, 512, dt)

    plt.show()
##END main
    

if __name__ == '__main__':
    main()
