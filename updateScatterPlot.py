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
xyArr = [([],[]),([],[]),([],[]),([],[])]

plt.draw()
def updatePlot():
    for i,xy in zip(range(4),xyArr):
        xy[0].append(np.random.rand(1)*15)
        xy[1].append(np.random.rand(1)*15)
        sc[i].set_offsets(np.c_[xy[0],xy[1]])
        

        '''x1.append(np.random.rand(1)*15)
        y1.append(np.random.rand(1)*15)
        sc[1].set_offsets(np.c_[x1,y1])
        
        x.append(np.random.rand(1)*15)
        y.append(np.random.rand(1)*15)
        sc[2].set_offsets(np.c_[x,y])
        

        x1.append(np.random.rand(1)*18)
        y1.append(np.random.rand(1)*13)
        sc[3].set_offsets(np.c_[x,y])'''

        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.1)


while True:
    user_input = input("Enter 'u' to update plot or 'q' to quit: ")
    if user_input == "q":
        print(xyArr)
        break
    if user_input =="u":
        updatePlot()

'''arr = []

arr = [([1],[2]),([3],[4]),([5],[6])]
arr.append(([7],[8]))
for x in arr:
  print(x[0],x[1])

print(arr)
'''






'''import random 
import numpy as np
import time
import matplotlib.pyplot as plt

plt.ion()
fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
ax4 = fig.add_subplot(2,2,4)

x, y = [],[]
x1,y1 =[],[]

sc1 = ax1.scatter(x,y,marker='|')
plt.setp(ax1, xlim=(0,20), ylim=(0,20))

sc2 = ax2.scatter(x1,y1,marker='x')
plt.setp(ax2, xlim=(0,21), ylim=(0,25))

sc3 = ax3.scatter(x,y,c = 'purple')
plt.setp(ax3, xlim=(0,22), ylim=(0,30))

sc4 = ax4.scatter(x1,y1,c = 'black')
plt.setp(ax4, xlim=(0,23), ylim=(0,35))




plt.draw()
def updatePlot():
        x.append(np.random.rand(1)*15)
        y.append(np.random.rand(1)*15)
        sc1.set_offsets(np.c_[x,y])
        

        x1.append(np.random.rand(1)*15)
        y1.append(np.random.rand(1)*15)
        sc2.set_offsets(np.c_[x1,y1])
        
        x.append(np.random.rand(1)*15)
        y.append(np.random.rand(1)*15)
        sc3.set_offsets(np.c_[x,y])
        

        x1.append(np.random.rand(1)*18)
        y1.append(np.random.rand(1)*13)
        sc4.set_offsets(np.c_[x,y])

        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.1)


while True:
    user_input = input("Enter 'u' to update plot or 'q' to quit: ")
    if user_input == "q":
        break
    if user_input =="u":
        updatePlot()

'''