#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 09:11:57 2019

@author: jmonroe

This script exists to 
"""
import sys, time, os
import numpy as np
import matplotlib.pyplot as plt

from probing_util import voltage_to_resistance_critCurr
import re


def some_Fun():
	'''
	DESCRIPTION: 
	INPUT:
	OUTPUT:
	TODO:
	'''
	pass
##END 


def parse_data(file_name_base=None):
    ## formatted data: voltage, err, resistance, label
    ## setup output arrays 
    all_voltages = np.array([])
    all_voltage_errs = np.array([])
    all_resistances = np.array([])
    all_labels = np.array([])


    ## read data from file
    data_path = "/Users/jmonroe/Projects/fabrication/dataProcessing/junctionTests/largeJJ_lorenzo_080219/data_probing/"
    
    for file_name in os.listdir(data_path):
        if not file_name.endswith(".txt"): continue
        if file_name_base is not None:
            if file_name_base not in file_name: continue

        die_name = file_name[-6:-4]
        full_path = os.path.join(data_path, file_name)
    
        with open(full_path) as open_file:
            readlines = open_file.readlines()
            open_file.close()
        
        ## use regex to search for uV measurements
        voltage_regex = "((\d+\.?\d*)\s\+/\-)" # decimal number, then space then '+/-'
        voltage_err_regex = "((\d+\.?\d*)\s uV)" # decimal number, then space then 'uV'
        
        ## this data has two columns of data. Each cell of data has measurement, error,
        ##  then resistance is on next line. Sometimes the data isn't taken becauce
        ##  of visual deformation/short, etc. 
        
        voltages = np.zeros((len(readlines)//2, 2))
        voltage_errs = np.zeros((len(readlines)//2, 2))
        resistances = np.zeros((len(readlines)//2, 2))
        for i,line in enumerate(readlines):
            row_index = i//2 
            if (i%2==0): ## even rows are voltages
                ## parse each data celL:
                for j,column_text in enumerate(line.split('\t')):
                    try:
                        ## IndexError is raised by index after re.findall() if regex didn't find anything
                        group, found_volt = re.findall(voltage_regex, column_text)[0]
                        group, found_volt_err = re.findall(voltage_err_regex, column_text)[0]
                    ## deal with empty data cells:
                    except IndexError:
                        found_volt = float('nan')
                        found_volt_err = float('nan')
                    voltages[row_index,j] = float(found_volt)
                    voltage_errs[row_index,j] = float(found_volt_err)                    
            else: ## odd rows are resistances
                for j,column_text in enumerate(line.split('\t')):
                    if "Ohms" not in column_text:
                        resistances[row_index,j] = np.nan
                    else:
                        resistances[row_index,j] = float(column_text.split()[0])
                        
        vs = voltages.flatten()
        v_errs = voltage_errs.flatten()
        rs = resistances.flatten()
        labels = [die_name for _ in range(len(vs))]
        
        all_voltages = np.append(all_voltages, vs)
        all_voltage_errs = np.append(all_voltage_errs, v_errs)
        all_resistances = np.append(all_resistances, rs)
        all_labels = np.append(all_labels, labels)
    ## end for through files

    return all_voltages, all_voltage_errs, all_resistances, all_labels
##END parse_data


geometry_dict = {"@":(1.5,1), "#":(1.8,1.2), "$":(2.1,1.4), "%":(2.4,1.6)}
def dieNum_to_geoLabel(label):
    ## INPUT: label is die index, eg 4F
    if label in ['1A', '1C', '1E', '3A', '3C', '3E', '5A', '5C', '5E']:
        geo_label = "@"
    elif label in ['2A', '2C', '2E', '4A', '4C', '4E', '6A', '6C', '6E']:
        geo_label ="#"
    elif label in ['1B', '1D', '1F', '3B', '3D', '3F', '5B', '5D', '5F']:
        geo_label = "$"
    elif label in ['2B', '2D', '2F', '4B', '4D', '4F', '6B', '6D', '6F']:
        geo_label = "%"
    else:
        raise IndexError("{} not a valid label".format(label))
    
    return geo_label 
##END dieNum_to_geoLabel 


def res_vs_bridge_area():
    ## grab data
    all_vs, all_errs, all_res, all_labels = parse_data("chip1a")
   
    ## put data into new structure 
    device_res_dict = {}
    for i in range(len(all_vs)):
        label = all_labels[i]
        voltage = all_vs[i]
        new_res, _ = voltage_to_resistance_critCurr(voltage, bias_r = 10200, v_mon=948.4E-6)
        geo_label = dieNum_to_geoLabel(label)
        geometry = geometry_dict[geo_label]

        ## populate dictionary with key=geo_label, val=resistances
        # make sure the key exists in dict
        if geo_label not in device_res_dict.keys():
            device_res_dict[geo_label] = [] 
        device_res_dict[geo_label].append(new_res)

    ## make plots
    max_res = 200
    resistance_bins = np.linspace(50,max_res, 25)
   
    # histogram 
    fig, ax = plt.subplots()
    count = 0
    for key in device_res_dict.keys():
        resistances = np.array(device_res_dict[key])
        resistances[resistances > max_res] = np.nan
        ax.hist(resistances, label=key, bins=resistance_bins, alpha=0.7)

    ax.legend()
    ax.set_xlabel("Resistance [$\Omega$]")
    ax.set_ylabel("Count")
   
    # plot resistance vs bridge area
    fig, ax2 = plt.subplots()
    ax2.set_xlabel("Nominal JJ Area [$\mu m^2$]")
    ax2.set_ylabel("Resistance [$\Omega$]") 
    for key in device_res_dict.keys():
        resistances = np.array(device_res_dict[key])
        length = geometry_dict[key][0]
        width  = geometry_dict[key][1]
        ## 60 deg evaporation, 1.0 um height (LOR10B)
        junction_area = width*(2*1.0*np.tan(60/180*np.pi) - length)
        xs = np.ones(len(resistances)) *junction_area

        ## some of the junctions have long leads. The top and bottom of each block of 4
        ## junctions has long lead. The below equation maps long junctions to 1 and short to 0
        long_lead_flag =  (np.arange(len(resistances)) -2) //4 %2
        short_lead_flag = long_lead_flag ^ 1 ## bit-wise flip 
        long_lead_flag = np.array(long_lead_flag, dtype='bool')
        short_lead_flag = np.array(short_lead_flag, dtype='bool')
        
        ax2.plot(xs[long_lead_flag], resistances[long_lead_flag],'or')
        ax2.plot(xs[short_lead_flag], resistances[short_lead_flag],'ob')

    ## add labels, but only one per long/short, not one for each dict key
    ax2.plot(xs[0], resistances[0], 'or', label="Long Lead")
    ax2.plot(xs[0], resistances[0], 'ob', label="Short Lead")

    ## add a line to guide the eye
    fit_xs = np.linspace(1.7,2,100)
    fit_ys = 280/fit_xs
    ax2.plot(fit_xs,fit_ys, 'k--', label="280/Area")
    ax2.set_ylim(0,300)
    ax2.legend()
    plt.show()
##END res_vs_bridge_area 


def res_vs_position():
    all_vs, all_errs, all_res, all_labels = parse_data("chip1b")
    #num_JJ_in_chip1b = len(all_vs)
    #all_vs, all_errs, all_res, all_labels = parse_data("chip1a")
   
    ## put data into new structure 
    device_res_dict= {}
    for i in range(len(all_vs)):
        label = all_labels[i]
        voltage = all_vs[i]
        new_res, _ = voltage_to_resistance_critCurr(voltage, bias_r = 10200, v_mon=948.4E-6)

        die_index = label[1]

        ## populate dictionary with key=geo_label, val=resistances
        # make sure the key exists in dict
        if die_index not in list(device_res_dict.keys()):
            device_res_dict[die_index] = [] 
        device_res_dict[die_index].append(new_res)
    ##END loop through all measurements 

    
    ## make histogram 
    fig, ax = plt.subplots()
    ax.set_xlabel("Resistance [$\Omega$]")
    ax.set_ylabel("Count [offset]")
    fig, ax2 = plt.subplots()
    ax2.set_xlabel("Pos. from wafer center")
    ax2.set_ylabel("Resistance [$\Omega$]")

    max_res = 200
    res_bins = np.linspace(100,max_res,20)

    res_support = np.linspace(100,max_res, 2000)
    
    for i,key in enumerate(device_res_dict.keys()):
        resistances = np.array(device_res_dict[key])
        #resistances[resistances > max_res] = np.nan
        position = ord(key)-65
        xs = [position for _ in range(len(resistances))]

        ax2.plot(xs, resistances,'o')
        ax.hist(resistances, label=key, bins=res_bins, alpha=0.7)
        '''
        ## top-hat kernel estimator
        ## consider each point as a bin. 
        ## for every point in support: if it has a point within width, add one
        width = 5
        smoothed = sum(  abs(res_support-r) <width  for r in resistances )
        i = ord(key)-65
        ax.plot(res_support, smoothed+10*i,label=key)   
        #'''
    ax2.plot([2.5,2.5], [0,15000], 'k--')
    ax.set_title("Chip 1b patterns, column 2")
    ax.legend()

    ## make plot vs position
  
    plt.show() 
##END res_vs_position


def save_all_data():
    all_vs, all_errs, all_res, all_labels = parse_data("chip1a")
    all_vs2, all_errs2, all_res2, all_labels2 = parse_data("chip1b")

    chip_label = np.array(["1a" for _ in range(len(all_vs))])
    chip_label2 = np.array(["1b" for _ in range(len(all_vs2))])

    all_vs = np.append(all_vs, all_vs2)
    all_errs = np.append(all_errs, all_errs2)
    all_res = np.append(all_res, all_res2)
    all_labels = np.append(all_labels, all_labels2)
    all_chip_labels = np.append(chip_label, chip_label2)
    
    full_data = np.array([ all_vs, all_errs, all_res, all_labels, all_chip_labels],dtype='str' ).T

    full_name = "full_info.csv" 
    np.savetxt(full_name, full_data, fmt="%s",delimiter=',')
##EDD analyze_both_chips


def main():
    res_vs_bridge_area()
    #res_vs_position()

##END main

if __name__ == '__main__':
    main()

