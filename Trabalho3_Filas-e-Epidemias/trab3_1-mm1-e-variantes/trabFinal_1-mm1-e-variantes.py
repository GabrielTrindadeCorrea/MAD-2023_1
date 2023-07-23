# M/M/1
# Arrival defined by a Poisson process
# Service defined by a exponential distribution

import matplotlib.pyplot as plt
import numpy as np
import math
from collections import deque
from time import time

# This function calculates confidence interval
# Requires numpy and math libraries
def confidenceInterval(list):
    #import numpy as np
    #import math
    firstTerm = np.mean(list)
    secondTerm = (1.96 * (np.std(list) / math.sqrt(len(list)) ))
    minCI = firstTerm - secondTerm
    maxCI = firstTerm + secondTerm
    return minCI, maxCI

# This function plots the CDF of waiting times and customer numbers according to professor suggestion
# <https://stackoverflow.com/questions/9378420/how-to-plot-cdf-in-matplotlib-in-python>
def plotCDF(waits, customers):
    
    wait_times_sorted = sorted(waits)
    num_customers_sorted = sorted(customers)

    plt.hist(wait_times_sorted, density=True, cumulative=True, histtype='step', alpha=0.8, color='k')
    plt.title("CDF of Waiting Times")
    plt.show()

    plt.hist(num_customers_sorted, density=True, cumulative=True,histtype='step', alpha=0.8, color='k')
    plt.title("CDF of Number of Customers in the System")
    plt.show()

