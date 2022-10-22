import numpy as np
import matplotlib.pyplot as plt

#baoab n par lennard jones potencial 2d

def potencial(pos):
    forca = np.zeros((npar, 2))
    forca[:, 0] = -4*alfa*(pos[:,0]**3) + 2*beta*pos[:,0]
    forca[:, 1] = -4*alfa*(pos[:,1]**3) + 2*beta*pos[:,1]
    return forca

def lennardjones2d(pos):
    x = pos[:, 0]

    y = pos[: ,1]

    ff = np.zeros((npar, 2))

    for i in range(npar):
        for j in range(i + 1, npar):
            dx = x[i] - x[j]

            dy = y[i] - y[j]
            
            r = np.sqrt(dx**2 + dy**2)

            if r < rcorte:
                a = 48*e*(((sigma/r)**14) - ((sigma/r)**8)/2 )/(sigma**2)
                #FX
                ff[i,0] += a*dx
                ff[j,0] -= a*dx
                #FY
                ff[i,1] += a*dy
                ff[j,1] -= a*dy
    return ff

alfa = (
0.25
)

beta = (
1
)

gaminha = (
10
)

sigma = (
0.5
)

dt = (
0.01
)

tmax = (
10
)

m = (
1
)

kb = (
1
)

temp = (
1
)

npar = (
12
)

rmax = (
4
)

rcorte = (
60
)

e = (
1
)

xini = 0

#fim das alteráveis

c1 = np.exp(-gaminha*dt)

c2  = (np.sqrt(1 - np.exp(-2*gaminha*dt)))*(np.sqrt(m*kb*temp))

npassos = int(np.round(tmax/dt))

aleatorios = np.random.normal(size = (npassos, npar, 2)) * c2

xy = np.zeros((npassos + 1, npar, 2))

xy[0] = (np.random.rand(npar, 2) - 0.5) * 2 * rmax

pxy = np.zeros((npassos + 1, npar, 2))

tempos = np.arange(0, tmax + dt, dt)

for i in range(0, npassos):

    #BAOAB
    #B
    pxytemp = pxy[i] + dt * (potencial(xy[i]) + lennardjones2d(xy[i]))/2
    #A
    xytemp = xy[i] + dt*pxytemp/(2*m)
    #O
    pxylinha = c1*pxytemp + aleatorios[i]
    #A
    xy[i+1] = xytemp + dt*pxylinha/(2*m)
    #B
    pxy[i+1] = pxylinha + dt * (potencial(xy[i+1]) + lennardjones2d(xy[i+1]))/2

for i in range(0, npassos):
    plt.cla()
    plt.xlim(-5, 5)
    plt.ylim(-5, 5)
    plt.scatter(xy[i, :, 0], xy[i, :, 1], alpha = 0.2, color = "green")
    plt.pause(0.0001)
plt.show(block = False)