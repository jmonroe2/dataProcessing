#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(username)s

This script exists to analyze probing data of  Softbake test 04/11/19
"""
import sys, time, os
import numpy as np
import matplotlib.pyplot as plt


def main():
    data_file = os.getcwd() + "/data.txt"
    min_res = 100
    max_res = 25E6

    ## open file
    with open(data_file) as open_file:
        read_lines = open_file.readlines()
    
    ## parse lines with resistance
    res_list = []
    for line in read_lines:
        #if "67" in line: print(line); break
        if "Ohms" not in line: continue
        num = float(line[:len("Ohms")+1])
    
        if min_res < num < max_res:
            res_list.append(num)
    ##END loop through 

    ## do stats
    mean = np.round(np.mean(res_list),-1)
    std = np.round(np.std(res_list), 1)
    print(mean, std)

    ## make figure
    bins = np.linspace(mean-2*std,mean+2*std, 15) 
    #bins = 10 #np.linspace(10E3,20E3,20)
    plt.hist(res_list,bins=bins)
    plt.xlabel("Resistance [$\Omega$]")
    plt.ylabel("Count")
    plt.show()
    
##END main
    

if __name__ == '__main__':
    main()
