import matplotlib.pyplot as plt

# Subplots are organized in a Rows x Cols Grid
# Tot and Cols are known

Tot = 7
Cols = 2

x=[1,2,3,4,5]
y=[1,4,9,16,25]

# Compute Rows required

Rows = Tot // Cols
Rows += Tot % Cols

# Create a Position index

Position = range(1,Tot + 1)

# Create main figure

fig = plt.figure(1)
for k in range(Tot):

  # add every single subplot to the figure with a for loop

  ax = fig.add_subplot(Rows,Cols,Position[k])
  ax.plot(x,y)      # Or whatever you want in the subplot

plt.show()