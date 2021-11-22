# Maintainer:     Ryan Young
# Last Modified:  Nov 21, 2021

import matplotlib.pyplot as plt
import load_data
import time
import functions as fx
import plot_data as plot
from IPython.display import display
import pandas as pd
# import numpy as np

start_time = time.time()

build_info = pd.read_csv("build_info.txt", header=None, delim_whitespace=True)
build_num = build_info.iloc[0,1]
new_build = False

# ============================================================================
# ========= SET QUANTITIES ===================================================
# ============================================================================

# 5000/500/4000 - retires 170 of 500 skis
# 1000/500/3000 - retires 30 of 500 skis
# try 1200/800/4500
# QUANTITIES
num_customers       = 2500
num_mounted_skis    = 3000
num_rentals         = 12000
# ACTIONS
generate_customers  = True
generate_skis       = True
generate_rentals    = True
other_enabled       = False
# PLOTS
plot_customer       = True
plot_rental         = True

# Document a new build if we are loading all three tables
if generate_customers and generate_skis and generate_rentals:
    new_build = True


# ============================================================================
# ============== DATA ========================================================
# ============================================================================

# DATA 
db = load_data.Data()

# Tables needed to generate skis
df_ski_model = db.df_ski_model
df_binding_model = db.df_binding_model
df_ski = db.df_ski
df_binding = db.df_binding
df_mounted_ski = db.df_mounted_ski

# Tables needed to generate rentals
df_ski_type = db.df_ski_type
df_brand = db.df_brand
df_customer = db.df_customer
df_rental = db.df_rental
df_damage = db.df_damage
df_damage_type = db.df_damage_type

if new_build:
    fx.clear_console()
    build_info.loc[0]="build_info",(build_num + 1)
    print(f"STARTING NEW BUILD: {int(build_num+1)}")
    plot_customer = True
    plot_rental = True

# ============================================================================
# ====== GENERATE CUSTOMER ===================================================
# ============================================================================
if generate_customers:
    df_customer = fx.clear_df(df_customer)
    for i in range(0,num_customers):
        new_customer = fx.gen_customer(df_customer, db.arr_boynames, db.arr_girlnames, db.arr_lastnames,
                db.arr_emailtypes, db.df_street, db.df_skitowns, db.df_dob, db.df_bootsizes, pretty_print=False)
        df_customer = df_customer.append(new_customer, ignore_index=True)

    display(df_customer)
    # Write to file

    if not new_build:
        df_customer.to_csv("karvedata/CUSTOMER.csv", header=False, index=False)
        build_info.loc[2] = "customers(updated)", num_customers

# ============================================================================
# ====== GENERATE SKI & BINDING ==============================================
# ============================================================================
if generate_skis:
    # Clear dataframes
    df_ski = fx.clear_df(df_ski)
    df_binding = fx.clear_df(df_binding)
    df_mounted_ski = fx.clear_df(df_mounted_ski)

    # Generate new skis
    for i in range(0,num_mounted_skis):
        new_ski = fx.gen_ski(df_ski, df_ski_model, df_ski_type, pretty_print=False)

        year = new_ski.PurchaseDate.iloc[0].year
        month = new_ski.PurchaseDate.iloc[0].month
        new_binding = fx.gen_binding(df_binding, df_binding_model, year, month)

        new_mounted_ski = fx.gen_mount_this_ski(df_mounted_ski, new_ski.SkiID.iloc[0], new_binding.BindingID.iloc[0], year, month)

        df_ski = df_ski.append(new_ski, ignore_index=True)
        df_binding = df_binding.append(new_binding, ignore_index=True)
        df_mounted_ski = df_mounted_ski.append(new_mounted_ski, ignore_index=True)

    # Write to file
    # Display
    display(df_ski)

    if not new_build:
        df_ski.to_csv("karvedata/SKI.csv", header=False, index=False)
        df_binding.to_csv("karvedata/BINDING.csv", header=False, index=False)
        df_mounted_ski.to_csv("karvedata/MOUNTED_SKI.csv", header=False, index=False)
        build_info.loc[3] = "mounted_skis(updated)", num_mounted_skis



