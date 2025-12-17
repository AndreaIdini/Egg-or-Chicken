import numpy as np

# rate in %, years as int or array-like
def calculate_compound_interest(principal, rate, time):
    # Ensure inputs are numpy arrays so math operations broadcast
    time = np.asarray(time)
    return principal * ((1 + rate/100) ** time)

def calculate_breakeven_year(target_amount, principal, rate):
    return np.log(target_amount / principal) / np.log(1 + rate/100)

# rate in %, time as int
def calculate_constant_investment(amount_rata, rate, time):
    wealth = [0]
    for t in range(1, time + 1):
        wealth.append( (wealth[-1] + amount_rata) * (1 + rate / 100) )
    return wealth

# Convert nominal annual rate to effective rate based on compounding frequency
def compounding_frequency_adjusted(nominal_rate, n_compounding):
    return 100 * ( (1 + nominal_rate/100)**(1/n_compounding) - 1)


def generate_deltas(n_steps, volatility, expected_return, seed=False):
    # normally distributed random number with a seed
    if seed: np.random.seed(int(n_steps/volatility/expected_return))
    rand = np.random.normal(size=(n_steps-1))
    
    deltaprice = expected_return/100. + volatility * rand
    return deltaprice

# Simulate Geometric Brownian Motion paths
# https://quant.stackexchange.com/questions/4589/how-to-simulate-stock-prices-with-a-geometric-brownian-motion
def generate_paths(n_steps, volatility, expected_return, start_val=1, seed=False):
    # normally distributed random number with a seed
    if seed: np.random.seed(int(n_steps/volatility/expected_return))
    rand = np.random.normal(size=(n_steps-1))
    # dt = 252 # Trading days in a year
    deltaprice = expected_return/100. + volatility * rand
    prices = np.zeros(n_steps)
    prices[0] = 1
    prices[1:] = np.cumprod(1 + deltaprice)

    return prices*start_val

# paths = []
# years = 1
# investment_volatility = 2
# investment_rate = compounding_frequency_adjusted(5, 12)
# initial_amount = 1000
# for i in range(3):
#     paths.append(generate_paths(12*years+1, investment_volatility/100, investment_rate, start_val=initial_amount))

# print(paths)
# # print the second element of each elements in paths
# for p in paths:
#     print(p[1])

# # #make histogram
# import matplotlib.pyplot as plt
# delta = 12000
# print(compounding_frequency_adjusted(5, delta))
# print(calculate_compound_interest(1000, 5, range(11)), calculate_compound_interest(1000, compounding_frequency_adjusted(5, delta), delta*10))
# plt.hist(generate_paths(100000, 0., 0.05), bins=30)
# # make array of cumulative sum
# deltaprice = generate_paths(10000, 0.02, 0.05/252)
# print(deltaprice)
# # plt.hist(deltaprice, bins=30)
# print(prices)
# plt.plot(generate_paths(100, 0.1, 5))

# # plt.title("Simulated GBM returns")
# plt.show()
