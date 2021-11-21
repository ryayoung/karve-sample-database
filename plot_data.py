# Maintainer:     Ryan Young
# Last Modified:  Nov 18, 2021

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from IPython.display import display


def height(male, female):
    with plt.rc_context({'axes.edgecolor':'#076678', 'xtick.color':'grey', 'ytick.color':'none', 'figure.facecolor':'none', 'figure.frameon':'False'}):
        fig = plt.figure(figsize=(8,4))
        bins = np.linspace(56,80,13)
        plt.hist(male,bins,density=True, color = '#076678', alpha=1.0)
        plt.hist(female,bins,density=True, color = '#8f3f71', alpha=0.9)
        plt.xticks(np.arange(56, 82, 2))
        plt.xlabel('Height (in.)', color='grey')
        plt.title('Customer Height: Frequency Distribution', fontweight='bold', color='grey')
        plt.savefig('plots/customer_height.png', dpi=300)
        # plt.show()
        return fig


def weight(male, female):
    with plt.rc_context({'axes.edgecolor':'#076678', 'xtick.color':'grey', 'ytick.color':'none', 'figure.facecolor':'none', 'figure.frameon':'False'}):
        fig = plt.figure(figsize=(8,4))
        bins = np.linspace(80,250,18)
        plt.hist(male,bins,density=True, color = '#076678', alpha=1.0)
        plt.hist(female,bins,density=True, color = '#8f3f71', alpha=0.9)
        plt.xticks(np.arange(80, 260, 10))
        plt.xlabel('Weight (lbs.)', color='grey')
        plt.title('Customer Weight: Frequency Distribution', fontweight='bold', color='grey')
        plt.savefig('plots/customer_weight.png', dpi=300)
        # plt.show()
        return fig


def boot_size(male, female):
    with plt.rc_context({'axes.edgecolor':'#076678', 'xtick.color':'grey', 'ytick.color':'none', 'figure.facecolor':'none', 'figure.frameon':'False'}):
        fig = plt.figure(figsize=(8,4))
        bins = np.linspace(21.5, 33.5, 13)
        plt.hist(male,bins,density=True, color = '#076678', alpha=1.0)
        plt.hist(female,bins,density=True, color = '#8f3f71', alpha=0.9)
        plt.xticks(np.arange(21.5, 34.5, 1))
        plt.xlabel('Boot Size (mondo)', color='grey')
        plt.title('Customer Boot Size: Frequency Distribution', fontweight='bold', color='grey')
        plt.savefig('plots/customer_boot_size.png', dpi=300)
        # plt.show()
        return fig


def ability(abilities, gender):
    with plt.rc_context({'axes.edgecolor':'#076678', 'xtick.color':'grey', 'ytick.color':'none', 'figure.facecolor':'none', 'figure.frameon':'False'}):
        fig = plt.figure(figsize=(8,4))
        bins = np.linspace(1, 4, 4)
        plt.hist(abilities,bins,density=False, color = '#076678') #, alpha=0.8)
        plt.xticks(np.arange(1, 4, 1))
        plt.xlabel('Ability', color='grey')
        plt.title(f'Ability Level - {gender}: Frequency Distribution', fontweight='bold', color='grey')
        plt.savefig(f'plots/customer_ability_{gender.lower()}.png', dpi=300)
        # plt.show()
        return fig


def order_date_month(df_rental):
    # This one is different because we need to re-order months
    # to look like a ski season. So we will make our own array with
    # counts of months, and then re-order the array
    with plt.rc_context({'axes.edgecolor':'#076678', 'xtick.color':'grey', 'ytick.color':'none', 'figure.facecolor':'none', 'figure.frameon':'False'}):
        month_counts = df_rental.OrderDate.groupby(pd.to_datetime(df_rental.OrderDate).dt.month).count().to_list()
        order = [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
        month_counts = [month_counts[i] for i in order]
        month_names = ['Sept','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun']
        fig = plt.figure(figsize=(8,4))
        plt.bar(month_names, month_counts, color = '#076678', width=0.95)
        plt.xlabel('Order Month', color='grey')
        plt.title('Order Month: Frequency Distribution', fontweight='bold', color='grey')
        plt.savefig('plots/order_date_month.png', dpi=300)
        return fig


def order_date_year(years):
    with plt.rc_context({'axes.edgecolor':'#076678', 'xtick.color':'grey', 'ytick.color':'none', 'figure.facecolor':'none', 'figure.frameon':'False'}):
        fig = plt.figure(figsize=(8,4))
        bins = np.linspace(2016, 2022, 7)
        plt.hist(years,bins,density=False, color = '#076678') #, alpha=0.8)
        plt.xticks(np.arange(2016, 2022, 1))
        plt.xlabel('Order Year', color='grey')
        plt.title('Order Year: Frequency Distribution', fontweight='bold', color='grey')
        plt.savefig(f'plots/order_date_year.png', dpi=300)
        # plt.show()
        return fig


def save_days_kept_pool(pool):
    """
    Plots and saves output of save_days_kept_pool so we can see the dist.
    """
    # print(f"Median: {int(np.median(pool))}")
    # print(f"Mean:   {int(np.mean(pool))}")
    # print(f"Min:    {int(np.min(pool))}")
    # Plot histogram to check skewness
    with plt.rc_context({'axes.edgecolor':'#076678', 'xtick.color':'grey', 'ytick.color':'none', 'figure.facecolor':'none', 'figure.frameon':'False'}):
        fig = plt.figure(figsize=(8,4))
        bins = np.linspace(0, 170, 18)
        plt.hist(pool,bins,density=False, color = '#076678', alpha=1.0)
        plt.xticks(np.arange(0, 170, 10))
        plt.xlabel('Days', color='grey')
        plt.title('Days Kept: Frequency Distribution', fontweight='bold', color='grey')
        plt.savefig('plots/hist_days_kept.png', dpi=300)
        return fig


def customer(df):
    # ---- HEIGHT ----
    height_male = df[df['Gender'] == 'm'].Height.to_numpy()
    height_female = df[df['Gender'] == 'f'].Height.to_numpy()
    fig_height = height(height_male, height_female)

    # ---- WEIGHT ----
    weight_male = df[df['Gender'] == 'm'].Weight.to_numpy()
    weight_female = df[df['Gender'] == 'f'].Weight.to_numpy()
    fig_weight = weight(weight_male, weight_female)

    # ---- BOOT SIZE ----
    boot_size_male = df[df['Gender'] == 'm'].BootSize.to_numpy()
    boot_size_female = df[df['Gender'] == 'f'].BootSize.to_numpy()
    fig_boot_size = boot_size(boot_size_male, boot_size_female)

    # ---- ABILITY ----
    ability_male = df[df['Gender'] == 'm'].Ability.to_numpy()
    fig_ability = ability(ability_male, 'Male')

    ability_female = df[df['Gender'] == 'f'].Ability.to_numpy()
    fig_ability = ability(ability_female, 'Female')


def rental(df_rental, days_kept_pool):
    # ---- MONTHS ----
    # months = df_rental.OrderDate.dt.month
    fig_order_month = order_date_month(df_rental)
    # ---- YEARS ----
    years = df_rental.OrderDate.dt.year
    fig_order_year = order_date_year(years)

    # ---- DAYS KEPT ----
    fig_days_kept = save_days_kept_pool(days_kept_pool)





