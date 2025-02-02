#probability-based approach
import pandas as pd
import numpy as np
from collections import Counter

# Load data from CSV
data = pd.read_csv("em.csv")

# Reverse the data
data = data.iloc[::-1].reset_index(drop=True)

# Extract numbers
main_numbers = data.iloc[:, 1:6].values.flatten()
lucky_stars = data.iloc[:, 6:8].values.flatten()

# Compute probability distributions
main_counts = Counter(main_numbers)
lucky_counts = Counter(lucky_stars)

def weighted_random_selection(counter, num_choices, value_range):
    total = sum(counter.values())
    probabilities = {k: v / total for k, v in counter.items()}
    numbers = list(probabilities.keys())
    weights = list(probabilities.values())
    
    selected = np.random.choice(numbers, size=num_choices, replace=False, p=weights)
    return [int(max(value_range[0], min(value_range[1], num))) for num in selected]

# Predict next numbers using probability approach
predicted_main = weighted_random_selection(main_counts, 5, (1, 50))
predicted_lucky = weighted_random_selection(lucky_counts, 2, (1, 12))

print("Predicted main numbers:", [int(num) for num in predicted_main])
print("Predicted lucky star numbers:", [int(num) for num in predicted_lucky])