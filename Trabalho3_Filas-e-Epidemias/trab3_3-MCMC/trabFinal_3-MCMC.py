import numpy as np
import matplotlib.pyplot as plt


# Load the trace from the file produced by the modified MM1 code
def load_trace(file_path):
    trace = []
    with open(file_path, "r") as file:
        for line in file:
            num_customers = int(line.strip())
            #print(num_customers)
            trace.append(num_customers)
    return trace


def likelihood(trace, rho):
    # Implement the likelihood function to calculate the likelihood of the observed data given trace and rho.
    # For an M/M/1 queue, the likelihood is the product of the probabilities of each observed trace value.
    likelihood = 1.0
    for num_customers in trace:
        # Probability of observing 'num_customers' customers in the system at each step
        prob_num_customers = (1 - rho) * (rho ** num_customers)
        likelihood *= prob_num_customers
    return likelihood


def prior(rho):
    # Implement the prior function to calculate the prior probability of rho.
    # For a uniform prior, return 1 within the range [0, 1] and 0 outside this range.
    if (0 <= rho <= 1):
        return 1.0
    return 0.0


def proposal(current_rho):
    # Implement the proposal function to generate a new proposal for rho.
    # For example, you can use a normal distribution centered at the current_rho.
    # Return the proposed rho value.
    proposal_sigma = 0.01  # You can adjust the proposal distribution variance

    return np.random.normal(current_rho, proposal_sigma)


def acceptance_ratio(trace, current_rho, proposed_rho):
    # Calculate the acceptance ratio for the Metropolis-Hastings algorithm.
    current_likelihood = likelihood(trace, current_rho)
    proposed_likelihood = likelihood(trace, proposed_rho)

    current_prior = prior(current_rho)
    proposed_prior = prior(proposed_rho)

    if (current_likelihood == 0) or (current_prior == 0):
        acceptance = 0
    else:
        acceptance = (proposed_likelihood * proposed_prior)/(current_likelihood * current_prior)

    return min(1, acceptance)


def metropolis_hastings(trace, iterations):
    rho_values = []
    current_rho = np.random.uniform(0, 1)  # Initialize rho randomly within [0, 1]
    #current_rho = 0.2
    #current_rho = 0.9
    #current_rho = 0.5

    for _ in range(iterations):
        # Propose a new rho using the proposal function
        proposed_rho = proposal(current_rho)

        # Calculate the acceptance ratio
        accept_prob = acceptance_ratio(trace, current_rho, proposed_rho)

        # Accept or reject the proposed rho based on the acceptance ratio
        if np.random.rand() < accept_prob:
            current_rho = proposed_rho

        rho_values.append(current_rho)

    return rho_values


# Load the observed data (trace) from the input file
trace = load_trace("mm1_trace.txt")

# Number of MCMC iterations
iterations = 10000

# Perform MCMC to estimate rho
rho_samples = metropolis_hastings(trace, iterations)


#-----------------------------------------------------------------------------------------

# Generate a histogram to show the estimated distribution of rho
plt.hist(rho_samples, bins=30, density=True, alpha=0.6)
plt.xlabel("Utilization Factor (ρ)")
plt.ylabel("Density")
plt.title("Estimated Distribution of Utilization Factor (ρ)")
plt.show()

# Calculate and print the mean and variance of the estimated rho values
mean_rho = np.mean(rho_samples)
var_rho = np.var(rho_samples)
estimated_rho = rho_samples[-1]
print(f"Estimated Value of ρ: {estimated_rho:.4f}")
print(f"Estimated Mean of ρ: {mean_rho:.4f}")
print(f"Estimated Variance of ρ: {var_rho:.4f}")


#-----------------------------------------------------------------------------------------

## Case a) m = 100, y = ∑vi = 25
m_a = 100
y_a = 25
v_a = np.ones(m_a) * (y_a // m_a)  # Create an array with equal values y/m
rho_samples_a = metropolis_hastings(v_a, iterations=10000)

# Generate a histogram to show the estimated distribution of rho for case a)
plt.hist(rho_samples_a, bins=30, density=True, alpha=0.6)
plt.xlabel("Utilization Factor (ρ)")
plt.ylabel("Density")
plt.title("Estimated Distribution of Utilization Factor (ρ) - Case a")
plt.show()


## Case b) m = 100, y = ∑vi = 100
m_b = 100
y_b = 100
v_b = np.ones(m_b) * (y_b // m_b)  # Create an array with equal values y/m
rho_samples_b = metropolis_hastings(v_b, iterations=10000)

# Generate a histogram to show the estimated distribution of rho for case b)
plt.hist(rho_samples_b, bins=30, density=True, alpha=0.6)
plt.xlabel("Utilization Factor (ρ)")
plt.ylabel("Density")
plt.title("Estimated Distribution of Utilization Factor (ρ) - Case b")
plt.show()


#-----------------------------------------------------------------------------------------

## c) ρ = 4/5, gerar trace via simulação, obter m e y, e extrair amostras de ρ usando MCMC
m_c = 100
rho_c = 4/5

trace_c = []
np.random.seed(42)
simultime = 0
n = 0
for _ in range(m_c):
    time_of_arrival_c = np.random.exponential(1 / (1 - rho_c))
    time_of_departure_c = np.random.exponential(1 / rho_c)

    if (n == 0 or time_of_arrival_c < time_of_departure_c):
        simultime += time_of_arrival_c
        n += 1
    else:
        simultime += time_of_departure_c
        n -= 1
    trace_c.append(n)

# Perform MCMC to estimate rho for case c
iterations = 10000
rho_samples_c = metropolis_hastings(trace_c, iterations)

# Generate a histogram to show the estimated distribution of rho for case c
plt.hist(rho_samples_c, bins=30, density=True, alpha=0.6)
plt.xlabel("Utilization Factor (ρ)")
plt.ylabel("Density")
plt.title("Estimated Distribution of Utilization Factor (ρ) - Case c")
plt.show()


## d) ρ = 1/2, gerar trace via simulação, obter m e y, e extrair amostras de ρ usando MCMC
m_d = 100
rho_d = 1/2

trace_d = []
np.random.seed(43)
simultime = 0
n = 0
for _ in range(m_d):
    time_of_arrival_d = np.random.exponential(1 / (1 - rho_d))
    time_of_departure_d = np.random.exponential(1 / rho_d)

    if (n == 0 or time_of_arrival_d < time_of_departure_d):
        simultime += time_of_arrival_d
        n += 1
    else:
        simultime += time_of_departure_d
        n -= 1
    trace_d.append(n)

# Perform MCMC to estimate rho for case d
rho_samples_d = metropolis_hastings(trace_d, iterations)

# Generate a histogram to show the estimated distribution of rho for case d
plt.hist(rho_samples_d, bins=30, density=True, alpha=0.6)
plt.xlabel("Utilization Factor (ρ)")
plt.ylabel("Density")
plt.title("Estimated Distribution of Utilization Factor (ρ) - Case d")
plt.show()
