# Karve Sample Database
The algorithms in these python scripts generate highly realistic business data to populate all *operational* tables in Karve, including Customer, Rental, Damage, Mounted Ski, Ski, and Binding.

It generates realistic distributions *not only* for existing measures, but also for measures that will be derived in the future, such as the number of days customers keep skis 
before swapping them, the amount and type of damage entries that get recorded in the Damage table when a rental ski is returned from a customer, or the probability that a ski will be rented based on which brand it was made by.

It even distributes the probability of a ski being rented based on when it was purchased and mounted. For example, once a ski is 2 years old, we will un-list it from our site and keep it on hand in case of inventory shortages, and let customers use it when newer models are already in use. So, its likelihood of being rented during year 3 is very low.

### Here are some visualizations of the data:
