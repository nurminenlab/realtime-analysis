import random 
import numpy as np
import time
import matplotlib.pyplot as plt

plt.ion()
fig, ax = plt.subplots()
x, y = [],[]
sc = ax.scatter(x,y)
plt.xlim(0,20)
plt.ylim(0,20)

plt.draw()

def updatePlot():
        x.append(np.random.rand(1)*15)
        y.append(np.random.rand(1)*15)
        sc.set_offsets(np.c_[x,y])
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.1)

while True:
    user_input = input("Enter 'u' to update plot or 'q' to quit: ")
    if user_input == "q":
        break
    if user_input =="u":
        updatePlot()

