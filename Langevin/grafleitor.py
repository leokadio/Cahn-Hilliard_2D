import numpy as np
import matplotlib.pyplot as plt

tp = 0

Dt = 0.5

array = np.load(f"tp_{tp}&Dt_{Dt}.npy")

xx = array[0]

yy = array[1]

vx = array[2]

vy = array[3]

tt = array[4]

xx2 = xx**2

yy2 = yy**2

rr = xx2 + yy2

fig = plt.figure()

plt.suptitle(f"tmax = {tt[-1]}, tp = {tp}, Dt = {Dt}")

plt.subplot(131)

plt.title("x no tempo")

plt.scatter(tt, xx, color = "orange", alpha = 0.006, s = 0.05)

plt.subplot(132)

plt.title("y no tempo")

plt.scatter(tt, yy, color = "blue", alpha = 0.006, s = 0.05)

plt.subplot(133)

plt.title("raio no tempo")

plt.scatter(tt, rr, color = "green", alpha = 0.006, s = 0.05)

plt.savefig(f"tmax = {tt[-1]}, tp = {tp}, Dt = {Dt}.png", dpi = fig.dpi)

plt.show()
