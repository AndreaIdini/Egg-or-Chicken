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

