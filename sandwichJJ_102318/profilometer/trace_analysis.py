#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 15:19:51 2018

@author: Fabusers

This script exists to 
"""
import sys, time, os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
plt.style.use('ggplot')
mpl.rcParams['font.size'] = 20
mpl.rcParams['axes.grid'] = False

def plot_all(data_dir):
    '''
    DESCRIPTION: blindly plots all traces from .dat files
    INPUT: base file to search
    OUTPUT: show figures
    '''
    for file_name in os.listdir(data_dir):
        if not file_name.endswith('.dat'): continue
        fig, trace_ax = plt.subplots()
        data = np.loadtxt(data_dir+"\\"+file_name, comments='"',delimiter=',')
        pos = data[:,0]
        height = data[:,1]
        trace_ax.plot(pos, height,',k')
        trace_ax.set_title(file_name[:-4])
        trace_ax.set_xlabel("Trace position [mm]")
        trace_ax.set_ylabel("Resist height [nm]")
    plt.show()
##END plot_all 


def plot_stack(data_dir):
    '''
    DESCRIPTION: show a few relevant pairs with appropriate labels
    INPUT: base file
    OUTPUT: shown figures
    '''
    
    f, ax_stack = plt.subplots()
    d = np.loadtxt(data_dir+r"\trace1.dat", comments='"',delimiter=',')
    pos, depth = d.T
    pos -= 0.015
    ax_stack.plot(pos,depth, 'b,', label='Column 5')
    d = np.loadtxt(data_dir+r"\trace3.dat", comments='"',delimiter=',')
    pos, depth = d.T
    ax_stack.plot(pos,depth, 'r,', label='Column 3')
    ax_stack.set_title("Full stack")
    ax_stack.set_xlabel("Trace position [mm]")
    ax_stack.set_ylabel("Resist height [nm]")
    ax_stack.set_xlim(0,0.08)
    ax_stack.legend()
##END plot_pairs


def plot_vert_variation(data_dir):
    f, ax_stack = plt.subplots()
    d = np.loadtxt(data_dir+r"\trace2.dat", comments='"',delimiter=',')
    pos, depth = d.T
    ax_stack.plot(pos,depth, 'b,', label='Column 5')
    d = np.loadtxt(data_dir+r"\trace4.dat", comments='"',delimiter=',')
    pos, depth = d.T
    ## cutoff a wierd feature 
    pos = pos[:-7000]
    depth = depth[:-7000]
    ax_stack.plot(pos,depth, 'r,', label='Column 3')
    ax_stack.set_title("Vert. Sweep")
    ax_stack.set_xlabel("Trace position [mm]")
    ax_stack.set_ylabel("Resist height [nm]")
    ax_stack.legend(loc=4)
##END plot_vert_variation


def plot_hor_variation(data_dir):
    f, ax_stack = plt.subplots()
    d = np.loadtxt(data_dir+r"\trace6.dat", comments='"',delimiter=',')
    pos6, depth6 = d.T
    ax_stack.plot(pos6,depth6, 'b,', label='Short')
    d = np.loadtxt(data_dir+r"\trace7c.dat", comments='"',delimiter=',')
    pos7, depth7 = d.T
    ax_stack.plot(pos7,depth7, 'r,', label='Long')
    ax_stack.set_title("Variation b/t runs (after realignment)")
    ax_stack.set_xlabel("Trace position [mm]")
    ax_stack.set_ylabel("Resist height [nm]")
    ax_stack.legend(loc=4)
    ax_stack.set_xlim(0,1.6)
    #ax_stack.set_ylim(-140,140)
    
    f, ax_full_range = plt.subplots()
    ax_full_range.set_title("Horizontal sweep")
    ax_full_range.set_xlabel("Trace position [mm]")
    ax_full_range.set_ylabel("Resist height [nm]")
    ax_full_range.plot(pos7,depth7)
##END plot_hor_variation


def main():
    data_dir = r"C:\Users\Fabusers\Documents\cleanRoomData\120418_sandwhich_profilometry\120518_sandwichJJ"
    
    #plot_all(data_dir)
    plot_stack(data_dir)
    plot_vert_variation(data_dir)
    plot_hor_variation(data_dir)
##END main
    

if __name__ == '__main__':
    main()

