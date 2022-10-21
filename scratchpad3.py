import datetime
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
t = []
x = []
line, = ax.plot_date(t,x, ls="-")

def update():
    now = datetime.datetime.now()
    if np.random.rand() > 0.9:
        t.append(now)
        x.append(np.random.randn())
        line.set_data(t,x)
        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw_idle()
        message = "new data drawn"
    else:
        message = "no new data"
    print(now.time(), message)


timer = fig.canvas.new_timer(interval=200)
timer.add_callback(update)
timer.start()

plt.show()