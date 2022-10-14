import numpy as np
import matplotlib.pyplot as pp
val = 0. # this is the value where you want the data to appear on the y-axis.
ar = np.arange(10) # just as an example array
pp.plot(ar, np.zeros_like(ar) + val, 'x')
pp.show()