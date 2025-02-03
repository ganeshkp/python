#Use Bayesian Inference
import pandas as pd
import numpy as np
from collections import Counter

# Load data from CSV
data = pd.read_csv("sfl.csv")

# Reverse the data
data = data.iloc[::-1].reset_index(drop=True)

# Extract numbers
main_numbers = data.iloc[:, 1:6].values.flatten()
lucky_stars = data.iloc[:, 6:7].values.flatten()

# Count occurrences
main_counts = Counter(main_numbers)
lucky_counts = Counter(lucky_stars)

def bayesian_prediction(counter, num_choices, value_range):
    total = sum(counter.values())
    probabilities = {k: (v + 1) / (total + len(counter)) for k, v in counter.items()}  # Laplace smoothing
    
    numbers = list(probabilities.keys())
    weights = list(probabilities.values())
    
    selected = np.random.choice(numbers, size=num_choices, replace=False, p=weights)
    return [int(max(value_range[0], min(value_range[1], num))) for num in selected]

# Predict using Bayesian Inference
predicted_main = bayesian_prediction(main_counts, 5, (1, 48))
predicted_lucky = bayesian_prediction(lucky_counts, 1, (1, 11))

print("Predicted main numbers:", [int(num) for num in predicted_main])
print("Predicted lucky star numbers:", [int(num) for num in predicted_lucky])
