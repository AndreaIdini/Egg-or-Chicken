import numpy as np

# rate in %, years as int or array-like
def calculate_compound_interest(principal, rate, years):
    # Ensure inputs are numpy arrays so math operations broadcast
    years = np.asarray(years) 
    return principal * ((1 + rate/100) ** years)

def calculate_breakeven_year(target_amount, principal, rate):
    return np.log(target_amount / principal) / np.log(1 + rate/100)


print(10, calculate_compound_interest(1000, 5, 10))  # Example usage
print(20, calculate_compound_interest(1000, 5, 20))  # Example usage

print(calculate_compound_interest(1000, 5, range(21)))  # Example usage