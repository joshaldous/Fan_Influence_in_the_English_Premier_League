#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import scipy.stats as stats
from statsmodels.stats import weightstats as statmodel
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import random as rd
import os


working_df = pd.read_csv('/home/josh/Documents/dsi/caps/cap1/data/epl_cleaned.csv')
working_df = working_df.iloc[:,1:]

df = working_df.copy()

total_home_yellow = sum(df.HY)
total_away_yellow = sum(df.AY)
total_home_red = sum(df.HR)
total_away_red = sum(df.AR)

plt.style.use('seaborn-dark')
fig = plt.figure(figsize=(16,7))
fig.patch.set_facecolor('gainsboro')
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.pie([total_home_yellow,total_away_yellow],labels=['Home Yellow','Away Yellow'],colors=['goldenrod','darkgoldenrod'],autopct='%1.1f%%',startangle=90)
ax2.pie([total_home_red, total_away_red],labels=['Home Red','Away Red'],colors=['firebrick','maroon'],autopct='%1.1f%%', startangle=90)

plt.tight_layout()
plt.savefig('../images/total_card_pie')
plt.show()

def yearlyDf(base_df,yrs): # splits the data frame into seasons and outputs the files as csv's that can be loaded into season by season data frames
    for yr in yrs:
        start = str(yr)+'-08-01'
        end = str(yr+1)+'-07-31'
        mask = (base_df.Date > start) & (base_df.Date < end)
        new_df = base_df.loc[mask]
        new_df.to_csv(f'/home/josh/Documents/dsi/caps/cap1/data/{x}/df_{x}.csv')

def create_df(inputfile): # creates data frames from the csv's created above
    n = pd.read_csv(inputfile)
    return n.iloc[:,1:]

def create_ref_df(df): # creates data frames grouped by refs
    ref_df = df.groupby('ref_name').sum()
    ref_df['Games_reffed'] = df.ref_name.value_counts()
    ref_df.reset_index(inplace=True)
    return ref_df

totrefs = create_ref_df(df)
total_refs_used_totyrs = len(totrefs.ref_name)

def ScatterPlot(x,y,title,xlabel,ylabel,dotlabel,card_color=None):
    plt.style.use('seaborn-dark')
    save_title = title.replace(' ','_')
    fig = plt.figure(figsize=(14,6))
    ax = fig.add_subplot(111)
    plt.rc('font',size=16)
    
    if card_color == 'Yellow' or card_color == 'yellow':
        dotcolor = 'darkgoldenrod'
        diag = 'gold'
    elif card_color == 'Red' or card_color == 'red':
        dotcolor = 'firebrick'
        diag = 'tomato'
        
    ax.scatter(x,y,color=dotcolor,label=dotlabel)
    ax.plot([0,x.max()],[0,y.max()],color=diag, linestyle='--')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'../images/{save_title}.jpeg')

    plt.show()

title_yell_scat = 'Home and Away Yellows Brandished per Referee (Season 2000-2020)'
dlabel = 'Each Referee\'s Yellow Cards Shown'
ScatterPlot(totrefs.HY,totrefs.AY,title_yell_scat,'Home Yellows Brandished','Away Yellows Brandished',dlabel,'yellow')

title_red_scat = 'Home and Away Reds Brandished per Referee (Season 2000-2020)'
dlabel = 'Each Referee\'s Red Cards Shown'
ScatterPlot(totrefs.HR,totrefs.AR,title_red_scat,'Home Reds Brandished','Away Reds Brandished',dlabel,'red')

def BarGraphGrouped(labels,title,xlabel,ylabel,group1,group1_label,group2,group2_label,card_color=None):

    fig = plt.figure(figsize=(12,5))
    ax = fig.add_subplot(111)
    
    save_title = title.replace(' ','_')
    
    barlabels = [x for x in labels]
    bar1 = [y for y in group1]
    bar2 = [z for z in group2]
    width_ = 0.4
    
    if card_color == 'Yellow' or card_color == 'yellow':
        color1, color2, edge = ('palegoldenrod','goldenrod','darkgoldenrod')
    elif card_color == 'Red' or card_color == 'red':
        color1, color2, edge = ('lightcoral','firebrick','maroon')
        
    r1 = np.arange(len(bar1))
    r2 = [x+width_ for x in r1]
    ax.bar(r1,bar1,color=color1,width=width_,edgecolor=edge,label=group1_label)
    ax.bar(r2,bar2,color=color2,width=width_,label=group2_label)

    ax.set_xticks(r1)
    ax.set_xticklabels(barlabels,rotation=45,fontdict={'fontsize':9})
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig(f'/home/josh/Documents/dsi/caps/cap1/images/{save_title}.jpeg',dpi=100)
    plt.show()

avg_games_reffed = df.ref_name.value_counts().mean() # The average number of games reffed is 120 games. There are 24 refs with more than 120 games. 
                                                    #   Any more than that would be too many to graph
