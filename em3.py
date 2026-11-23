#Use Bayesian Inference
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

# Compute frequency of numbers
main_freq = Counter(main_numbers)
lucky_freq = Counter(lucky_stars)

# Convert frequencies to probabilities
main_probs = {num: count / len(main_numbers) for num, count in main_freq.items()}
lucky_probs = {num: count / len(lucky_stars) for num, count in lucky_freq.items()}

# Predict next numbers based on highest probabilities
predicted_main = sorted(main_probs, key=main_probs.get, reverse=True)[:5]
predicted_lucky = sorted(lucky_probs, key=lucky_probs.get, reverse=True)[:2]

print("Predicted main numbers:", predicted_main)
print("Predicted lucky star numbers:", predicted_lucky)
