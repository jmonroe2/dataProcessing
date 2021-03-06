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

def get_test_data():
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


def factor_plot(data,label_list="ABCD"):
    ## separates data for each factor (column) and plots '+' case and '-' case
    fig, ax_matrix = plt.subplots(2,2)
    #x_list = ax_matrix.flatten()
    for i in range(data.shape[1]-1): ## all index columns, less data column
        label = label_list[i]
        on_index = np.where(data[:,i]==1)
        off_index = np.where(data[:,i]==0)
        on_data = data[on_index, -1]
        off_data = data[off_index, -1]
        print(label,on_data)
        print('\t',off_data)
        
        plt.plot( np.zeros(len(off_data)), off_data, 'ok')
        plt.plot( np.ones(len(on_data)), on_data, 'ok')
        plt.xlabel(label+" status")
        plt.ylabel("Outcome")
##END factor_plot


def correlation_plot(data,label_list="ABCD",y_label="Outcome"):
    '''
    For each interaction, find how a primary variable changes conditioned on a secondary
    variable is on or off.
    '''
    
    num_indices = len(label_list)
    n = 3 ## should be num_indices-1 (indexing) but that fails for n=2
    n2 = n**2
    
    fig, ax_array = plt.subplots(n,n)
    unused_plot_indices = list(range(1,n2+1))

    for primary_index in range(num_indices):
        for condition_index in range(primary_index+1,num_indices):
            plot_index = (primary_index + n*(condition_index-1)) % n2 +1
            axes = plt.subplot(n,n,plot_index)
            unused_plot_indices.remove(plot_index)
            
            subset_on = data[ np.where(data[:,condition_index]==1) ]
            subset_off = data[ np.where(data[:,condition_index]==0) ]
            for i,subset in enumerate([subset_on,subset_off]):
                c = 'rb'[i]
                m = '*x'[i]
                on_off = ["ON", "OFF"][i]
                label = label_list[condition_index]+ ' '+ on_off
                off_slice = subset[np.where( subset[: ,primary_index] ==0) ]
                on_slice  = subset[np.where( subset[: ,primary_index] ==1) ]
                off_data = off_slice[:,-1]
                on_data = on_slice[:,-1]
                
                xs = [0,1]
                ys = [np.mean(off_data), np.mean(on_data)]
                std = [np.std(off_data), np.std(on_data)]
                axes.errorbar(xs,ys, color=c, marker=m, label=label,yerr=std)
                
                ## fit a line!
                #slope,offset = np.polyfit(xs,ys,1)
                #@@print("{0}|{1} {2}".format(index_list[primary_index],
                     #index_list[condition_index], on_off),
                     #   slope)
                axes.set_xlabel(label_list[primary_index]+" state")
            ## END loop through on-off plot making
            axes.legend(loc=2,fontsize=8)
            axes.set_xticks([0,1])
            #axes.set_ylim(40,100)
            if primary_index==0:axes.set_ylabel(y_label)
        ##END loop of conditional values
    ##END loop through subsets
    
    ## some nice formatting
    y_max, y_min = -np.inf, np.inf
    for ax in ax_array.flat:
            y_max = max(ax.get_ylim())
            y_min = min(ax.get_ylim())
    for ax in ax_array.flat:
            ax.set_ylim((y_min,y_max))
    ## clear the unused figures
    for i in unused_plot_indices:
        axes = plt.subplot(3,3,i)
        axes.set_axis_off()
##END correlation_plot


def make_pareto_plot(data,label_list="ABCD"):
    anova_results = []
    num_trials = 4
   
    for index in range(num_trials ):
        label = label_list[index]
        on_slice = data[np.where(data[:,index]==1)]
        off_slice = data[np.where(data[:,index]==0)]
        
        on_data = on_slice[ :,-1]
        off_data = off_slice[:,-1]
        all_data = np.zeros((len(on_data), 2))
        all_data[:,0] = off_data
        all_data[:,1] = on_data
        
        f_stat = oneWay_anova(all_data)
        anova_results.append( (label,f_stat) )
    ##END through single anova loop
    
    ## double anova double fun
    for i in range(num_trials ):
        for j in range(i+1,num_trials ):
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
    ##END two-way ANOVA loop

    ## make plot
    plt.figure()
    print("Anova")
    print(anova_results)
    anova_results.sort(key=lambda x:x[1])
    ordered_labels,ordered_vals = zip(*anova_results)
    print(ordered_labels)
    print(ordered_vals)

    y_coords = np.arange(len(ordered_vals))
    plt.barh(y_coords, ordered_vals)
    plt.yticks(y_coords, ordered_labels)
##END make_pareto
   

def oneWay_anova(data,verbose=False):
    ## calculate F-test by comparing Sum of Squares between group means
    ##      and between data points
    ## data: should be 2-D 
    num_groups = data.shape[0]
    num_repeats = data.shape[1]
   
    M = np.mean(data) 
  
    ## SS treatment: compare each group mean to global mean 
    diff = np.mean(data,axis=1) - M
    ss_treat = num_repeats*np.sum( diff**2 )
    ms_treat = ss_treat/(num_groups-1)

    ## SS err: compare all points to global mean
    all_dist = np.apply_along_axis(lambda x: x-np.mean(x),axis=1, arr=data)
    ss_err = np.sum( all_dist**2)
    ms_err = ss_err/( data.size-num_groups)

    #ss_tot = np.sum( (data-M)**2 )
    if verbose:
        print(ms_treat, ms_err)
        print(data)
        print(np.sum(data,axis=1))
        print(np.var(data,axis=1))
    return ms_treat/ms_err
##END oneWay_anova    


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
    ss_ab= n_repeats *np.sum(c**2)
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
    #data = data.T
    print("F:", oneWay_anova(data))

    textBook_data = np.array([[[48, 58], [28, 33], [7, 15]],
                          [[62, 54], [14, 10], [9, 6]]])
    a,b,ab = twoWay_anova(textBook_data)
    print("2-way")
    print("A:",a, "B:", b, "A*B:", ab)

    print(f)
    
##END test_anova 
   
 
def main():
    #test_anova()

    data = get_test_data()
    correlation_plot(data)
    #make_pareto_plot(data)

    plt.show()
##END main
   
 
if __name__ == '__main__':
    main()