sorted_totrefs = totrefs.sort_values('Games_reffed',ascending=False)
top_refs = sorted_totrefs[sorted_totrefs['Games_reffed'] >= avg_games_reffed]

title_yellow_bar = 'Home and Away Yellow Cards for Referees that have Overseen at least 120 Games'
BarGraphGrouped(top_refs.ref_name,title_yellow_bar,'Referees','Number of Cards',top_refs.HY,'Home Yellows',top_refs.AY,'Away Yellows','yellow')

title_red_bar = 'Home and Away Red Cards for Referees that have Overseen at least 120 Games'
BarGraphGrouped(top_refs.ref_name,title_red_bar,'Referees','Number of Cards',top_refs.HR,'Home Reds',top_refs.AR,'Away Reds','red')

home_yellow_mean = np.mean(df.HY) # variables to be used in z-test
away_yellow_mean = np.mean(df.AY)
home_red_mean = np.mean(df.HR)
away_red_mean = np.mean(df.AR)

home_yellow_std = np.std(df.HY)
away_yellow_std = np.std(df.AY)
home_red_std = np.std(df.HR)
away_red_std = np.std(df.AR)

hnorm_yell = stats.norm(home_yellow_mean,home_yellow_std) # normal distribution of home yellow cards
anorm_yell = stats.norm(away_yellow_mean,away_yellow_std) # normal distribution of away yellow cards
delta_yell = hnorm_yell.cdf(away_yellow_mean) - hnorm_yell.cdf(home_yellow_mean) # difference in the area of the distribution between the means of home and away yellows

x_yell = np.linspace(-3,7,len(df.HY))
statmodel.ztest(hnorm_yell.pdf(x_yell),anorm_yell.pdf(x_yell),ddof=7569)


hnorm_red = stats.norm(home_red_mean,home_red_std) # normal distribution of home red cards
anorm_red = stats.norm(away_red_mean,away_red_std) # normal distribution of away red cards
delta_red = hnorm_red.cdf(away_red_mean) - hnorm_red.cdf(home_red_mean) # difference in the area of the distribution between the means of home and away reds

x_red = np.linspace(-1,1.5)
statmodel.ztest(hnorm_red.pdf(x_red),anorm_red.pdf(x_red),ddof=7569)

plt.style.use('seaborn-dark')
fig = plt.figure(figsize=(15,5))
ax = fig.add_subplot(111)

x = np.linspace(-1,1.5,len(df.HR))
ax.plot(x,hnorm_red.pdf(x),color='firebrick')

ax.axvline(home_red_mean,color='firebrick',linestyle='--',label='Average Home Red Cards Given per Match')
ax.axvline(away_red_mean,color='maroon',linestyle='-.',label='Average Away Red Cards Given per Match')

ax.set_xlabel('Home Red Cards Received Distribution (Seasons 2000 - 2020)')
ax.set_ylabel('Probability Density')
ax.fill_between(x, hnorm_red.pdf(x), 0, 
                   where=( (x <= away_red_mean) & (x>=home_red_mean)),
                   color="darkred", alpha=0.2)

ax.arrow(-0.5,0.5,0.35,-0.1,color='firebrick', width=0.05)
ax.text(-1,0.65,f'This difference in means\n is very small',color='maroon',fontsize=20)

plt.legend()
plt.savefig('/home/josh/Documents/dsi/caps/cap1/images/Home_red_normdist.jpeg')
plt.show()

plt.style.use('seaborn-dark')
fig = plt.figure(figsize=(15,5))
ax = fig.add_subplot(111)
plt.gca()
ax.set_facecolor('gainsboro')

x = np.linspace(-2,5,len(df.HY))
ax.plot(x,hnorm_yell.pdf(x),color='goldenrod')
ax.axvline(home_yellow_mean,color='gold',linestyle='--',label='Average Home Yellow Cards\n Given per Match')
ax.axvline(away_yellow_mean,color='darkgoldenrod',linestyle='-.',label='Average Away Yellow Cards\n Given per Match')
ax.set_xlabel('Home Yellow Cards Received Distribution (Seasons 2000 - 2020)')
ax.set_ylabel('Probability Distribution')
ax.fill_between(x, hnorm_yell.pdf(x), 0, 
                   where=( (x <= away_yellow_mean) & (x>=home_yellow_mean)),
                   color="orange", alpha=0.2)
ax.arrow(3.5,0.15,-1.55,-0.05,color='darkgoldenrod', width=0.04)
ax.text(3.6,0.175,f'This difference between\n average away yellows\n and home yellows is\n not large',color='darkgoldenrod',fontsize=20)
plt.legend(loc='upper left')
plt.savefig('/home/josh/Documents/dsi/caps/cap1/images/Home_yellow_normdist.jpeg')
plt.show()
