import os
import pandas as pd
import numpy as np
import random
import calendar
# from IPython import display
from datetime import timedelta, datetime#,date
from scipy.stats import skewnorm
# import matplotlib.pyplot as plt

max_year = 2021

def random_date(year, month):
    """
    Returns a random day in a given month and year.
    """
    dates = calendar.Calendar().itermonthdates(year, month)
    return np.random.choice([date for date in dates if date.month == month])

def clear_df(df):
    """
    Why did I make a function for this, you ask? READABILITY!!!
    """
    return df[0:0]

def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

def get_exp_growing_year():
    """
    Returns a year with a distribution that grows exponentially
    from 2016 to 2021.
    """
    return np.random.choice(
        [2016, 2017, 2018, 2019, 2020, 2021],
        p=(.05,.06,.08,.15,.24,.42))

def get_month_rental_dist():
    """
    Returns a month with a distribution that represents
    customer rental order activity
    """
    return np.random.choice(
        [9, 10, 11, 12, 1, 2, 3, 4, 5, 6],
        p=(.03,.06,.12,.20,.17,.13,.16,.09,.03,.01))

def get_brand_dist():
    """
    Returns a brand with a custom distribution. Some brands are much
    more popular than others, so we use this when purchasing skis from
    a list of ski models.
    """
    return np.random.choice(
        ['4FRNT','Icelantic','Moment','ON3P','Rossignol'],
        p=(.08,.27,.28,.22,.15))

def get_gender_dist():
    """
    Returns a gender according to a distribution of our choice.
    72% male, 28% female. The real world overall ski population is
    more like 60/40, but we assume a business like ours would appeal much
    more to men than to women.
    """
    return np.random.choice(['m','f'], p=(.72,.28))

