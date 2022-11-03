
import random 
import numpy as np
import time
import matplotlib.pyplot as plt

#initialise
x = np.array([])
y = np.array([])
plt.ion()

figure, ax = plt.subplots(figsize=(10, 8))
line1, = ax.plot(x, y,'o')
plt.setp(ax, xlim=(0,6), ylim=(0,50))
def updatePlot(x,y):
	
	#value update
	line1.set_xdata(x)
	line1.set_ydata(y)

	figure.canvas.draw()
	figure.canvas.flush_events()
	time.sleep(0.1)

while True:
	
    user_input = input("Enter 'u' to update plot or 'q' to quit: ")
    if user_input == "q":
        break
    if user_input =="u":
        updatePlot(1,10)
        #time.sleep(0.5)
        updatePlot(2,20)
        #time.sleep(0.5)
        updatePlot(3,30)
        #time.sleep(0.5)
        updatePlot(4,40)


