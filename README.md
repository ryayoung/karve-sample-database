# Karve Sample Database
The algorithms in these python scripts generate highly realistic business data to populate all *operational* tables in Karve, including Customer, Rental, Damage, Mounted Ski, Ski, and Binding.

It generates realistic distributions *not only* for existing measures, but also for measures that will be derived in the future, such as the number of days customers keep skis 
before swapping them, the amount and type of damage entries that get recorded in the Damage table when a rental ski is returned from a customer, or the probability that a ski will be rented based on which brand it was made by.

It even distributes the probability of a ski being rented based on when it was purchased and mounted. For example, once a ski is 2 years old, we will un-list it from our site and keep it on hand in case of inventory shortages, and let customers use it when newer models are already in use. So, its likelihood of being rented during year 3 is very low.

> A Python script to simulate real business patterns and distributions of customer data to populate the Karve database with sample data. The result is a sample SQL Server database that students can use to practice analytical tasks such as queries or visualizations to discover hidden patterns and trends in the data.

- **Here are some examples of how business operations are simulated**
   - Rental order volume and return statistics are distributed bimodally, peaking near christmas and spring break.
   - Rental operations are valid, such that a ski won't be in the hands of more than one customer at a time, won't be used after it has been damaged critically, will be rented less frequently over consecutive seasons, and always gets returned on time at the end of the season.
   - The rate at which skis get damaged, the number of damage records per order, and the frequency of different types of ski damage are distributed based on time of season, the type of rider, and the type of ski.
   - All customers are treated as real people. Thus, their key identifiers (name, gender, email, home address) line up with each other, and their body type and rider metrics (height, weight, boot size, ability) are aligned with each other. Those metrics also follow the distributions of real people.
   
1. Simulate real business patters
    * Create an order volume distribution that's bimodal, peaking in Dec. and Mar. Then, _based on time of season_, choose how the length of time customers keep skis for will be distributed. This is skewed right for most of the season, but shortens in the spring since all rentals _must_ be returned by July 7th.   
   * Choose how often skis get damaged, which types of damage are most common, how often multiple (2-3) damages occur in one rental event, how often a ski gets totaled/broken, and which types of critical damage are most common. And, when a ski does get totaled, update records to permanently prevent it from being rented again.

2. Simulate a realistic distribution for each measure and include dependencies
    * Pick what percent of customers are male/female.
    * Height will be normally distributed based on gender.
    * Weight will be based on height, and also normally distributed differently based on gender.
    * Boot size will be normally distributed based on gender.
    * Boot sole length will be based on boot size and then randomized within 3 millimeters.
    * Skier ability level will be slightly skewed towards advanced skiers
    * Days Used (# of days a customer _claims_ to have actually used the ski) will roughly correlate with the # of days between order and return date.

### Here are some visualizations of the data:

[<img src="plots/hist_days_kept.png" height="450"/>]()
[<img src="plots/order_date_month.png" height="450"/>]()
[<img src="plots/order_date_year.png" height="450"/>]()
[<img src="plots/customer_boot_size.png" height="450"/>]()
[<img src="plots/customer_height.png" height="450"/>]()
[<img src="plots/customer_weight.png" height="450"/>]()
[<img src="plots/customer_ability_female.png" height="450"/>]()

### Notes for running scripts:
```main_driver.py``` is the file to configure and run.

New data is loaded into CSV files stored in ```/karvedata```.

If you configured main to load data for customers, skis, AND rentals, it will document the output as a new "build" and update ```build_info.txt``` with the latest version number and descriptive info. It will also automatically update the plots in ```/plots```.

Time complexity is linear for loading Customers and Ski/Binding/MountedSki. HOWEVER, time complexity to compute new Rental events depends on the ratio of mounted skis to rental events. Remember, the algorithm needs to place each rental event at a time that doesn't conflict with the customer or ski's previous rentals. So, for example, if you tell it to generate 30,000 rental events over 5 years with only 200 mounted skis available for rental, where skis are kept for around 30 days at a time on average, the program will obviously NOT work. But if you tell it to generate 1000 rental events, given 1000 mounted ski pairs to work with, it will run linearly without a problem.