def gen_customer(df_customer, arr_boynames, arr_girlnames, arr_lastnames, arr_emailtypes,
        df_street, df_skitowns, df_dob, df_bootsizes, pretty_print=True):
    """
    Generates realistic customer data.
    Returns a single row dataframe.
    """

    # CUSTOMER ID
    customer_id = -1
    try:
        customer_id = int(df_customer[['CustomerID']].max()) + 1
    except ValueError:
        customer_id = 1
        print('YAY! Generating first customer.')

    # GENDER
    gender = str(np.random.choice(['m','f'], p=(.72,.28)))

    # FIRST NAME
    first_name = ""
    if gender == 'm':
        first_name = str(np.random.choice(arr_boynames))
    else:
        first_name = str(np.random.choice(arr_girlnames))

    # LAST NAME
    last_name = str(np.random.choice(arr_lastnames))

    # EMAIL
    provider = np.random.choice(arr_emailtypes)
    email = str(np.random.choice([
        f'{last_name.lower()}.{first_name[0].lower()}@{provider}.com',
        f'{first_name.lower()}{last_name[0].lower()}{np.random.randint(1,999)}@{provider}.com',
        f'{last_name.lower()}{first_name.lower()}{np.random.randint(1,999)}@{provider}.com',
        f'{first_name.lower()}{last_name.lower()}{np.random.randint(1,999)}@{provider}.com'
    ]))

    # STREET
    street = str(np.random.choice(df_street))

    # CITY, STATE, ZIP
    city = random.choices(df_skitowns.City.to_list(), weights=df_skitowns.Weight.to_list())[0]
    location = df_skitowns[df_skitowns['City'] == city].sample()
    state = str(location.State.iloc[0])
    zip = str(location.Zip.iloc[0])

    # SIGNUP DATE: pick randomly from address_dob_signup
    # Select year
    # Signups should grow exponentially
    year = get_exp_growing_year()
    # Select month
    # Signups close at the end of january, and re-open every august
    month = np.random.choice(
        [8, 9, 10, 11, 12, 1],
        p=(.10, .08, .15, .20, .24, .23))

    signup_date = str(random_date(year, month))
    signup_date = pd.to_datetime(signup_date)


    # DOB: pick randomly from address_dob_signup
    dob = str(np.random.choice(df_dob))

    # Height: generate normal distribution
    height = 0
    while True:
        if gender == 'm':
            height = int(np.random.normal(69, 3.0, 1))
        else:
            height = int(np.random.normal(64, 2.8, 1))
        if 57 <= height <= 79:
            break
    height = int(height)

    # WEIGHT: Generate normal distribution
    weight = 0
    # Figure out how much their height deviates from the average human height
    height_deviation = - (66 - height)
    # Change the mean by this value.
    mu = 140 + height_deviation
    while True:
        if gender == 'm':
            weight = int(np.random.normal(mu+25, 25, 1))
        else:
            weight = int(np.random.normal(mu, 22, 1))
        if 90 <= weight <= 250:
            break
    weight = int(weight)

    # ABILITY: Pick random int 1-3 but left skewed from advanced skiers
    if gender == 'm':
        ability_level = np.random.choice([1,2,3], p=(.2,.35,.45))
    else:
        ability_level = np.random.choice([1,2,3], p=(.16,.33,.51))


    # BOOT SIZE: Pick at random (normal dist) from bootsizes, based on gender
    boot_size = 0.0
    while True:
        if gender == 'm':
            boot_size = int(np.random.normal(27.5, 2, 1)[0]) + 0.5
        else:
            boot_size = int(np.random.normal(25.5, 1.5, 1)[0]) + 0.5
        if 22.5 <= boot_size <= 31.5: # Only accept this value if it's within the valid size range
            break

    # BSL: pick corresponding average BSL, and randomize so bsl falls within 3mm of average for that boot size
    bsl = int(df_bootsizes[['bsl']][df_bootsizes['size'] == boot_size].iloc[0])
    bsl += np.random.randint(-3,4)

    if pretty_print:
        print()
        print('----- GENERATING NEW CUSTOMER -----')
        print(f"ID:             {customer_id}")
        print(f"Name:           {first_name} {last_name}")
        print(f"Email:          {email}")
        print(f"Street:         {street}")
        print(f"City:           {city}")
        print(f"State:          {state}")
        print(f"Zipcode:        {zip}")
        print(f"SignupDate:     {signup_date}")
        print(f"DOB:            {dob}")
        print(f"Gender:         {gender}")
        print(f"Height:         {height}")
        print(f"Weight:         {weight}")
        print(f"Ability:        {ability_level}")
        print(f"Boot Size:      {boot_size}")
        print(f"BSL:            {bsl}")

    # LOAD ALL DATA INTO A 1 ROW DATAFRAME AND RETURN
    new_customer = pd.DataFrame({
        'CustomerID':[customer_id], 'FirstName':[first_name],
        'LastName':[last_name], 'Email':[email],
        'Street':[street], 'City':[city],
        'State':[state], 'Zipcode':[zip],
        'SignupDate':[signup_date], 'DOB':[dob],
        'Gender':[gender], 'Height':[height],
        'Weight':[weight], 'Ability':[ability_level],
        'BootSize':[boot_size], 'BSL':[bsl]
    })
    return new_customer



