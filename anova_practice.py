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
    #print("sample", SS_sample, df)
    
    squares = np.var(data,axis=0)*n_samples
    SS_err = n_tests*np.sum(squares)
    df = n_samples-1
    MS_err = SS_err/df
    #print("error", SS_err, df)
    
    return MS_sample/MS_err
##END singleWay_anova


def oneWay_anova(data):
    ## calculate F-test by comparing Sum of Squares between group means
    ##      and between data points
    ## data: should be 2-D 
    num_groups = data.shape[0]
    num_repeats = data.shape[1]
   
    M = np.mean(data) 
  
    ## SS treatment: compare each group mean to global mean 
    diff = np.mean(data,axis=1) - M
    ss_treat = np.sum( diff**2 )
    ms_treat = ss_treat/(num_groups-1)
    print("treat:", ss_treat)

    ## SS err: compare all points to global mean
    ss_err = np.sum( (data-M)**2 )
    ms_err = ss_err/( data.size-num_groups)
    print("err:", ss_err)

    return ms_treat/ms_err

##END oneWay_anova    
    

def textbook_anova(data):
    ## calculate F for each trace of data by comparing mean square (MS) of 
    ##   the categories to the MS of the cross-group data.
    print("TBA")
    n_samples = data.shape[0]
    n_tests = data.shape[1]
    
    tot = np.sum(data)
    marginal = np.sum(data,axis=0)
    SS_treatments = sum(marginal**2)/n_samples - tot**2/data.size
    df = n_tests-1
    MS_treatments = SS_treatments/df
    print(SS_treatments, df)
   
    ## SS error is whatever isn't accounted for with treatment: SS_tot - SS_treat
    m = np.mean(data)
    SS_tot = np.sum( (data-m)**2 )
    SS_tot = (data.size-1)*np.var(data)  
    SS_err = SS_tot - SS_treatments
    df = data.size-n_samples

    MS_err = SS_err/df

    print("error", SS_err, df)
    
    return MS_treatments/MS_err
##END textBook_anova
    

def make_pareto_plot(data):
    anova_results = []
   
    label_list = "ABCD" 
    for index in range(4):
        label = label_list[index]
        on_slice = data[np.where(data[:,index]==1)]
        off_slice = data[np.where(data[:,index]==0)]
        
        on_data = on_slice[ :,-1]
        off_data = off_slice[:,-1]
        all_data = np.zeros((len(on_data), 2))
        all_data[:,0] = off_data
        all_data[:,1] = on_data
        
        f_stat = singleWay_anova(all_data)
        #anova_results.append( (label,f_stat) )
    ##END through single anova loop
    
    ## double anova double fun
    for i in range(4):
        for j in range(i+1,4):
            label = label_list[i] +'*'+ label_list[j] 
            first_on = data[np.where(data[:,i] ==1)]
            first_off = data[np.where(data[:,i] ==0)]
            sec_on_indices = np.where(first_on[:,j] ==1)
            sec_off_indices = np.where(first_on[:,j] ==0)
            ## datum columns: a on, off, rows: c on, c off
            datum = [[ first_on[sec_on_indices][:,-1] , first_off[sec_on_indices][:,-1]  ] ,
                     [ first_on[sec_off_indices][:,-1], first_off[sec_off_indices][:,-1] ] ]
            datum = np.array(datum)
        
            first, second, interact = twoWay_anova(datum)
            anova_results.append( (label, interact) )
            anova_results.append( (label_list[j], first) )
    ##END two-way ANOVA loop

    ## make plot
    anova_results.sort(key=lambda x:x[1])
    ordered_labels,ordered_vals = zip(*anova_results)
    print(anova_results)

    y_coords = np.arange(len(ordered_vals))
    plt.barh(y_coords, ordered_vals)
    plt.yticks(y_coords, ordered_labels)
    
##END make_pareto
   

def twoWay_anova(data):
    '''
    Two-way anova on 3 dimensional data:
       expected data format: data[gp A index, gp B index, repetition ]
    '''
    ## two-way anova: assuming AxBxN matrix
    n_a = data.shape[0]
    n_b = data.shape[1]
    n_repeats = data.shape[2] 

    M = np.mean(data) ## global mean
    avg_repeats = np.mean(data,axis=2)
    
    ## first factor
    a_dist = np.mean(avg_repeats,axis=1) - M
    ss_a = n_b*n_repeats*np.sum(a_dist**2)
    ms_a = ss_a /(n_a-1) ## degrees of freedom via Bessel's correction

    ## second factor
    b_dist= np.mean(avg_repeats,axis=0) - M
    ss_b = n_a*n_repeats*np.sum(b_dist**2)
    ms_b = ss_b /(n_b-1) ## degrees of freedom via Bessel's correction

    ## interaction
    net_dist = np.apply_along_axis(lambda x: x-a_dist,axis=0, arr=avg_repeats)
    net_dist = np.apply_along_axis(lambda x: x-b_dist,axis=1, arr=net_dist)
    net_dist -= M
    ss_ab= n_repeats *np.sum(net_dist**2)
    ms_ab= ss_ab /(n_a-1) /(n_b-1)

    ## error
    all_dist = np.apply_along_axis(lambda x: x-np.mean(x),axis=2, arr=data)
    
    #all_dist = np.apply_along_axis(my_fun,axis=2, arr=data)
    ss_err = np.sum(all_dist**2)
    ms_err = ss_err /( n_a*n_b*(n_repeats-1))
    
    ## (check against total)
    ss_tot= np.sum((data-M)**2 )
    #print(ss_tot, '==', ss_a + ss_b + ss_ab + ss_err)
   
    ## convert to F-statistics 
    return ms_a/ms_err, ms_b/ms_err, ms_ab/ms_err
##END twoWay_anova


def test_anova():
    print("1-way")
    data = np.array([[1.93, 2.38, 2.20, 2.25],
                     [2.55, 2.72, 2.75, 2.7],
                     [2.4, 2.68, 2.31, 2.28],
                     [2.33, 2.4, 2.28, 2.25]])
    print("F:", oneWay_anova(data))

    textBook_data = np.array([[[48, 58], [28, 33], [7, 15]],
                          [[62, 54], [14, 10], [9, 6]]])
    a,b,ab = twoWay_anova(textBook_data)
    print("2-way")
    print("A:",a, "B:", b, "A*B:", ab)

    textBook_data.shape = 2,2*3
    f = singleWay_anova(textBook_data)
    print(f)
    
##END test_anova 
   
 
def main():
    #test_anova()

    data = get_data()
    #factor_plot(data)
    #correlation_plot(data)
    make_pareto_plot(data)

    plt.show()
##END main
   
 
if __name__ == '__main__':
    main()
