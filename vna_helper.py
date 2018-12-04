#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 13:56:09 2018

@author: jmonroe

This script exists to shore up helper functions for VNA data processing.
"""
import numpy as np


def parse_smith(data,fs,electrical_delay=None):
    real = data[0::2]
    imag = data[1::2]
    
    
    linmag = np.sqrt(real**2 + imag**2)
    logmag = 10*np.log10(linmag)
    phase = np.angle( real + 1j*imag)
    
    uw_phase,diff = unwrap_phase(phase)
    span = max(fs) - min(fs)
    if electrical_delay:
        uw_phase += electrical_delay*(fs-min(fs))/span/1.4

    out_dict= {}
    out_dict["real"]= real
    out_dict["imag"]= imag
    out_dict["linmag"]= linmag
    out_dict["logmag"]= logmag
    out_dict["phase"]= phase
    
    out_dict["shifted_phase"] = uw_phase
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
     