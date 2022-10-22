import numpy as np
import matplotlib.pyplot as plt

#poço duplo euler potencial

alfa = 2

beta = 1

dt = 0.001

tmax = 100

xini = 1

npassos = int(tmax/dt)

aleatorios = np.random.normal(size = npassos)

dw = np.sqrt(dt) * beta * aleatorios

xx = np.zeros(npassos + 1)

xx[0] = xini

tempos = np.arange(0, tmax + dt, dt)

for j in range(0, npassos):
    xx[j + 1] = xx[j] + dt*xx[j]*(alfa - xx[j]**2) + dw[j]

plt.plot(tempos, xx)

plt.show()