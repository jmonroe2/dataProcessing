# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 08:21:24 2018

@author: jonathan
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import re
from probing_util import voltage_to_resistance_critCurr, parse_input
sys.path.append("..")
import anova_util as anova

    
def return_singleJJ_allCol(res):
    
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
    return sorted_byNumJJ_dict[1]
##END return_singleJJ_allCol
    
    
def prepare_data():
    ## load data
    dataFile_list = []
    base_name = "sandwichJJ_102318"
    codename_list = ["pbj","blt","sub","loaf"]
    color_list = ['red', 'purple', 'cyan', 'orange']
    quarterIndex_list = [3,4]
    for q in quarterIndex_list:
        for codename in codename_list:
            next_file = base_name+f"_{codename}_q{q}.dat"
            dataFile_list.append(next_file)
    ##END loop through codenames
    
    ''' recall 5 dimensions
    1. angle of evaporation
    2. extra oxide
    3. ---column-position----
    4. exposure parameters
    5. num JJ (average over)
    '''
    ## array_structure:
    ## angle flag, extra oxide flag, quarter flag, data_list
    ## based on code_name_list I can preprogram these values:
    full_array =          [[0, 0, 0, 9],
                           [0, 1, 0, 9],
                           [1, 1, 0, 9],
                           [1, 0, 0, 9],
                           [0, 0, 1, 9],
                           [0, 1, 1, 9],
                           [1, 1, 1, 9],
                           [1, 0, 1, 9]]
    
    numJJ_template = np.array([[1, 1, 1, 0],
                               [2, 2, 2, 0],
                               [4, 4, 0, 0],
                               [8, 8, 0, 0],
                               [15, 7, 3, 1],
                               [1, 0, 0, 0]])
    
    
    for i,dataFile in enumerate(dataFile_list):
        # setup formating
        data_color = color_list[i%4]
        codename = codename_list[i%4]
        outline = [0, 1.5][(i//4)%2] ## Q3 is empty, Q4 gets thick outline
        
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
        measurement_list = return_singleJJ_allCol(res/1E3)
        full_array[i][-1] = measurement_list
    ##END loop through files
    return full_array
##END plot_resistance_vs_numJunctions

    
def main():
    data = prepare_data()
    
    ## convert to average
    for i in range(len(data)):
        final_list = data[i][-1]
        data[i][-1] = np.nanmean(final_list)
    averaged = np.array(data)

    label_list = ["Angle", "$O_2$","Expose"]
    anova.correlation_plot( averaged,label_list, y_label="kOhms" )
    plt.show()
##END main()
    
    
if __name__ == '__main__':
    main()