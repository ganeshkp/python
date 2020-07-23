import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(12, 8))
x_array = np.random.randn(6, 10)
y_array = np.random.randn(6, 10)

i = 0
for row in axes:
    for ax in row:
        x = x_array[i]
        y = y_array[i]
        ax.scatter(x, y)
        ax.set_title("Plot " + str(i))
        i += 1
plt.tight_layout()
plt.show()