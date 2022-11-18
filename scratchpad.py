import numpy as np
import matplotlib.pyplot as plt
# if using a Jupyter notebook, include:


x = np.linspace(0,5.5,10)
y = 10*np.exp(-x)
xerr = np.random.random_sample(10)
yerr = np.random.random_sample(10)


fig, ax = plt.subplots()


ax.errorbar(x, y,
            xerr=xerr,
            yerr=yerr,
            fmt='-o')


ax.set_xlabel('x-axis')
ax.set_ylabel('y-axis')
ax.set_title('Line plot with error bars')


plt.show()