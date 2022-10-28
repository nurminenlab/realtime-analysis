import random 
import numpy as np
import time
import matplotlib.pyplot as plt

plt.ion()

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

axes = [ax1,ax2,ax3,ax4] 
sc = []
for axis,i in zip(axes,range(len(axes))):
    sc.append(axis.scatter([],[],marker='|'))
    plt.setp(axis, xlim=(0,35), ylim=(0,35))
x, y = [],[]
x1,y1 =[],[]


plt.draw()
def updatePlot():
        x.append(np.random.rand(1)*15)
        y.append(np.random.rand(1)*15)
        sc[0].set_offsets(np.c_[x,y])
        

        x1.append(np.random.rand(1)*15)
        y1.append(np.random.rand(1)*15)
        sc[1].set_offsets(np.c_[x1,y1])
        
        x.append(np.random.rand(1)*15)
        y.append(np.random.rand(1)*15)
        sc[2].set_offsets(np.c_[x,y])
        

        x1.append(np.random.rand(1)*18)
        y1.append(np.random.rand(1)*13)
        sc[3].set_offsets(np.c_[x,y])

        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.1)


while True:
    user_input = input("Enter 'u' to update plot or 'q' to quit: ")
    if user_input == "q":
        break
    if user_input =="u":
        updatePlot()

'''arr = []
def addXY(arr,x,y):
    print()
    arr.extend([(x,y)])

addXY(arr,34,67)
addXY(arr,23,89)
print(arr[0])'''














