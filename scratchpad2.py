# importing library
import matplotlib.pyplot as plt
import numpy as np
 
# Data for plotting
x = np.arange(0.0, 2.0, 0.01)
y = 1 + np.sin(2 * np.pi * x)
channelDict = {'A-000': [9864], 'A-001': [8804, 9382, 13681], 'A-002': [13857], 'A-003': [3970, 8618, 10668, 11306, 12353, 14243, 14475, 15108]} 
# Creating 6 subplots and unpacking the output array immediately
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
ax1.plot(x, y, color="orange")
ax2.plot(x, y, color="green")
ax3.plot(x, y, color="blue")
ax4.plot(x, y, color="magenta")

print(y)
plt.show()