def gen_ski(df_ski, df_ski_model, df_ski_type, pretty_print=True):
    # SKI ID: Generate next number
    """
    Realistically generates a ski from our available ski models.
    Returns a single row dataframe.
    In the driver, the binding and mounted_ski will depend on the purchase
    date of this generated ski.
    """
    try:
        ski_id = int(df_ski[['SkiID']].max()) + 1
    except ValueError:
        print("Buying your first set of skis YEEEWWW!!!")
        ski_id = 1

    # SKI MODEL: Choose random BASED ON brand and gender distributions
    df_ski_model_info = inner_join(df_ski_model, 'SkiTypeID', df_ski_type)
    while True:
        brand = get_brand_dist()
        gender = get_gender_dist()
        choices = df_ski_model_info[(df_ski_model_info['BrandName'] == brand) & (df_ski_model_info['Gender'] == gender)]
        if choices.shape[0] > 0:
            break
    # chosen_ski_model = df_ski_model.sample()
    chosen_ski_model = choices.sample()
    ski_model_id = int(chosen_ski_model[['SkiModelID']].iloc[0]['SkiModelID'])

    # PURCHASE DATE: Pick a random date from august to october
    year = get_exp_growing_year()
    # year = np.random.randint(min_year, max_year)
    month = np.random.randint(8,10)
    ski_purchase_date = random_date(year, month)
    ski_purchase_date = pd.to_datetime(ski_purchase_date)

    # LENGTH: pick at random from available lengths in ski model that was chosen
    # make string
    lengths_available = str(chosen_ski_model[['LengthsAvailable']].iloc[0]['LengthsAvailable'])
    # split string into array
    lengths_available = np.fromstring(lengths_available, dtype=int, sep=' ')
    # pick from array
    length = int(np.random.choice(lengths_available))

    # ACTIVE
    active = 1

    if pretty_print:
        # PRINT RESULTS
        print()
        print(f"----- PURCHASE NEW SKI -----")
        print(f"SkiID: {ski_id}\nSkiModelID: {ski_model_id}")
        model_name = str(chosen_ski_model[['Name']].iloc[0]['Name'])
        print(f"{model_name} is available in: ", end='')
        print(lengths_available)
        print(f"Purchased size {length} on {ski_purchase_date}.")

    new_ski = pd.DataFrame({
        'SkiID':[ski_id],
        'SkiModelID':[ski_model_id],
        'PurchaseDate':[ski_purchase_date],
        'Length':[length],
        'ActiveSki':[active]
    })
    # ---- END FUNCTION gen_ski() ----
    return new_ski

def gen_binding(df_binding, df_binding_model, year, month):
    """
    Generates a binding.
    Returns a single row dataframe.
    Call this function right after calling gen_ski. Pass the
    year and month from the generated ski as params here. Then,
    the month/year will be the same but the actual purchase date will
    be random.
    """
    # BINDING ID
    try:
        binding_id = int(df_binding[['BindingID']].max()) + 1
    except ValueError:
        print("Buying your first set of bindings YEEEWWW!!!")
        binding_id = 1

    # BINDING MODEL ID
    binding_model_id = int(df_binding_model.sample()[['BindingModelID']].iloc[0]['BindingModelID'])

    # Select year
    binding_purchase_date = random_date(year, month)
    binding_purchase_date = pd.to_datetime(binding_purchase_date)

    # ACTIVE
    active = 1

    new_binding = pd.DataFrame({
        'BindingID':[binding_id],
        'BindingModelID':[binding_model_id],
        'PurchaseDate':[binding_purchase_date],
        'ActiveBinding':[active]
    })
    return new_binding


def gen_mount_this_ski(df_mounted_ski, ski_id, binding_id, year, month):
    """
    Creates a new mounted_ski entry (single row dataframe)
    given a ski ID, binding ID, and time. Call this function right after
    generating a ski and binding, and pass the ski purchase year and month
    as params. This function will simulate the ski and binding being mounted
    together at a random day, exactly 1 month after the ski and binding were
    purchased.
    """

    # SELECT ID
    try:
        mounted_ski_id = int(df_mounted_ski[['MountedSkiID']].max()) + 1
    except ValueError:
        print("Generating first mounted_ski! YEEEWW!!")
        mounted_ski_id = 1

    # NOTICE: The ski gets mounted 1 month after binding and ski were purchased
    mounted_ski_mount_date = random_date(year, month + 1)
    mounted_ski_mount_date = pd.to_datetime(mounted_ski_mount_date)

    active = 1

    new_mounted_ski = pd.DataFrame({
        'MountedSkiID':[mounted_ski_id],
        'BindingID':[binding_id],
        'SkiID':[ski_id],
        'MountDate':[mounted_ski_mount_date],
        'ActiveMountedSki':[active]
    })
    return new_mounted_ski



