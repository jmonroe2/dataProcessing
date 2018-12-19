#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 23:52:59 2018

@author: jonathan

This script exists to 
"""
import sys, time, os
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')


def main():
    data_dir = r"C:\Users\jonathan\Desktop\\121318_spinTest\\"
    
    compare_spins(data_dir)
    compare_dataFormats(data_dir)
    
##END main
    
    
def compare_spins(data_dir):
    trace_ids = [(1,3), (3,4),(1,None)] 
    for i,basename in enumerate(["sop1", "dynamic", "sop2"]):
        first_trace, second_trace = trace_ids[i]
        name1 = data_dir+f"{basename}_trace{first_trace}_raw.dat"
        name2 = data_dir+f"{basename}_trace{second_trace}_raw.dat"
        
        fig, ax = plt.subplots()
        d1 = np.loadtxt(name1, comments='"', delimiter=',')
        xs = d1[:, 0]
        ys = d1[:, 1]
        ax.plot(xs,ys,'bo',label="Perimeter",ms=1)
        
        if second_trace: 
            d2 = np.loadtxt(name2, comments='"', delimiter=',')
            xs = d2[:, 0]
            ys = d2[:, 1]
            ax.plot(xs,ys,'ro', label="off-center",ms=1)
        ax.legend(title="Starting\n position:", markerscale=5)
        ax.set_title(f"Spun w/ {basename.upper()} [Raw data]")
    plt.show()    
##END compare_samples


def compare_dataFormats(data_dir):
    fig, ax = plt.subplots()
    for suffix in ["", "_raw", "_levelStep"]:
        filename = data_dir+"dynamic_trace4"+suffix+".dat"
        d1 = np.loadtxt(filename, comments='"', delimiter=',')
        xs = d1[:, 0]
        ys = d1[:, 1]

        name = suffix[1:] if len(suffix) else "Auto level-fixed"
        ax.plot(xs,ys,'o',label=name,ms=1)
    ax.legend(title="Data saved", markerscale=5)
    ax.set_title("Dynamic Spin Saving Format")
    plt.show()
##END compare_dataFormats
        
        
if __name__ == '__main__':
    main()
    

