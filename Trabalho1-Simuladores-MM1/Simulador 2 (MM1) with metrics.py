# M/M/1
# Entrada dada por um processo Poison
# Servico dada por uma distribuicao exponencial

import numpy as np
import math

# Sets the random number generator seed to 1
np.random.seed(1)

# Initializes the number of customers in the system and the simulation time 
n = 0
simultime = 0

# These lines define constants for the events of arrival and departure
ARRIVAL = 1
DEPARTURE = 2

# Variables which armazenate the times of arrival and departure
tax_arrival = 1         # arrival time
tax_departure = 0.5     # service time

# The eventqueue is a list that stores information about the future events in the simulation. Each element of the list represents an event,
# with a tuple containing the time at which the event occurs, and the type of the event (either an arrival or a departure).
eventqueue = [(np.random.exponential(1), ARRIVAL)]
# In this simulation, the head of the event queue (the next event to occur) is always stored in the first element of the list

# This array stores the time of arrival of each customer. It will be acessed during a arrival event.
arrivals = []

# This array stores the waiting times of each customer. It will be acessed during a departure event.
# Values consist of time_of_service - time_of_arrival of each customer
waits = []

# Array stores the number of customers each iteration
customers = []

# This variables receives the total number of elements in the event queue (being 1 at the start)
nelements = 1

# This function calculates useful metrics of chosen list
def metrics(list):
    return len(list), np.mean(list), np.std(list), 1.96

# This function calculates confidence interval
def confidenceInterval(samples, mean, std, precision):
    minCI = mean - (precision * (std / math.sqrt(samples) ))
    maxCI = mean + (precision * (std / math.sqrt(samples) ))
    return minCI, maxCI

MAXITERATION = 10000
# Starts the main simulation loop, which iterates MAXITERATION times or until there are no more events in the queue.
for i in range(MAXITERATION):

    # This block checks if there are any more events in the queue. If there are no events, the simulation stops.
    if (nelements == 0):
        print("The queue was emptied. End of simulation.")
        break

    # These line picks the first event in the queue and store its time and type.
    # current_event_time - stores time of the event
    # current_event_type - stores type of the event
    current_event_time, current_event_type = eventqueue[0]

    # Updates the simulation time to the time of the current event.
    simultime = current_event_time

    # This line removes the first event from the queue (total of elements decreases in 1).
    nelements -= 1

    # If there are more events in the queue, this block gets the next event in the queue
    if (nelements >= 1):
        eventqueue[0] = (eventqueue[1][0], eventqueue[1][1])
        eventqueue.pop(1)
        #print(len(eventqueue))
        #print(nelements)


    # This block checks if the current event is an arrival.
    if (current_event_type == ARRIVAL):

        print(f"[{simultime:08.4f}] {'arrival':>10}, {n} => {n + 1}")     # This block prints out a message indicating the arrival,
        n += 1                                                          # updates the number of customers in the system
        customers.append(n)                                                 # appends current number of customers
        arrivals.append(simultime)                                          # appends arrival of current customer
        time_next_arrival = np.random.exponential(tax_arrival)          # generates the time of the next arrival, which is exponentially distributed by 'tax_arrival'

        # if there are no more events in the queue.
        if (nelements == 0):
            # Generates the service time for the new customer, which is exponentially distributed by tax_departure
            time_next_service = np.random.exponential(tax_departure)

            # Checks if the next arrival occurs before the service for the new customer finishes
            if (time_next_arrival < time_next_service):

                # If the next arrival occurs before the next departure, it schedules the departure of the old customer after the arrival of the new one
                eventqueue.append((simultime + time_next_service, DEPARTURE))
                eventqueue.append((simultime + time_next_arrival, ARRIVAL))

                nelements += 2

            else:
                # % Otherwise, it schedules the arrival of the new costumer after the departure of the old one
                eventqueue.append((simultime + time_next_arrival, ARRIVAL))
                eventqueue.append((simultime + time_next_service, DEPARTURE))

                nelements += 2

        # If there are events in the queue, add the next arrival to the queue in the appropriate position
        elif (eventqueue[0][0] > simultime + time_next_arrival):
            eventqueue.insert(0, (simultime + time_next_arrival, ARRIVAL))

            nelements += 1

        # If the next arrival occurs before the next event in the queue, add it to the end of the queue
        else:
            eventqueue.append((simultime + time_next_arrival, ARRIVAL))

            nelements += 1

    # This block treats the event as a departure.
    else:
        print(f"[{simultime:08.4f}] {'departure':>10}, {n} => {n - 1}")
        n = n-1
        customers.append(n)                                                 # appends current number of customers
        waits.append(simultime-arrivals[0])                                 # appends waiting time of departing customer
        arrivals.pop(0)

        # If there are still elements in the queue
        if (n > 0):

            # Generates next service time for the next customer, which is exponentially distributed with by 'tax_departure'
            time_next_service = np.random.exponential(tax_departure)

            # If the next event in the queue is an arrival event and occurs before the next service time,
            # we schedule the departure event immediately after the arrival event
            if (eventqueue[0][0] < simultime + time_next_service):
                eventqueue.append((simultime + time_next_service, DEPARTURE))

                nelements += 1

            # Otherwise, we schedule the departure event at the beginning of the queue
            else:
                eventqueue.insert(0, (simultime + time_next_service, DEPARTURE))

                nelements += 1
     
    # This block warns end of simulation by reaching max number of iterations
    if(i==MAXITERATION-1): print(f"\nMax iteration number ({MAXITERATION}) reached. End of simulation\n")

# this block gets the number of customeres serviced, average waiting time and standard deviation of waiting time
samples_w, mean_w, std_w, precision_w = metrics(waits)

# this block prints customers serviced and average waiting time
print(f"Number of customers serviced (samples): {samples_w}")
print(f"Average Waiting Time: {mean_w:08.4f}s")

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