def inner_join(df1, key, df2, var='None'):
    """
    Returns a dataframe with df2 inner joined to df1.
    If a variable is passed, only that column from df2 will be joined to df1.
    """
    if var == 'None':
        df2 = df2
    else:
        df2 = df2[[key, var]]
    merged = pd.merge(df1, df2, on=key, how='inner')
    return merged


def damage(rental_id, damage_type_id):
    """
    Returns a DataFrame with a RentalID and DamageTypeID pair
    """
    return pd.DataFrame({
        'RentalID':[rental_id],
        'DamageTypeID':[damage_type_id]
    })

def gen_damage(rental_id, df_damage):
    """
    Algorithm for realistically damaging skis that are returned from customers
    Returns the updated damage table, and whether or not the ski was totaled
    """
    damage_table = df_damage
    totaled_ski = False
    # Pick whether any damage occurs.
    caused_damage = np.random.choice([True,False], p=(.38, .62))
    if not caused_damage:
        pass
    else:
        # Pick whether the ski is totaled (it probably isn't)
        totaled_ski = np.random.choice([True,False], p=(0.03, 0.97))
        if totaled_ski:
            # Ski is totaled, so we only record ONE damage entry. (why charge $5 for delamination if the ski is broken)
            # Pick from the 3 types of critical damage:
            # TYPES: 10: core unrepairable, 20: edge break, 30: full ski break
            damage_type = np.random.choice([10,20,30], p=(.60,.30,.10))
            damage_table = damage_table.append(damage(rental_id, damage_type), ignore_index=True)
        else:
            # Ski isn't totaled, so we might record multiple types of damage.
            # We need at LEAST 1 damage, since we already decided the ski was damaged
            # TYPES: 1: edge scratching, 2: Base core shot, 3: delamination. Pick one and add it.
            first_damage = np.random.choice([1, 2, 3], p=(.50, .30, .20))
            damage_table = damage_table.append(damage(rental_id, first_damage), ignore_index=True)
            # Decide if there will be additional damages to the ski
            more_damage = np.random.choice([True,False], p=(.30, .70))
            if more_damage:
                possible_damages = [1, 2, 3]
                # Possibilities for additional damage CANNOT include the first damage. (NO DUPLICATES)
                possible_damages.remove(first_damage)
                # Decide how many additional damages will occur
                num_of_extra_damages = np.random.choice([1, 2], p=(.69, .31))
                # Pick randomly from the pool, n number of times
                for i in range(0, num_of_extra_damages):
                    damage_type = np.random.choice(possible_damages)
                    damage_table = damage_table.append(damage(rental_id, damage_type), ignore_index=True)
                    # remove type from the pool to prevent duplicates
                    possible_damages.remove(damage_type)
    # Returns two values because if the ski is totaled, we need to kill the ski afterwards
    return damage_table, totaled_ski


def find_active_skis(df_ski):
    return df_ski[df_ski['ActiveSki'] == True]

def find_active_bindings(df_binding):
    return df_binding[df_binding['ActiveBinding'] == True]

def find_active_mounted_skis(df_mounted_ski):
    return df_mounted_ski[df_mounted_ski['ActiveMountedSki'] == True]

def mounted_ski_info(df_ski, df_binding, df_mounted_ski, df_ski_model, df_brand, df_ski_type, df_binding_model):
    mounted_ski = find_active_mounted_skis(df_mounted_ski)
    ski_model = inner_join(df_ski_model, 'SkiTypeID', df_ski_type)
    ski_model = inner_join(ski_model, 'BrandName', df_brand, 'Country')
    ski = inner_join(find_active_skis(df_ski), 'SkiModelID', ski_model)
    binding = inner_join(find_active_bindings(df_binding), 'BindingModelID', df_binding_model)

    mounted_skis = inner_join(mounted_ski, 'SkiID', ski)
    mounted_skis = inner_join(mounted_skis, 'BindingID', binding)
    mounted_skis = mounted_skis[[
        'MountedSkiID', 'SkiID', 'BindingID', 'SkiModelID',
        'Name', 'Length', 'WaistWidth', 'Gender','MountDate',
        'LengthsAvailable', 'ModelYear', 'Category', 'SkiTypeID',
        'BindingModelID', 'BindingName', 'MaxDin'
    ]]

    return mounted_skis


