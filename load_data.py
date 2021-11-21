import pandas as pd
import numpy as np
"""
NOTES
Next quarter will build full stack web apps 
using MongoDB, Express.js, Angular, Node.js
"""

class Data:
    df_customer = pd.read_csv("karvedata/CUSTOMER.csv", header=None)
    df_rental = pd.read_csv("karvedata/RENTAL.csv", header=None)
    df_damage = pd.read_csv("karvedata/DAMAGE.csv", header=None)
    df_damage_type = pd.read_csv("karvedata/DAMAGE_TYPE.csv", header=None)
    df_mounted_ski = pd.read_csv("karvedata/MOUNTED_SKI.csv", header=None)
    df_ski = pd.read_csv("karvedata/SKI.csv", header=None)
    df_ski_model = pd.read_csv("karvedata/SKI_MODEL.csv", header=None)
    df_binding = pd.read_csv("karvedata/BINDING.csv", header=None)
    df_binding_model = pd.read_csv("karvedata/BINDING_MODEL.csv", header=None)
    df_ski_type = pd.read_csv("karvedata/SKI_TYPE.csv", header=None)
    df_brand = pd.read_csv("karvedata/BRAND.csv", header=None)

    df_bootsizes = pd.read_csv("sampledata/bootsizes.csv", header=None)
    df_skitowns = pd.read_csv("sampledata/skitowns.csv", header=None, dtype=str)
    df_address_dob_signup = pd.read_csv("sampledata/address_dob_signupdate.csv", header=None)
    df_street = pd.read_csv("sampledata/address_dob_signupdate.csv", header=None)[0]
    df_dob = pd.read_csv("sampledata/address_dob_signupdate.csv", header=None)[1]
    df_signup = pd.read_csv("sampledata/address_dob_signupdate.csv", header=None)[2]
    arr_emailtypes = pd.read_csv("sampledata/emailtypes.txt", header=None)[0].to_numpy()
    arr_boynames = pd.read_csv("sampledata/boynames.txt", header=None)[0].to_numpy()
    arr_girlnames = pd.read_csv("sampledata/girlnames.txt", header=None)[0].to_numpy()
    arr_lastnames = pd.read_csv("sampledata/lastnames.txt", header=None)[0].to_numpy()

    df_customer.columns = [
        'CustomerID', 'FirstName', 'LastName', 'Email',
        'Street', 'City', 'State', 'Zipcode',
        'SignupDate', 'DOB', 'Gender', 'Height',
        'Weight', 'Ability', 'BootSize', 'BSL'
    ]
    df_rental.columns = [
        'RentalID', 'CustomerID', 'MountedSkiID', 'OrderDate', 'ReturnDate',
        'DaysUsed', 'Tuned'
    ]
    df_damage.columns = [
        'RentalID', 'DamageTypeID'
    ]
    df_damage_type.columns = [
        'DamageTypeID', 'DamageDescription', 'Fee', 'SkiTotaled'
    ]
    df_mounted_ski.columns = [
        'MountedSkiID', 'BindingID', 'SkiID', 'MountDate', 'ActiveMountedSki'
    ]
    df_ski.columns = [
        'SkiID', 'SkiModelID', 'PurchaseDate', 'Length', 'ActiveSki'
    ]
    df_ski_model.columns = [
        'SkiModelID', 'SkiTypeID', 'BrandName', 'Name', 'WaistWidth',
        'ModelYear', 'LengthsAvailable'
    ]
    df_ski_type.columns = [
        'SkiTypeID', 'Category', 'Gender'
    ]
    df_brand.columns = [
        'BrandName', 'BrandTypeID', 'Country', 'YearEstablished', 'Description'
    ]
    df_binding.columns = [
        'BindingID', 'BindingModelID', 'PurchaseDate', 'ActiveBinding'
    ]
    df_binding_model.columns = [
        'BindingModelID', 'BindingBrand', 'BindingName', 'MaxDin', 'MinDin',
        'MaxBSL', 'MinBSL', 'BindingModelYear'
    ]

    df_rental['OrderDate'] = pd.to_datetime(df_rental['OrderDate'])
    df_rental['ReturnDate'] = pd.to_datetime(df_rental['ReturnDate'])

    df_rental.DaysUsed = df_rental.DaysUsed.astype(int)

    df_skitowns.columns = ['City', 'State', 'Zip', 'Weight']
    df_bootsizes.columns = ['size','bsl']

    df_skitowns.Weight = df_skitowns.Weight.astype(float)

