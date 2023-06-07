# M/M/1
# Entrada dada por um processo Poison
# Servico dada por uma distribuicao exponencial

import matplotlib.pyplot as plt
import numpy as np
import math

# Sets the random number generator seed to 1
np.random.seed(1)

# Initializes the number of customers in the system and the simulation time 
n = 0
simultime = 0

# Variables which armazenate the times of arrival and departure
tax_arrival = 1         # arrival time (1/lambda, where lambda=1)
tax_departure = 0.5     # service time (1/mi, where mi=2)

# This variable stores the time of arrival of each first customer, when the system is empty. It will be acessed during a arrival event.
firstCustomer = 0

# This array stores the busy periods of the server. It will be acessed during a departure event.
# Values consist of time_of_service (of last customer before empty) - time_of_arrival (of first customer after empty)
busyPeriod = []

# This function calculates confidence interval
def confidenceInterval(list):
    minCI = np.mean(list) - (1.96 * (np.std(list) / math.sqrt(len(list)) ))
    maxCI = np.mean(list) + (1.96 * (np.std(list) / math.sqrt(len(list)) ))
    return minCI, maxCI

MAXITERATION = 10000
# Starts the main simulation loop, which iterates MAXITERATION times.
for i in range(MAXITERATION):

    # this block get samples exponentially distributed by the variables tax_arrival or tax_departure
    time_of_arrival = np.random.exponential(tax_arrival)
    time_of_departure = np.random.exponential(tax_departure)

    if (n==0 or time_of_arrival < time_of_departure):
        simultime += time_of_arrival
        #print(f"[{simultime:08.4f}] {'arrival':>10}, {n} => {n + 1}")      # This block prints out a message indicating the arrival,
        n += 1                                                              # updates the number of customers in the system
        if(n==1): firstCustomer = simultime                                 # register the arrival of first customer

    else:
        simultime += time_of_departure
        #print(f"[{simultime:08.4f}] {'departure':>10}, {n} => {n - 1}")     # This block prints out a message indicating the departure,
        n -= 1                                                              # updates the number of customers in the system
        if(n==0): busyPeriod.append(simultime-firstCustomer)                # register busy period

print(f"\nMax iteration number ({MAXITERATION}) reached. End of simulation\n")

# this block prints number of busy periods and their average
print(f"Number of busy periods of server (samples): {len(busyPeriod)}")
print(f"Average Busy Period: {np.mean(busyPeriod):08.4f}")

# this block gets the confidence interval and prints it
ciMin, ciMax = confidenceInterval(busyPeriod)
print(f"Confidence Interval: [{ciMin:08.4f}, {ciMax:08.4f}]\n")

#"""
#this block creates a bar graph for comparison of duration of the busy periods
print("\nCreating Busy Period bar graph...\n")
x_w = list(range(0, len(busyPeriod)))
plt.bar(x_w, busyPeriod, color ='blue',width = 0.7)
plt.xlabel("Busy periods")
plt.ylabel("Time in seconds")
plt.title("Busy Period Comparison")
plt.show()
#"""
