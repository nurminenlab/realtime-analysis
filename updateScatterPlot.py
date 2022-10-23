import random 
import numpy as np
import time
import matplotlib.pyplot as plt
'''fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
fig.suptitle('SPIKE Data for channels ')
ax1.scatter([0],[0])
ax2.scatter([0],[0])
ax3.scatter([0],[0])
ax4.scatter([0],[0])




plt.show()'''

plt.ion()
fig, ax = plt.subplots()
x, y = [],[]
sc = ax.scatter(x,y)
plt.xlim(0,10)
plt.ylim(0,10)

plt.draw()
for i in range(1000):
    x.append(np.random.rand(1)*10)
    y.append(np.random.rand(1)*10)
    sc.set_offsets(np.c_[x,y])
    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(0.1)

