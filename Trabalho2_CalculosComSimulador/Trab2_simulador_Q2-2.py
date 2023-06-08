# M/M/1
# Entrada dada por um processo Poison
# Servico dada por uma distribuicao exponencial

import matplotlib.pyplot as plt
import numpy as np
import math

# Sets the random number generator seed to 1
np.random.seed()

# This block defines lambda, mu and the Average Busy Period (ABP = E(B_C)) according mathematical analysis of Question 2.1
LAMBDAMM1 = 1
MUMM1 = 2
ABP = (1/MUMM1)/(1-(LAMBDAMM1/MUMM1))

# This function calculates confidence interval
def confidenceInterval(list):
    minCI = np.mean(list) - (1.96 * (np.std(list) / math.sqrt(len(list)) ))
    maxCI = np.mean(list) + (1.96 * (np.std(list) / math.sqrt(len(list)) ))
    return minCI, maxCI

# this function calculates number of busy periods, their average, confidence interval and if expected values are within the interval 
def metricsTimeToLastClient(list, c):

    expectedValue = (c*ABP) - ABP       # E(U_C) = C*E(B_C) - E(B_C) according to mathematical analysis of Question 2.2

    ciMin, ciMax = confidenceInterval(list)
    print(f"Number of samples: {len(list)}")
    print(f"Average Time until 1 client, C = {c}: {np.mean(list):.4f}")
    print(f"Confidence Interval: [{ciMin:.4f}, {ciMax:.4f}]")

    if(ciMin<=expectedValue<=ciMax):
        print(f"Success. Expected value {expectedValue} within confidence interval.\n")
        return True

    else:
        print(f"Failure. Expected value {expectedValue} NOT within confidence interval.\n")
        return False


# this function realiza a M/M/1 simulation
# This simulator specifically starts with predefined customers and ends when the server reaches 1 customer for the first time
def simulatorMM1(n):
    
    # Initializes the simulation time 
    simultime = 0

    # Variables which armazenate the times of arrival and departure
    tax_arrival = 1         # arrival time (1/lambda, where lambda=1)
    tax_departure = 0.5     # service time (1/mu, where mu=2)

    #print(f"\nBeginning M/M/1 simulator with {n} customers.\n")

    # Starts the main simulation loop, which iterates until the server reaches 1 customer
    while(1):

        # this block get samples exponentially distributed by the variables tax_arrival or tax_departure
        time_of_arrival = np.random.exponential(tax_arrival)
        time_of_departure = np.random.exponential(tax_departure)

        if (n==0 or time_of_arrival < time_of_departure):
            simultime += time_of_arrival
            #print(f"[{simultime:08.4f}] {'arrival':>10}, {n} => {n + 1}")      # This block prints out a message indicating the arrival,
            n += 1                                                              # updates the number of customers in the system

        else:
            simultime += time_of_departure
            #print(f"[{simultime:08.4f}] {'departure':>10}, {n} => {n - 1}")    # This block prints out a message indicating the departure,
            n -= 1                                                              # updates the number of customers in the system
            if(n==1): break                                                     # end simulation loop

    #print(f"\nSystem empty. End of simulation with {simultime:08.4f} time\n")
    return simultime                                                            # Return time until last client in the server

# This block defines the range of starting number of customers in the system and number of iterations
MINCUSTOMERS = 2
MAXCUSTOMERS = 10
NUMITERATIONS = 400

#This block defines list of average times and variable of successes
avgTimeToLastClient = []
successes = 0

# This block executes the program based on Question 2.2 parameters
for numC in range (MINCUSTOMERS,MAXCUSTOMERS+1):
    temp = []
    for i in range (NUMITERATIONS):
        temp.append(simulatorMM1(numC))
    if(metricsTimeToLastClient(temp, numC)): successes += 1
    avgTimeToLastClient.append(np.mean(temp))
print(f"Simulation ended with {successes}/{MAXCUSTOMERS-MINCUSTOMERS+1} successes.\n")

#"""
#this block creates a bar graph for comparison of duration of the times to 1 client
print("Creating Time To Last Client bar graph...\n")
x = list(range(MINCUSTOMERS,MAXCUSTOMERS+1))
plt.bar(x, avgTimeToLastClient, color ='blue',width = 0.7)
plt.xlabel("C = 2, 3, ..., 10")
plt.ylabel("Average Time To Last Client")
plt.title("Time To Last Client Comparison")
plt.show()
#"""
