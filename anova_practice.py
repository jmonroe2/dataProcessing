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
   
 
def test_anova(data):
    ## 2-factor data is structured as matrix in dim1 x dim2, but repetitions
    ##  are included in rows
    """ For 2 factors with 2 repetitions
        x1       x2         x3
    y1  p1_list  p2_list    p3_list
    y2  p4_list  p5_list    p6_list
    """
    num_treat0 = data.shape[0]
    num_treat1 = data.shape[1]
    num_avg = data.shape[2]
    averaged = np.mean(data,axis=2)

    m = np.sum(averaged*num_avg)**2/data.size ## grand sum of squares, mean?
    mean_squares_dict = dict()
    df_tot = 0

    ## do V-stats
    '''
    v_arranged = data.copy()
    per_sample = data.size//num_treat0
    v_arranged.shape = (num_treat0, per_sample)
    print(np.sum(v_arranged,axis=1)**2 /per_sample )
    return 0;
    '''
     
    # we could sum over repeated trials, but instead replace with n*mean
    marginal = np.sum(averaged*num_avg,axis=1)
    df= num_treat1*num_avg 
    df_tot +=df
    SS_v = np.sum(marginal**2)/df  -m
    mean_squares_dict["d1"] = SS_v/(num_treat1-1)
    print("V:", SS_v)
    
    ## do E-stats
    marginal = np.sum(averaged*num_avg,axis=0)
    df = num_treat0*num_avg 
    df_tot += df
    SS_e = np.sum(marginal**2)/df  -m
    mean_squares_dict["d2"] = SS_e/(df-num_avg)
    print("E:", SS_e)
    
    ## do E*V stats
    # first find variance for any group, then subtract individual
    flat = data.copy()
    flat.shape = (6,2)
    
    gp_mean = np.mean(flat,axis=1) ## average over columns
    mm = np.mean(data)
    diff =(gp_mean-mm)**2 *2
    SS_gp = np.sum( 2*(gp_mean- mm)**2 )
    print("SS_gp", SS_gp)
    SS_ev = SS_gp - SS_e - SS_v
    df = (num_treat0-1)*(num_treat1-1)
    df_tot += df
    mean_squares_dict["int"] = SS_ev/(df)
    print("E*V:", SS_ev)

    ## error (cf each point to it's group mean)
    gp_mean = gp_mean # defined above
    SS_err = 0
    for i in np.arange(flat.shape[1]):
        row = flat[:,i]
        dist_from_gp = (row - gp_mean)**2
        SS_err += np.sum(dist_from_gp)
    df = (data.size-1) 
    print("Err:", SS_err) 
    mean_squares_dict["int"] = SS_ev/df
    
    ## total
    marg_tot = data-np.mean(data)
    SS_total = np.sum(marg_tot**2)
    print("total", SS_total)
    df = data.size-1
    mean_squares_dict["tot"] = SS_total/df
   
    print(mean_squares_dict) 
    return mean_squares_dict 
##END test_anova
    
    
def main():
    data = get_data()
    
    #factor_plot(data)
    #correlation_plot(data)
    
    ## ANOVA
    #make_pareto_plot(data)
    ## from textbook
    test_data = np.array([[[48, 58], [28, 33], [7, 15]],
                          [[62, 54], [14, 10], [9, 6]]])

    a_on = data[np.where(data[:,0] ==1)]
    a_off = data[np.where(data[:,0] ==0)]
    c_on_indices = np.where(a_on[:,2] ==1)
    c_off_indices = np.where(a_on[:,2] ==0)
    ## datum columns: a on, off, rows: c on, c off
    #datum = [[ a_on[np.where(a_on[:,2] == 1)][:,-1],  a_on[np.where(a_on[:,2] == 0)][:,-1] ],
    #         [ a_off[np.where(a_off[:,2] == 1)][:,-1],  a_off[np.where(a_off[:,2] == 0)][:,-1] ]]
    datum = [[ a_on[c_on_indices][:,-1] , a_off[c_on_indices][:,-1]  ] ,
             [ a_on[c_off_indices][:,-1], a_off[c_off_indices][:,-1] ] ]
    datum = np.array(datum)
    
    test_anova(test_data)
    return 0;

    singleWay_anova(test_data)
    singleWay_anova(all_data)
    plt.show()
##END main
   
 
if __name__ == '__main__':
    main()
