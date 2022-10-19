import random
from itertools import count
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

# plt.scatter(x_vals,[ None if x in x_vals else 1 for x in range(len(x_vals)) ])

index = count()

def animate(i):
    x_vals.append(next(index))
    y_vals.append(random.randint(0,5))
    plt.plot(x_vals,y_vals)

# gcf -> Get the current figure
anim = FuncAnimation(plt.gcf(), animate,interval=1000 )
plt.tight_layout()
plt.show()














channelDict = {'A-000': [609], 'A-001': [5290], 'A-002': [9371], 'A-003': [6029, 7665, 8055, 8465, 10763, 14605, 15243, 18067, 18382]}


print([ None if x in channelDict['A-000'] else 1 for x in range(len(channelDict['A-000'])) ])

#timeStampArray = [0, 3014, 24055, 37993, 47727, 54492, 123708, 134071, 138909]

