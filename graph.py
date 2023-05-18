import matplotlib.pyplot as plt

minimax_nodes = [100, 200, 400, 800, 1600, 3200]
alpha_beta_nodes = [50, 70, 90, 110, 130, 150]

depth = [1, 2, 3, 4, 5, 6]

# Plotting the graph
plt.plot(depth, minimax_nodes, label='Minimax')
plt.plot(depth, alpha_beta_nodes, label='Alpha-Beta')
plt.xlabel('Depth')
plt.ylabel('Number of Nodes Evaluated')
plt.title('Performance Comparison: Minimax vs Alpha-Beta')
plt.legend()
plt.show()