# ============================================================================
# ========== GENERATE RENTAL =================================================
# ============================================================================
days_kept_pool = fx.gen_days_kept_nums()
if generate_rentals:
    df_rental = fx.clear_df(df_rental)
    df_damage = fx.clear_df(df_damage)
    rentals_generated = 0
    skis_retired = 0
    skis_totaled = 0

    for i in range(0,num_rentals):
        new_rental, df_damage, df_ski, df_binding, df_mounted_ski, rentals_generated, skis_retired, skis_totaled = fx.gen_rental(df_rental, df_customer, df_damage, df_ski, df_binding, df_mounted_ski, df_ski_model, df_brand, df_ski_type, df_binding_model, days_kept_pool, rentals_generated, skis_retired, skis_totaled)
        df_rental = df_rental.append(new_rental, ignore_index=True)

    display(df_rental)

    if not new_build:
        df_rental.to_csv("karvedata/RENTAL.csv", header=False, index=False)
        df_damage.to_csv("karvedata/DAMAGE.csv", header=False, index=False)
        df_ski.to_csv("karvedata/SKI.csv", header=False, index=False)
        df_binding.to_csv("karvedata/BINDING.csv", header=False, index=False)
        df_mounted_ski.to_csv("karvedata/MOUNTED_SKI.csv", header=False, index=False)
        build_info.loc[4] = "rentals(updated)", num_rentals



# ============ END TIMER =====================================================
end_time = time.time()
elapsed_time = round((end_time - start_time), 3)

# ============================================================================
# ============ PLOT DATA =====================================================
# ============================================================================

if plot_customer:
    plot.customer(df_customer)

if plot_rental:
    plot.rental(df_rental, days_kept_pool)

if plot_customer or plot_rental: # add an OR statement for each plot category
    """Only call plt.show() ONCE, so all charts display at the same time."""
    plt.show()


# ============================================================================
# =============== OTHER ======================================================
# ============================================================================

if other_enabled:
    """Here goes miscellaneous actions, such as debugging"""
    # display(df_rental.OrderDate.dt.month)
    # df_year = df_rental.OrderDate.dt.year.to_frame()

    # display(df_year)
    # df_year.columns = ['Index', 'Year']
    # print(f"2021: {df_year[df_year.OrderDate == 2021].shape[0]}")
    # print(f"2020: {df_year[df_year.OrderDate == 2020].shape[0]}")
    # print(f"2019: {df_year[df_year.OrderDate == 2019].shape[0]}")



# ============================================================================
# ======== UPDATE BUILD INFO =================================================
# ============================================================================

if new_build:
    while True:
        try:
            df_customer.to_csv("karvedata/CUSTOMER.csv", header=False, index=False)
            df_ski.to_csv("karvedata/SKI.csv", header=False, index=False)
            df_binding.to_csv("karvedata/BINDING.csv", header=False, index=False)
            df_mounted_ski.to_csv("karvedata/MOUNTED_SKI.csv", header=False, index=False)
            df_rental.to_csv("karvedata/RENTAL.csv", header=False, index=False)
            df_damage.to_csv("karvedata/DAMAGE.csv", header=False, index=False)
            df_ski.to_csv("karvedata/SKI.csv", header=False, index=False)
            df_binding.to_csv("karvedata/BINDING.csv", header=False, index=False)
            df_mounted_ski.to_csv("karvedata/MOUNTED_SKI.csv", header=False, index=False)
            build_info.to_csv("build_info.txt", header=False, index=False, sep=' ')
            break
        except:
            print("Something went wrong. Try again?")
            retry = input("")
            if not retry == "no":
                continue

    build_info.loc[1] = "exe_time(s)", elapsed_time
    build_info.loc[2] = "customers", num_customers
    build_info.loc[3] = "mounted_skis", num_mounted_skis
    build_info.loc[4] = "rentals", num_rentals
    build_info.loc[5] = "skis_retired", skis_retired
    build_info.loc[6] = "percent_retired", (skis_retired / num_mounted_skis)
    build_info.loc[7] = "skis_totaled", skis_totaled
    build_info.loc[8] = "percent_totaled", (skis_totaled / num_mounted_skis)
    build_info.loc[9] = "percent_deactivated", ((skis_totaled + skis_retired) / num_mounted_skis)


print(f"Execution time: {elapsed_time}")
build_info.to_csv("build_info.txt", header=False, index=False, sep=' ')





