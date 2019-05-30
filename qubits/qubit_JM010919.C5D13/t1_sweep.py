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
    data_dir = "/Volumes/Crow104/jmonroe/qubit_JM010919.C5D13"
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
    
    def my_exp(x,a,b,c):
        return a*np.exp(-b*x) + c 
    
    plt.figure()
    t1_toSave = []
    for i in range(num_fluxes):
        avg_seq = np.zeros(num_steps//2)
        if fluxes[i] < -5: continue ## skip noisy measurements
        for j in range(num_measurements):
            if j==0: continue
            initial_index = num_steps//2 + j*num_steps
            final_index = (j+1)*num_steps
            single_seq = data[i, initial_index:final_index]
            avg_seq += single_seq
            try:
                param, covariance = scipy.optimize.curve_fit(my_exp, ts, single_seq,  p0=(0.8,0.1,0.5 ))
                std_err = np.sqrt(covariance[1,1])
                #ax_fluxTuned.errorbar(fluxes[i], 1/param[1], yerr=std_err/param[1]**2)
            except RuntimeError:
                print(f"Max num of calls, flux {fluxes[i]} mA, measurement {j}")
            if i==30: plt.plot(ts, single_seq, '.k', alpha=0.7) 
        ##END loop of measurement repeats

        avg_seq /= num_measurements
        try:
            param, covariance = scipy.optimize.curve_fit(my_exp, ts, avg_seq,  p0=(0.8,0.1,0.5 ))
            std_err = np.sqrt(covariance[1,1])
        except RuntimeError:
            print(f"Max num of calls, flux {fluxes[i]} average")

        ax_fluxTuned.errorbar(fluxes[i], 1/param[1], yerr=std_err/param[1]**2)
        t1_toSave.append(1/param[1])

        if i==30:
            plt.plot( ts, avg_seq,'-b')
            print( 1/param[1])
            plt.plot( ts, my_exp(ts, *param) ,'r--')
            plt.xlabel("Time")
            plt.ylabel("avg seq")
        ##END loop of fluxes
    ax_fluxTuned.set_ylim(0,15)
       
    np.savetxt(data_dir+"/T1_repeat_flux_-5,4_averaged.txt",t1_toSave)
    
    ax_fluxTuned.set_xlabel("Flux bias [mA]")
    ax_fluxTuned.set_ylabel("$T_1$ [$\mu s$]")
    ax_fluxTuned.plot(fluxes,25*np.ones(len(fluxes)), 'k--')
    ax_fluxTuned.annotate("Seq. Length", (0,25))
    plt.show()
##END main
    
    
if __name__ == '__main__':
    main()

