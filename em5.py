import pandas as pd
import numpy as np
from collections import Counter
from sklearn.neighbors import KNeighborsClassifier

# Load data from CSV
data = pd.read_csv("em.csv")

# Reverse the data
data = data.iloc[::-1].reset_index(drop=True)

# Extract numbers
main_numbers = data.iloc[:, 1:6].values
lucky_stars = data.iloc[:, 6:8].values

# Prepare training data
X = np.arange(len(main_numbers)).reshape(-1, 1)
y_main = main_numbers
y_lucky = lucky_stars

# Train KNN model
knn_main = KNeighborsClassifier(n_neighbors=3, weights='distance')
knn_lucky = KNeighborsClassifier(n_neighbors=3, weights='distance')
knn_main.fit(X, y_main)
knn_lucky.fit(X, y_lucky)

# Predict next numbers
next_index = np.array([[len(main_numbers)]])
predicted_main = knn_main.predict(next_index)[0]
predicted_lucky = knn_lucky.predict(next_index)[0]

print("Predicted main numbers:", predicted_main.tolist())
print("Predicted lucky star numbers:", predicted_lucky.tolist())
