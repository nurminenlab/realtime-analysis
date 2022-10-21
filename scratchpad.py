from matplotlib import pyplot as plt
from IPython.display import clear_output
import numpy as np
from matplotlib.animation import FuncAnimation
import time


def animate(x):
    y = np.random.random([10,1])
    plt.cla()
    plt.plot(y)
    time.sleep(1)

anim = FuncAnimation(plt.gcf(), animate )


plt.show()