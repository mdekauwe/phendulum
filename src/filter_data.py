#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from os.path import isfile
import sys

def main(fpath):
    
    # Display column names and their index for reference
    ec_data = pd.read_csv(fpath, parse_dates=True , index_col=['DT'])
    show_names = False
    show_plot = True
    if show_names == True:
        for n,i in zip(ec_data.columns.values,range(ec_data.shape[1])):
            print( str(i) + " : " + n )

    # Let just grab what we need -- SWC and NDVI
    ec_phen = ec_data.loc[:,("Sws_Con","250m_16_days_NDVI_new_smooth")]

    # Resample the hourly data to daily (although we could just do 16-day)
    ec_sampled = ec_phen.resample('D', how='mean',)
    ec_sampled.columns = ["SWC10","NDVI250X"]
    ec_filt = ec_sampled[np.isfinite(ec_sampled['NDVI250X'])]
    
    # Add date/time index
    ec_filt.reset_index(level=0, inplace=True)
    
    draw_plot = True
    # Plots environmental data
    if draw_plot==True:
        
        fig, (ax1,ax2) = plt.subplots(2, 1, sharex=True, figsize=(9,6))
        fig.subplots_adjust(hspace=0.1)
        fig.subplots_adjust(wspace=0.1) 
        plt.rcParams['text.usetex'] = False
        plt.rcParams['font.family'] = "sans-serif"
        plt.rcParams['font.sans-serif'] = "Helvetica"
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['font.size'] = 12
        plt.rcParams['legend.fontsize'] = 9
        plt.rcParams['xtick.labelsize'] = 12
        plt.rcParams['ytick.labelsize'] = 12
        
        almost_black = '#262626'
        # change the tick colors also to the almost black
        plt.rcParams['ytick.color'] = almost_black
        plt.rcParams['xtick.color'] = almost_black

        # change the text colors also to the almost black
        plt.rcParams['text.color'] = almost_black

        # Change the default axis colors from black to a slightly lighter black,
        # and a little thinner (0.5 instead of 1)
        plt.rcParams['axes.edgecolor'] = almost_black
        plt.rcParams['axes.labelcolor'] = almost_black
        
        ax1.plot(ec_filt['DT'], ec_filt["NDVI250X"], linestyle='-', color='red')
        ax2.plot(ec_filt['DT'], ec_filt["SWC10"], linestyle='-', color='blue')
        ax1.set_ylabel(r"NDVI (-)")
        ax2.set_ylabel(r"$\theta_{10cm}$")
        ax2.set_xlabel(r"Years")
        
        # force zero start in range
        ax1.set_ylim(ymin=0)
        ax2.set_ylim(ymin=0)
        
        ax1.yaxis.major.locator.set_params(nbins=5) 
        ax2.yaxis.major.locator.set_params(nbins=5)         
        
        simpleaxis(ax1)
        simpleaxis(ax2)
        
        #fig.autofmt_xdate()
        fig.savefig("{0}{1}_filt.pdf".format(fig_fold,site), 
                    bbox_inches='tight', pad_inches=0.1)
        
    # Write to CSV into the Data folder
    ec_filt.to_csv(opath, sep=",")

def simpleaxis(ax):
    """ Remove the top line and right line on the plot face """
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

if __name__ == '__main__':
    
    # Import EC tower Dingo dataset for Sturt Plains [move this to a config file]
    out_fold = "../data/"
    fig_fold = "../figs/"
    out_name = "filtered"
    site = "SturtPlains"
    version = "_v12"
    opath = "{0}{1}_{2}{3}.csv".format(out_fold,out_name,site,version)
    fpath = "{0}{1}{2}.csv".format(out_fold,site,version)
    
    main(fpath)