# This function realizes a M/M/1 simulation
# Max iterations and initial number of customers have default values
def simulatorMM1(lambda_mm1, mu_mm1, show_messages = False, show_metrics = True, show_plots = False, max_iterations = 10000, initial_customers = 0):
    
    # Initializes the simulation time, number of customers and random number generator
    simultime = 0
    num_customers = initial_customers
    rho_mm1 = lambda_mm1/mu_mm1 
    rng = np.random.default_rng()

    # Auxiliary lists (using collections.deques) for sampling waiting times and customer numbers
    arrivals = deque([])
    waits = deque([])
    customers = deque([])

    # Variables defining parameters of arrival and departure
    # Numpy exponential function uses the scale parameter, which is the inverse of the rate parameter (in this case lambda and mu) 
    # <https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.exponential.html#numpy.random.Generator.exponential>
    arrival_scale = 1/lambda_mm1           
    departure_scale = 1/mu_mm1            

    print(f"\nBeginning M/M/1 simulator with {num_customers} customers.")
    start_time = time()

    # Starts the main simulation loop, which iterates until the max iterations is reached.
    for _ in range(max_iterations):

        # this block get samples exponentially distributed by the variables arrival_scale or departure_scale
        # while arrivals occur according to a Poisson process, time between Poisson arrivals is exponential distribution
        time_of_arrival = rng.exponential(arrival_scale)
        time_of_departure = rng.exponential(departure_scale)

        if (num_customers==0 or time_of_arrival < time_of_departure):
            simultime += time_of_arrival
            if(show_messages):
                print(f"[{simultime:08.4f}] {'arrival':>10}, {num_customers} => {num_customers + 1}")       # This block prints out a message indicating the arrival,
            num_customers += 1                                                      # updates the number of customers in the system
            customers.append(num_customers)                                         # appends current number of customers
            arrivals.append(simultime)                                              # appends arrival of current customer

        else:
            simultime += time_of_departure
            if(show_messages):
                print(f"[{simultime:08.4f}] {'departure':>10}, {num_customers} => {num_customers - 1}")     # This block prints out a message indicating the departure,
            num_customers -= 1                                                      # updates the number of customers in the system
            customers.append(num_customers)                                         # appends current number of customers
            waits.append(simultime-arrivals.popleft())                              # appends waiting time of departing customer

    end_time = time()
    print(f"\nMax iteration number ({max_iterations}) reached. End of simulation. Duration of {(end_time-start_time):.4} seconds.\n")

    # This block shows metrics of waiting times and number of customers
    if(show_metrics):
        # this block prints average number of customers in the system and confidence interval
        print(f"Sampled average number of customers in the system: {np.mean(customers):.4f} customers.")
        ciMin_c, ciMax_c = confidenceInterval(customers)
        print(f"Confidence Interval: [{ciMin_c:.4f}, {ciMax_c:.4f}]")

        if(not lambda_mm1<mu_mm1):
            print("[Arrivals] are faster than [Services], queue will grow indefinitely long!\n")
        else:
            avg_num_customers = rho_mm1/(1-rho_mm1)
            print(f"Analytical average number of customers, according to (rho/(1-rho)): {avg_num_customers} customers.")
            success = ciMin_c<=avg_num_customers<=ciMax_c
            if(success):
                print(f"SUCCESS. Expected value {avg_num_customers} within confidence interval.\n")
            else:
                print(f"FAILURE. Expected value {avg_num_customers} NOT within confidence interval.\n")

        # this block prints customers serviced, average waiting time and confidence interval
        print(f"Number of customers serviced (samples): {len(waits)}")
        print(f"Sampled average Waiting Time (waiting queue + server): {np.mean(waits):.4f}")
        ciMin_w, ciMax_w = confidenceInterval(waits)
        print(f"Confidence Interval: [{ciMin_w:.4f}, {ciMax_w:.4f}]")

        if(not lambda_mm1<mu_mm1):
            print("[Arrivals] are faster than [Services], queue will grow indefinitely long!\n")
        else:
            avg_wait_time = 1/(mu_mm1-lambda_mm1)
            print(f"Analytical average Waiting Time (waiting queue + server) according to (1/(mu-lambda)): {avg_wait_time}")
            success = ciMin_w<=avg_wait_time<=ciMax_w
            if(success):
                print(f"SUCCESS. Expected value {avg_wait_time} within confidence interval.\n")
            else:
                print(f"FAILURE. Expected value {avg_wait_time} NOT within confidence interval.\n")

    # This block shows bar graphs for each target metric
    if(show_plots):
        #this block creates a bar graph of number of customers in the system per iteration of the simulator
        print(f"Creating Customer in System bar graph with Lambda = {lambda_mm1}, Mu = {mu_mm1}, Rho = {rho_mm1}\n")
        x_c = list(range(0, len(customers)))
        plt.bar(x_c, customers, color ='blue',width = 0.7)
        plt.xlabel("Iteration of simulator loop")
        plt.ylabel("Number of customers in the system")
        plt.title(f"Number of customers per iteration: Lambda = {lambda_mm1}, Mu = {mu_mm1}, Rho = {rho_mm1}")
        plt.show()

        #this block creates a bar graph of waiting time per customer serviced
        print(f"Creating Waiting Time bar graph with Lambda = {lambda_mm1}, Mu = {mu_mm1}, Rho = {rho_mm1}\n")
        x_w = list(range(0, len(waits)))
        plt.bar(x_w, waits, color ='blue',width = 0.7)
        plt.xlabel("Customers serviced")
        plt.ylabel("Waiting time in seconds")
        plt.title(f"Waiting time per customer serviced: Lambda = {lambda_mm1}, Mu = {mu_mm1}, Rho = {rho_mm1}")
        plt.show()
        
    return waits, customers

# Main function
if __name__ == "__main__":

    #S'''
    # 1st Case: Lambda = 1, Mu = 2, Rho = 0.5
    print("\n1st Case: Lambda = 1, Mu = 2, Rho = 0.5")
    wait_times, num_customers = simulatorMM1(lambda_mm1=1, mu_mm1=2, show_plots = True)
    plotCDF(wait_times, num_customers)
    print("--------------------------------------------------------\n")
    #'''

    #'''
    # 2nd Case: Lambda = 2, Mu = 4, Rho = 0.5
    print("2nd Case: Lambda = 2, Mu = 4, Rho = 0.5")
    wait_times, num_customers = simulatorMM1(lambda_mm1=2, mu_mm1=4, show_plots = True)
    plotCDF(wait_times, num_customers)
    print("--------------------------------------------------------\n")
    #'''

    #'''
    # 3rd Case: Lamda = 4, Mu = 2, Rho = 2
    print("3rd Case: Lamda = 4, Mu = 2, Rho = 2")
    wait_times, num_customers = simulatorMM1(lambda_mm1=4, mu_mm1=2, show_plots = True)
    plotCDF(wait_times, num_customers)
    print("--------------------------------------------------------\n")
    #'''