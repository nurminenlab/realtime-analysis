import matplotlib.pyplot as plt
fig, axes = plt.subplots(1,1,figsize=(10, 10))
manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
plt.show()
