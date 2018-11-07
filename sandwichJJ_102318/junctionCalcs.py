# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 08:21:24 2018

@author: jonathan
"""

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import re


def voltage_to_resistance_critCurr(v_obs_uv,bias_r=1E6):
    v_mon = 0.939E-3 # volts
    v = np.array(v_obs_uv)*1E-6/v_mon
    res = bias_r/(1/v-1) ## from solving for Rs in voltage divider
    i_c = 270.0/res ## magic number from paramp 09/12/18 lookup table
    
    
    return res, i_c 
##END resistance_to_voltage
    

def parse_input(input_list, regex_template, num_blocks,num_cols=None):
    '''
    A function to extract all voltage measurements from a list of .dat file lines
    input_list: string list of rows of .dat file
    regex_template: template to search for
    num_blocks: how many comments to expect
    (num_cols): if you'd like a matrix, this parameter will pad cols with nan
    
    return
    3D matrix where each "block" (first index) contains a matrix structured
        in the same way as the input .dat file (second index is line #, third
        index is inter-row number)
    '''
    
    measurement_list = [ [] ] # intialize to a list of one empty list
    block_index = 0
    for target_str in input_list:
        #print(len(measurement_list)); return 0;
        if "#" in target_str: # comment line
            if len(measurement_list[0]): ## not the first lines of the file
                measurement_list.append([])
                block_index += 1
            continue
        ## findall returns any match
        found = re.findall(regex_template, target_str) 
        if len(found):
            new_row = []
            for group,addition in found:
                new_row.append( float(addition) )
            measurement_list[block_index].append(new_row)
        else:
            #print(target_str,"has no template matches")
            measurement_list[block_index].append([])
    ##END loop through measurements
    
    ## np arrays should have equal length vectors to make matrix
    if num_cols:
        size_array = (block_index+1,len(measurement_list[0]), num_cols)
        output = np.zeros(size_array)
        for i in range(size_array[0]):
            for j in range(size_array[1]):
                k=0
                while k < size_array[2]:
                    try:
                        output[i,j,k] = measurement_list[i][j][k]
                    except IndexError:
                        output[i,j,k] = np.nan
                    k += 1
    else:
        return measurement_list
    return output
##END parse_input
    
    
def addToPlot_res_numJJ(resistance,style_dict=None):
    res = resistance/1E3
    ## parse into dict
    numJJ_template = np.array([[1, 1, 1, 0],
                               [2, 2, 2, 0],
                               [4, 4, 0, 0],
                               [8, 8, 0, 0],
                               [15, 7, 3, 1],
                               [1, 0, 0, 0]])
    
    ## separate all measurements by number of junctions
    sorted_byNumJJ_dict = {} # key,value is num JJ, list of resistances
    for chip_column in res:
        num_rows = chip_column.shape[0]
        num_cols = chip_column.shape[1]
        for i in range(num_rows):
            for j in range(num_cols):
                num_jj = numJJ_template[i,j]
                if not num_jj in sorted_byNumJJ_dict.keys():
                    sorted_byNumJJ_dict[num_jj] = []
                sorted_byNumJJ_dict[num_jj].append(chip_column[i,j])
        ##END loop through single block
    ##END loop through all chip columns
    
    for num_jj in sorted_byNumJJ_dict.keys():
        resistance_list = sorted_byNumJJ_dict[num_jj]
        xs = num_jj*np.ones(len(resistance_list),dtype='int')
        plt.scatter(xs,resistance_list,c='black',alpha=0.6,s=9)
        
        ## plot average
        avg = np.nanmean(resistance_list)        
        std = np.nanstd(resistance_list)
        plt.errorbar(num_jj,avg, yerr=std, **style_dict)
    ##END loop through number of junctions
    plt.xlabel("Number of SQuIDs")
    plt.ylabel("RT Resistance [k$\Omega$]")
        
##END plot_resistance_vs_numJunctions
    
    
def plot_resistance_vs_numJunctions():
    ## load data
    #dataFile = "sandwichJJ_102318_blt_q3Only.dat"
    dataFile_list = []
    base_name = "sandwichJJ_102318"
    codename_list = ["pbj","blt","sub","loaf"]
    quarterIndex_list = [3,4]
    for q in quarterIndex_list:
        for codename in codename_list:
            next_file = base_name+f"_{codename}_q{q}.dat"
            dataFile_list.append(next_file)
    ##END loop through codenames
    
    for i,dataFile in enumerate(dataFile_list):
        # setup formating
        data_color = ['red', 'purple', 'cyan', 'orange'][i%4]
        codename = codename_list[i%4]
        outline = [0, 2][(i//4)%2] ## Q3 is empty, Q4 gets thick outline
        print(dataFile, data_color, outline)
        
        # load file
        with open(dataFile) as open_file:
            read = open_file.readlines()
            open_file.close()
    
        ## use regular expressions to extract 2 numbers (ints)
        re_template = "((\d+\.?\d*)\suV)" # decimal number, then space then 'uV'
        num_blocks = 5
        voltage_list = parse_input(read, re_template, num_blocks=num_blocks,num_cols=4)
        res, current = voltage_to_resistance_critCurr(voltage_list,bias_r=1E6)
        
        ## do specific analysis
        style_dict = {'color':data_color,'markeredgewidth':outline,'ms':15,
                      'alpha':0.8, 'fmt':'o','markeredgecolor':'k'} 
        addToPlot_res_numJJ(res,style_dict=style_dict)
    ##END loop through files
    
    ## make a custom legend
    box_outline = dict(facecolor='white', alpha=0.8)
    x_pos,y_pos = 9,400
    gap = 55
    plt.text(x_pos,y_pos,"PBJ Q3\n(No extra $O_2$) ", color='red',bbox=box_outline)  
    plt.text(x_pos,y_pos-1*gap,"BLT Q3\n(0.5 nm Al$O_x$)", color='purple',bbox=box_outline)  
    plt.text(x_pos,y_pos-2*gap,"SUB Q4\n(ibid, $45^\circ$ evap)", color='cyan',bbox=box_outline)  
    plt.text(x_pos,y_pos-3*gap,"PBJ Q4\n(No extra $O_2$)", color='orange',bbox=box_outline)  
    
    ## more labels
    plt.title("Sandwich Junction test 10/23/18")
    plt.xlabel("Number of SQuIDs")
    plt.ylabel("RT Resistance [k$\Omega$]")    
    #plt.xlim(0,9)
    #plt.ylim(0,200)
##END plot_resistance_vs_numJunctions
    
    
def plot_chip_variation():
    ## load data
    ## function: get first junction
    ## based on chip number, is exterior the first or last column?
    ## add to plot
##END plot_chip_variation
    
    
def main():
    plot_resistance_vs_numJunctions()
    plot_chip_variation()
##END main()
    
    
if __name__ == '__main__':
    main()