def select_pair(df_customer, df_ski, df_binding, df_mounted_ski, df_ski_model, df_brand, df_ski_type, df_binding_model):
    # SELECT A "RANDOM" CUSTOMER AND MOUNTED SKI
    """
    Selects a random customer and mounted ski pair.
    If gender is male, select a men's ski.
    Returns customer dataframe and mounted ski dataframe
    """
    cust = df_customer.sample()
    temp_gender = cust[['Gender']].iloc[0][0]
    possible_skis_info = mounted_ski_info(df_ski, df_binding, df_mounted_ski, df_ski_model, df_brand, df_ski_type, df_binding_model)

    signup_year = pd.to_datetime(cust.iloc[0].SignupDate).year

    # This line filters the possible skis to only include those which
    # were mounted within 3 years prior to the customer signing up.
    # For example, a customer who signs up in 2021 would never rent a
    # ski that was mounted in 2016.
    possible_skis_info = possible_skis_info[pd.to_datetime(possible_skis_info.MountDate).dt.year >= (signup_year-3)]

    if temp_gender == 'm':
        possible_skis_info = possible_skis_info[possible_skis_info['Gender'] == 'm']
    temp_mtdski_id = possible_skis_info.sample()[['MountedSkiID']].iloc[0][0]
    temp_active_mtd_skis = find_active_mounted_skis(df_mounted_ski)
    ski = temp_active_mtd_skis[temp_active_mtd_skis['MountedSkiID'] == temp_mtdski_id]
    return cust, ski


def kill_ski(df_ski, ski_id):
    index = df_ski[['ActiveSki']][df_ski['SkiID'] == ski_id].index
    df_ski.at[index, 'ActiveSki'] = 0
    return df_ski

def kill_binding(df_binding, binding_id):
    index = df_binding[['ActiveBinding']][df_binding['BindingID'] == binding_id].index
    df_binding.at[index, 'ActiveBinding'] = 0
    return df_binding

def kill_mounted_ski(df_mounted_ski, mounted_ski_id):
    index = df_mounted_ski[['ActiveMountedSki']][df_mounted_ski['MountedSkiID'] == mounted_ski_id].index
    df_mounted_ski.at[index, 'ActiveMountedSki'] = 0
    return df_mounted_ski

def kill_all(df_ski, ski_id, df_binding, binding_id, df_mounted_ski, mounted_ski_id):
    df_ski = kill_ski(df_ski, ski_id)
    df_binding = kill_binding(df_binding, binding_id)
    df_mounted_ski = kill_mounted_ski(df_mounted_ski, mounted_ski_id)
    return df_ski, df_binding, df_mounted_ski, 


def gen_days_kept_nums():
    """
    Returns a numpy array of ints with a right skewed distribution.
    This will be the selection pool when deciding how many days a ski will be kept.
    """
    numValues = 10_000
    maxValue = 150
    skewness = 7   #Negative values are left skewed, positive values are right skewed.

    nums = skewnorm.rvs(a = skewness,loc=maxValue, size=numValues)  

    nums = nums - min(nums)     # Shift the set so the minimum value is equal to zero.
    nums = nums / max(nums)     # Standardize all the values between 0 and 1.
    nums = nums * maxValue      # Multiply the standardized values by the maximum value.
    nums = nums + 7             # Shift the set so minimum time is 7 days
    return nums.astype(int)


