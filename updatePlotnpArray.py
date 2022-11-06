
import random 
import numpy as np
import time
import matplotlib.pyplot as plt

#initialise
x = np.array([])
y = np.array([])
plt.ion()

figure, ax = plt.subplots(figsize=(10, 8))
line1, = ax.plot(x, y)
plt.setp(ax, xlim=(0,6), ylim=(0,50))


def updatePlot(x,yArr,y):	
	#value update
    line1.set_xdata(x)
    y = np.append(y,yArr)
    line1.set_ydata(y)
    figure.canvas.draw()
    figure.canvas.flush_events()
    time.sleep(0.1)

while True:
	
    user_input = input("Enter 'u' to update plot or 'q' to quit: ")
    if user_input == "q":
        break
    if user_input =="u":
        
        updatePlot(np.array([1,2,3,4]),np.array([10,30,20,40]),y)
        #time.sleep(0.5)
    if user_input =="v":
        
        updatePlot(np.array([1+1,2+1,3+1,4+1]),np.array([10+10,30+10,20+10,40+10]),y)
    