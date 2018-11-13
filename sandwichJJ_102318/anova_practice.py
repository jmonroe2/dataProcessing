#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 18:19:30 2018

@author: jmonroe

This script exists to verify my understanding of ANOVA with the test dataset from wiki
"""
import sys, time, os
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

def get_data():
    ## copying data from wiki/Factorial_experiment#Analysis
    data_array = [45,71,48,65,68,60,80,65,43,100,45,104,75,86,70,96]
    full_data  = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    index = l*2**0 + k*2**1 + j*2**2 + i*2**3
                    data = data_array[index]
                    full_data.append(np.array([l,k,j,i,data]))
    ##END assignment of indices
    return np.array(full_data)
##END get_data


def factor_plot(data):
    ## separates data for each factor (column) and plots '+' case and '-' case
    
    fig, ax_matrix = plt.subplots(2,2)
    #ax_list = ax_matrix.flatten()
    for i in range(data.shape[0]-1): ## all index columns, less data column
        label = "ABCD"[i]
        print(i); continue
        on_index = np.where(data[:,i]==1)
        off_index = np.where(data[:,i]==0)
        on_data = data[on_index, -1]
        off_data = data[off_index, -1]
        
        plt.plot( np.zeros(len(off_data)), off_data, 'ok')
        plt.plot( np.ones(len(on_data)), on_data, 'ok')
        plt.xlabel(label+" status")
        plt.ylabel("Flow rate")
##END factor_plot


def correlation_plot(data):
    '''
    For each interaction, find how a primary variable changes conditioned on a secondary
    variable is on or off.
    '''
    
    index_list = "ABCD"
    num_indices = len(index_list)
    
    for primary_index in range(num_indices):
        for condition_index in range(primary_index+1,num_indices):
            print(primary_index, condition_index)
            subset_on = data[ np.where(data[:,condition_index]==1) ]
            subset_off = data[ np.where(data[:,condition_index]==0) ]
            plt.clf()
            for i,subset in enumerate([subset_on,subset_off]):
                c = 'rb'[i]
                m = '*x'[i]
                on_off = ["ON", "OFF"][i]
                label = index_list[condition_index]+ ' '+ on_off
                off_slice = subset[np.where( subset[: ,primary_index] ==0) ]
                on_slice  = subset[np.where( subset[: ,primary_index] ==1) ]
                off_data = off_slice[:,-1]
                on_data = on_slice[:,-1]
                
                xs = [0,1]
                ys = [np.mean(off_data), np.mean(on_data)]
                plt.plot(xs,ys, color=c, marker=m, label=label)
                
                ## fit a line!
                slope,offset = np.polyfit(xs,ys,1)
                print("{0}|{1} {2}".format(index_list[primary_index],
                      index_list[condition_index], on_off),
                        slope)
                
            ## END loop through on-off plot making
            plt.legend(loc=2)
            plt.xlabel(index_list[primary_index]+" state")
            plt.ylabel("Filtration Rate")
    ##END loop through subsets
    plt.ylim(40,100)

##END correlation_plot


def singleWay_anova(data):
    ## calculate F for each trace of data by comparing mean square (MS) of 
    ##   the categories to the MS of the cross-group data.
    
    ##begin ANOVA
    m = np.mean(data)
    m = 0 ## don't subtract mean according to textbook
    n_samples = data.shape[0]
    n_tests = data.shape[1]
    
    squares = (np.mean(data,axis=0) -m)**2
    SS_sample = n_samples*np.sum(squares)
    df = n_tests-1
    MS_sample = SS_sample/df
    print("sample", SS_sample, df)
    
    squares = np.var(data,axis=0)*n_samples
    SS_err = n_tests*np.sum(squares)
    df = n_samples-1
    MS_err = SS_err/df
    print("error", SS_err, df)
    
    return MS_sample/MS_err
##END singleWay_anova
    

def textbook_anova(data):
    ## calculate F for each trace of data by comparing mean square (MS) of 
    ##   the categories to the MS of the cross-group data.
    print("TBA")
    n_samples = data.shape[0]
    n_tests = data.shape[1]
    
    tot = np.sum(data)
    marginal = np.sum(data,axis=0)/n_samples
    SS_treatments = sum(marginal**2) - tot**2/data.size
    df = n_tests-1
    MS_treatments = SS_treatments/df
    print("treat", SS_treatments, df)
    
    mar_var = np.var(data,axis=0)*n_samples
    SS_err = n_tests*np.sum(mar_var)
    df = n_samples-1
    MS_err = SS_err/df
    print("error", SS_err, df)
    
    return MS_treatments/MS_err
##END textBook_anova
    

def make_pareto_plot(data):
    anova_dict = {}
    
    for index in range(4):
        label = "ABCD"[index]
        on_slice = data[np.where(data[:,index]==1)]
        off_slice = data[np.where(data[:,index]==0)]
        
        on_data = on_slice[ :,-1]
        off_data = off_slice[:,-1]
        all_data = np.zeros((len(on_data), 2))
        all_data[:,0] = off_data
        all_data[:,1] = on_data
        
        result = singleWay_anova(all_data)
        anova_dict[result] = label ## easier to sort keys than values
    ##END through single anova loop
    
    ## double anova double fun
##END data
    
def test_anova(data,num_avg):
    ## 2-factor data is structured as matrix in dim1 x dim2, but repetitions
    ##  are included in rows
    """ For 2 factors with 2 repetitions
        x1       x2
    y1  p1       p3
        p2       p4
    y2  p5       p7
        p8       p9
    """
    num_cols = data.shape[0]//num_avg
    num_rows = data.shape[1]
    ## do y-stats
    f = textbook_anova(data.T)
    print(f)
    ## rearrange for x-stats
    
##END test_anova
    
    
def main():
    data = get_data()
    
    #factor_plot(data)
    #correlation_plot(data)
    
    ## ANOVA
    #make_pareto_plot(data)
    test_data = np.array([[48, 58, 28, 33, 7, 15],
                          [62, 54, 14, 10, 9, 6]])

    test_anova(test_data,2)
    return 0;

    singleWay_anova(test_data)
    singleWay_anova(all_data)
    plt.show()
##END main
   
 
if __name__ == '__main__':
    main()