# rentals_generated = 0
# skis_retired = 0
def gen_rental(df_rental, df_customer, df_damage, df_ski, df_binding, df_mounted_ski, df_ski_model, df_brand, df_ski_type, df_binding_model, days_kept_pool, rentals_generated, skis_retired, skis_totaled):
    rental_id = -1
    valid_dates_found = False

    # Generate new rentalID
    try:
        rental_id = int(df_rental[['RentalID']].max()) + 1
    except ValueError:
        print("Generating first rental! YEEEWW!!")
        rental_id = 1

    # Count is used for debugging so we don't get stuck in an endless loop
    count = 0
    while not valid_dates_found:
        # print("Loop started")
        count += 1
        if count > 100: break
        # Randomly select a customer and mounted ski
        customer, mounted_ski = select_pair(df_customer, df_ski, df_binding, df_mounted_ski, df_ski_model, df_brand, df_ski_type, df_binding_model)

        # From chosen customer & ski, select their IDs and previous rental history
        customer_id = int(customer.iloc[0][0])
        customer_rentals = df_rental[df_rental['CustomerID'] == customer_id]
        customer_rentals = customer_rentals.reset_index(drop=True)
        mounted_ski_id = int(mounted_ski.iloc[0][0])
        mounted_ski_rentals = df_rental[df_rental['MountedSkiID'] == mounted_ski_id]
        mounted_ski_rentals = mounted_ski_rentals.reset_index(drop=True)

        # Retire the ski if it's been used too much
        too_many_uses = np.random.randint(10,16)
        if len(mounted_ski_rentals) > too_many_uses:
            skis_retired += 1
            if skis_retired % 5 == 0:
                print(f"RETIRED: {skis_retired} skis")
            ski_id = int(df_mounted_ski[df_mounted_ski['MountedSkiID'] == mounted_ski_id][['SkiID']].iloc[0][0])
            binding_id = int(df_mounted_ski[df_mounted_ski['MountedSkiID'] == mounted_ski_id][['BindingID']].iloc[0][0])
            df_ski, df_binding, df_mounted_ski = kill_all(df_ski, ski_id, df_binding, binding_id, df_mounted_ski, mounted_ski_id)
            continue

        # Make sure the customer and mounted ski ARE NOT involved in active rentals
        impossible_date = datetime(2000, 1, 1)
        if (customer_rentals['ReturnDate'] < impossible_date).any():
            continue
        if (mounted_ski_rentals['ReturnDate'] < impossible_date).any():
            continue

        """
        ==== SELECT YEAR ====
        """
        # Get the year our ski was mounted, and the year the customer signed up
        year_mounted_ski = pd.to_datetime(mounted_ski.iloc[0].MountDate).year

        """
        Most of a ski's usage will happen the year it was purchased.
        It will also be used the year after, but won't be nearly as
        popular since it's an outdated model. It will be kept for the
        third year but ONLY to be used as a backup. Now, we will pick
        the year according to a distribution that matches this scenario.
        """
        year = np.random.choice(
                [year_mounted_ski, year_mounted_ski+1, year_mounted_ski+2, year_mounted_ski+3],
                p=(.30,.45,.15,.10))
        # Year must not exceed max year
        if year > max_year:
            continue

        # Select month
        month = get_month_rental_dist()
        # Select order date
        order_date = random_date(year, month)
        order_date = pd.to_datetime(order_date)
        # print(order_date)

        # RETURN DATE ------------
        days_kept = 0
        while True:
            # Select from the days kept choice pool that's skewed right
            days_kept = int(np.random.choice(days_kept_pool, 1)[0])
            # If the ski was ordered after december, it's due back the same year. Otherwise it's due back the following year.
            return_year_due = year
            if 7 <= month <= 12:
                return_year_due = year + 1
            # Return date equals order date plus number of days kept
            return_date = order_date + timedelta(days=days_kept)
            # All orders must be returned by July 7 OF THE YEAR THAT THEY WERE ORDERED
            if return_date > datetime(return_year_due, 7, 7):
                continue
            # near impossible to keep a ski less than 7 days, since order shipping and return shipping times are included
            if days_kept < 7:
                continue
            break

        # This last test makes sure our dates don't overlap with a previous rental
        valid_dates = True
        # For each previous rental by chosen customer
        # If chosen orderdate < previous return date, AND chosen return date > previous order date, CONTINUE
        for i in range(0, len(customer_rentals)):
            if order_date < customer_rentals.at[i, 'ReturnDate'] and return_date > customer_rentals.at[i, 'OrderDate']:
                # print(f"NOPE: Customer Ordered {customer_rentals.at[i, 'OrderDate']} and returned {customer_rentals.at[i, 'ReturnDate']}")
                valid_dates = False

        # For each previous rental with chosen MountedSki
        # If chosen orderdate < previous return date, AND chosen return date > previous order date, CONTINUE
        for i in range(0, len(mounted_ski_rentals)):
            if order_date < mounted_ski_rentals.at[i, 'ReturnDate'] and return_date > mounted_ski_rentals.at[i, 'OrderDate']:
                valid_dates = False

        if not valid_dates: continue

        # If we've made it this far, then our dates are valid and we can create a new rental event.
        valid_dates_found = True

    # This is very important, and might need improvement.
    # It determines for how many days the customer chooses to actually use the ski.
    days_used_multiplier = np.random.randint(1, 9) / 10
    days_used = int(days_kept * days_used_multiplier)

    new_rental = pd.DataFrame({
        'RentalID':[rental_id],
        'CustomerID':[customer_id],
        'MountedSkiID':[mounted_ski_id],
        'OrderDate':[order_date],
        'ReturnDate':[return_date],
        'DaysUsed':[days_used],
        'Tuned':[1]
    })


    """
    Correctly totaling skis is incredibly difficult in our situation
    because we are creating rentals in a random order. If we were generating
    rental events chronologically, then the probability of a ski getting totaled would
    remain the same for each new rental. But, since we are creating events in random
    order and can only total a ski if its rental date is the most recent of all
    previous rentals, the probability of totaling a ski will decrease linearly with
    each additional rental added to a ski's rental history. This is stupid. If anything,
    the probablity of totaling should increase over time, not decrease!

    One (rather clumsy) solution is this: if we total the ski and the current rental
    event is the newest in the mounted ski's history (no rentals are recorded at
    a later date) proceed as normal and kill the ski. ELSE, start by killing the ski,
    and then find the newest rental event for the ski, and update all of its damage records 
    with the current rental id. Then, make a totaled damage entry linked to the rental ID
    of that newest rental event, instead of the current one. For example, if we total
    a ski in 2016 that has been rented in 2017, update the 2017 damage entries with
    the rental id from the 2016 rental (remember, damage entries don't have a date attached
    to them. Only a rental id). Then add a totaled damage entry for the 2017 rental,
    and kill the ski.
    """
    df_damage, ski_totaled = gen_damage(rental_id, df_damage)
    if ski_totaled:
        ski_id = int(df_mounted_ski[df_mounted_ski['MountedSkiID'] == mounted_ski_id][['SkiID']].iloc[0][0])
        binding_id = int(df_mounted_ski[df_mounted_ski['MountedSkiID'] == mounted_ski_id][['BindingID']].iloc[0][0])
        df_ski, df_binding, df_mounted_ski = kill_all(df_ski, ski_id, df_binding, binding_id, df_mounted_ski, mounted_ski_id)
        skis_totaled += 1
        if skis_totaled % 2 == 0:
            print(f"TOTALED: {skis_totaled}. Now killing ski {ski_id}")

    rentals_generated += 1
    if rentals_generated % 50 == 0:
        print(f"{rentals_generated} orders")
    return new_rental, df_damage, df_ski, df_binding, df_mounted_ski, rentals_generated, skis_retired, skis_totaled





