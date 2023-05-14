# M/D/1
# Entrada dada por um processo Poison
# Servico dada por uma distribuicao exponencial

import numpy as np
import math

# Sets the random number generator seed to 1
np.random.seed(1)

# Initializes the number of customers in the system and the simulation time 
n = 0
simultime = 0

# Variables which armazenate the times of arrival and departure
tax_arrival = 1         # arrival time
tax_service = 0.5       # service time

# This array stores the time of arrival of each customer. It will be acessed during a arrival event.
arrivals = []

# This array stores the waiting times of each customer. It will be acessed during a departure event.
# Values consist of time_of_service - time_of_arrival of each customer
waits = []

# Array stores the number of customers each iteration
customers = []

# This function calculates useful metrics of chosen list
def metrics(list):
    return len(list), np.mean(list), np.std(list), 1.96

# This function calculates confidence interval
def confidenceInterval(samples, mean, std, precision):
    minCI = mean - (precision * (std / math.sqrt(samples) ))
    maxCI = mean + (precision * (std / math.sqrt(samples) ))
    return minCI, maxCI

MAXITERATION = 1000
# Starts the main simulation loop, which iterates MAXITERATION times or until there are no more events in the queue.
for i in range(MAXITERATION):

    # this block gets an arrival sample exponentially distributed by the variable tax_arrival
    time_of_arrival = np.random.exponential(tax_arrival)
    # this block gets a deterministic service sample  
    time_of_service = tax_service

    if (n==0 or time_of_arrival < time_of_service):
        simultime += time_of_arrival
        print(f"[{simultime:08.4f}] {'arrival':>10}, {n} => {n + 1}")       # This block prints out a message indicating the arrival,
        n += 1                                                              # updates the number of customers in the system
        customers.append(n)                                                 # appends current number of customers
        arrivals.append(simultime)                                          # appends arrival of current customer

    else:
        simultime += time_of_service
        print(f"[{simultime:08.4f}] {'departure':>10}, {n} => {n - 1}")     # This block prints out a message indicating the departure,
        n -= 1                                                              # updates the number of customers in the system
        customers.append(n)                                                 # appends current number of customers
        waits.append(simultime-arrivals[0])                                 # appends waiting time of departing customer
        arrivals.pop(0)

print(f"\nMax iteration number ({MAXITERATION}) reached. End of simulation\n")

# this block gets the number of customeres serviced, average waiting time and standard deviation of waiting time
samples_w, mean_w, std_w, precision_w = metrics(waits)

# this block prints customers serviced and average waiting time
print(f"Number of customers serviced (samples): {samples_w}")
print(f"Average Waiting Time: {mean_w:08.4f}")

# this block gets the confidence interval and prints it
ciMin_w, ciMax_w = confidenceInterval(samples_w, mean_w, std_w, precision_w)
print(f"Confidence Interval: [{ciMin_w:08.4f}, {ciMax_w:08.4f}]\n")

# this block gets the number of customers per iteration, average number of customers and standard deviation of customers in the system
samples_c, mean_c, std_c, precision_c = metrics(customers)

# this block prints average number of customers in the system
print(f"Average number of customers in the system: {mean_c:08.4f} customers")

# this block gets the confidence interval and prints it
ciMin_c, ciMax_c = confidenceInterval(samples_c, mean_c, std_c, precision_c)
print(f"Confidence Interval: [{ciMin_c:08.4f}, {ciMax_c:08.4f}]")