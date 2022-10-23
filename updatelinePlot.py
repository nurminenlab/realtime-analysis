
import random 
import numpy as np
import time
import matplotlib.pyplot as plt

#initialise
x = np.linspace(0, 10, 100)
y = np.linspace(20, 30, 100)
plt.ion()

figure, ax = plt.subplots(figsize=(10, 8))
line1, = ax.plot(x, y)

def updatePlot():
	new_y = np.linspace(20, 40, 100)
	
	#value update
	line1.set_xdata(x)
	line1.set_ydata(new_y)

	figure.canvas.draw()

	figure.canvas.flush_events()
	time.sleep(0.1)

while True:
	
    user_input = input("Enter 'u' to update plot or 'q' to quit: ")
    if user_input == "q":
        break
    if user_input =="u":
        updatePlot()

