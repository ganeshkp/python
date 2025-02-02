#Combination Analysis Approach
import pandas as pd
from itertools import combinations
from collections import Counter

# Load the dataset
df = pd.read_csv("em.csv")

# Combine all ball numbers into a single list of tuples (each draw is a tuple)
ball_columns = ["Ball 1", "Ball 2", "Ball 3", "Ball 4", "Ball 5"]
all_draws = df[ball_columns].apply(lambda row: tuple(sorted(row)), axis=1).tolist()

# Generate all possible pairs, triplets, etc., and count their frequency
combination_size = 2  # You can change this to 3 for triplets, etc.
combination_counter = Counter()

for draw in all_draws:
    for combo in combinations(draw, combination_size):
        combination_counter[combo] += 1

# Get the most frequent combinations
most_frequent_combinations = combination_counter.most_common(10)

# Print the most frequent combinations
# print("Most Frequent Combinations:")
# for combo, frequency in most_frequent_combinations:
#     print(f"Combination: {combo}, Frequency: {frequency}")

# Predict the next set of numbers based on the most frequent combinations
# Step 1: Extract the most frequent numbers from the top combinations
frequent_numbers = []
for combo, _ in most_frequent_combinations:
    frequent_numbers.extend(combo)

# Step 2: Count the frequency of each number in the frequent combinations
number_counter = Counter(frequent_numbers)

# Step 3: Select the top 5 most frequent numbers as the predicted balls
predicted_balls = [num for num, _ in number_counter.most_common(5)]

# Step 4: Repeat the process for Lucky Stars
lucky_star_columns = ["Lucky Star 1", "Lucky Star 2"]
all_lucky_stars = df[lucky_star_columns].apply(lambda row: tuple(sorted(row)), axis=1).tolist()

lucky_star_counter = Counter()
for stars in all_lucky_stars:
    for combo in combinations(stars, combination_size):
        lucky_star_counter[combo] += 1

# Get the most frequent lucky star combinations
most_frequent_lucky_stars = lucky_star_counter.most_common(10)

# Extract the most frequent lucky star numbers
frequent_lucky_stars = []
for combo, _ in most_frequent_lucky_stars:
    frequent_lucky_stars.extend(combo)

# Count the frequency of each lucky star number
lucky_star_number_counter = Counter(frequent_lucky_stars)

# Select the top 2 most frequent lucky star numbers
predicted_lucky_stars = [num for num, _ in lucky_star_number_counter.most_common(2)]

# Print the predicted numbers
print("Predicted Balls (1-50):", sorted(predicted_balls))
print("Predicted Lucky Stars (1-12):", sorted(predicted_lucky_stars))