#Markov chains approach
import pandas as pd
import numpy as np
from collections import defaultdict

# Load data from CSV
data = pd.read_csv("sfl.csv")

# Reverse the data
data = data.iloc[::-1].reset_index(drop=True)

# Extract numbers
main_numbers = data.iloc[:, 1:6].values
lucky_stars = data.iloc[:, 6:7].values

# Function to build Markov transition matrix
def build_transition_matrix(sequences, max_value):
    transition_matrix = defaultdict(lambda: np.zeros(max_value + 1))
    
    for sequence in sequences:
        for i in range(len(sequence) - 1):
            transition_matrix[sequence[i]][sequence[i + 1]] += 1
    
    for key in transition_matrix:
        total = sum(transition_matrix[key])
        if total > 0:
            transition_matrix[key] /= total  # Normalize to probabilities
    
    return transition_matrix

# Build Markov chains
main_transition_matrix = build_transition_matrix(main_numbers, 48)
lucky_transition_matrix = build_transition_matrix(lucky_stars, 11)

# Function to predict next numbers using Markov Chain
def predict_markov(transition_matrix, num_choices, max_value):
    predictions = []
    start = np.random.randint(1, max_value + 1)  # Random start number
    
    for _ in range(num_choices):
        if start in transition_matrix:
            probabilities = transition_matrix[start]
            next_number = np.random.choice(range(max_value + 1), p=probabilities)
        else:
            next_number = np.random.randint(1, max_value + 1)
        
        predictions.append(next_number)
        start = next_number  # Move to next state
    
    return predictions

# Predict numbers
predicted_main = predict_markov(main_transition_matrix, 5, 47)
predicted_lucky = predict_markov(lucky_transition_matrix, 1, 10)

print("Predicted main numbers:", [int(num) for num in predicted_main])
print("Predicted lucky star numbers:", [int(num) for num in predicted_lucky])