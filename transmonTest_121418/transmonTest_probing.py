#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 16:27:34 2018

@author: jmonroe

This script exists to 
"""
import sys, time, os
import numpy as np
import matplotlib.pyplot as plt


def main():
    lhs_resistance = np.array([[None, 0, 0],
                               [None, 0, 281],
                               [None, -40, 298],
                               [None, 534, 315],
                               [None, 330, 387],
                               [0, 347, 431],
                               [-40, 424, 488],
                               [500, 592, 789],
                               [770, 873, 1929],
                               [1125, 1375, 1086],
                               [1195, 1605, 1030]])
    N_rows = lhs_resistance.shape[0]
    ## histogram the values
    fig, hist_ax = plt.subplots()
    hist_ax.hist(lhs_resistance.flatten(), bins=10)
    hist_ax.set_xlabel("Resistance [Ohms]", fontsize=20)
    hist_ax.set_ylabel("Counts", fontsize=20)
    
    
    def resistance_to_markersize(resistance):
        ## let's make resistance in [0, 1200] make markers of [1,40]
        max_res = 1500
        max_marker = 40
        return resistance/max_res *max_marker + 1
    ##END resistance_to_markersize
    
    ## spatial display
    fig, spatial_ax = plt.subplots()
    for i,row in enumerate(lhs_resistance):
        for j,resistance in enumerate(row): 
            try:
                ms = resistance_to_markersize(resistance)
                color = 'k'
                if ms < 0:
                    color = 'r'
                    ms = 20
            except 
            spatial_ax.plot(j, i, 'o', ms=ms,color=color, alpha=0.7)

    spatial_ax.invert_yaxis()
    spatial_ax.set_ylabel("Row Number", fontsize=20)
    spatial_ax.set_xticks([0,1,2])
    spatial_ax.set_xticklabels(["Col 1", "Col 2", "Col 3"], fontsize=20 )
    
    ## custom legend
    plt.text(0.15, 0, "Size $\propto$ Res. [Ohms]",fontsize=14)
    plt.text(0.15, 0.7, "Open", color='r', fontsize=14)
    plt.show()
##END main
    

if __name__ == '__main__':
    main()

