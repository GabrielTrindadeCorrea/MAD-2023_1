# M/M/1
# Entrada dada por um processo Poison
# Servico dada por uma distribuicao exponencial

import matplotlib.pyplot as plt
import numpy as np
import math

# Sets the random number generator seed to 1
np.random.seed()

# Initializes the number of customers in the system and the simulation time 
n = 0
simultime = 0

# Variables which armazenate the times of arrival and departure
tax_arrival = 1         # arrival time (1/lambda, where lambda=1)
tax_departure = 0.5     # service time (1/mi, where mi=2)

# This array stores the time of arrival of each customer of the desired sequence. It will be acessed during a arrival event.
#For this case, its C = 2,3,4,...,10
customerSequence = {2:0.0, 3:0.0, 4:0.0, 5:0.0, 6:0.0, 7:0.0, 8:0.0, 9:0.0, 10:0.0}

# This array stores the busy periods of the server. It will be acessed during a departure event.
# Values consist of time_of_service (of last customer before empty) - time_of_arrival (of first customer after empty)
busyPeriod = {2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[]}

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
        if(2 <= n <= 10):
            customerSequence[n] = simultime                                 # register the arrival of target customer (2 -> 10)

    else:
        simultime += time_of_departure
        #print(f"[{simultime:08.4f}] {'departure':>10}, {n} => {n - 1}")     # This block prints out a message indicating the departure,
        n -= 1                                                              # updates the number of customers in the system
        if(n==0):
            for i in range (2,11):
                if (customerSequence.get(i)!=0.0):                      # Verify if the i-th customer arrived
                    temp = busyPeriod.get(i)                            #
                    temp.append(simultime-customerSequence.get(i))      # this block registers the desired busy periods
                    busyPeriod[i] = temp                                #
            customerSequence.update({2:0.0, 3:0.0, 4:0.0, 5:0.0, 6:0.0, 7:0.0, 8:0.0, 9:0.0, 10:0.0})         #resets the times of arrival

print(f"\nMax iteration number ({MAXITERATION}) reached. End of simulation\n")

means = []
samples = []

# this block prints number of busy periods, their average and the confidence interval
for i in range (2,11):
    periods = busyPeriod.get(i)
    numSamples = len(periods)
    samples.append(numSamples)
    if(numSamples):
        avg = np.mean(periods)
        means.append(avg)
        ciMin, ciMax = confidenceInterval(periods)
        print(f"Average Busy Period, C={i}: {avg:08.4f} . Number of samples: {numSamples}")
        print(f"Confidence Interval: [{ciMin:08.4f}, {ciMax:08.4f}]\n\n")
    else:
        means.append(0.0)
        print(f"Average Busy Period, C={i}: {0.0} . Number of samples: {numSamples}")
        print(f"Confidence Interval: [{0.0}, {0.0}]\n\n")


#"""
#this block creates a bar graph for comparison of duration of the busy periods
print("\nCreating Busy Period bar graph...\n")
x_w = list(range(2,11))
plt.bar(x_w, means, color ='blue',width = 0.7)
plt.xlabel("C = 2, 3, ..., 10")
plt.ylabel("Average Busy Period")
plt.title("Busy Period Comparison")
plt.show()
#"""

#"""
#this block creates a bar graph for comparison of duration of the busy periods
print("\nCreating Samples bar graph...\n")
x_w = list(range(2,11))
plt.bar(x_w, samples, color ='blue',width = 0.7)
plt.xlabel("C = 2, 3, ..., 10")
plt.ylabel("Number of Samples")
plt.title("Number of Samples Comparison")
plt.show()
#"""
