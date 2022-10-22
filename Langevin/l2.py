import numpy as np
import matplotlib.pyplot as plt

#poço duplo baoab potencial 1 particula 1d

def potencial(x):
    forca = -4*alfa*(x**3) + 2*beta*x
    return forca

alfa = 0.25

beta = 1

gaminha = 10

dt = 0.0001

tmax = 100

xini = 0

m = 1

kb = 1

temp = 1

#fim das alteráveis

c1 = np.exp(-gaminha*dt)

c2  = (np.sqrt(1 - np.exp(-2*gaminha*dt)))*(np.sqrt(m*kb*temp))

npassos = int(np.round(tmax/dt))

aleatorios = np.random.normal(size = npassos) * c2

xx = np.zeros(npassos + 1)

pp = np.zeros(npassos + 1)

xx[0] = xini

tempos = np.arange(0, tmax + dt, dt)

for i in range(0, npassos):
    #B
    ptemp = pp[i] + dt*potencial(xx[i])/2
    #A
    xtemp = xx[i] + dt*ptemp/(2*m)
    #O
    plinha = c1*ptemp + aleatorios[i]
    #A
    xx[i+1] = xtemp + dt*plinha/(2*m)
    #B
    pp[i+1] = plinha + dt*potencial(xx[i+1])/2

plt.scatter(tempos, xx, s = 0.5)

plt.show()