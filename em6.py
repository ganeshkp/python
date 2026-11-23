#MONTE CARLO
import pandas as pd
import numpy as np
from collections import Counter

# Load data from CSV
data = pd.read_csv("em.csv")

# Reverse the data (latest first)
data = data.iloc[::-1].reset_index(drop=True)

# Extract numbers
main_numbers = data.iloc[:, 1:6].values.flatten()
lucky_stars = data.iloc[:, 6:8].values.flatten()

# Function to calculate weighted probabilities
def weighted_probabilities(numbers, weight_decay=0.9):
    counts = Counter()
    total_weight = 0
    weight = 1
    
    for num in reversed(numbers):  # More recent draws have higher weight
        counts[num] += weight
        total_weight += weight
        weight *= weight_decay  # Apply decay to older draws
    
    probabilities = {num: count / total_weight for num, count in counts.items()}
    return probabilities

# Get probability distributions
main_probs = weighted_probabilities(main_numbers)
lucky_probs = weighted_probabilities(lucky_stars, weight_decay=0.85)

# Monte Carlo Simulation to generate likely numbers
def predict_numbers(probabilities, num_choices, max_value):
    numbers = list(probabilities.keys())
    probs = list(probabilities.values())
    return sorted(np.random.choice(numbers, num_choices, replace=False, p=probs))

# Predict next set of numbers
predicted_main = predict_numbers(main_probs, 5, 50)
predicted_lucky = predict_numbers(lucky_probs, 2, 12)

print("Predicted main numbers:", predicted_main)
print("Predicted lucky star numbers:", predicted_lucky)
