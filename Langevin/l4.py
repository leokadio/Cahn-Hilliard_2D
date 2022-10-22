import numpy as np
import matplotlib.pyplot as plt
import os
import time

#baoab n par lennard jones potencial 2d
#region funcoes
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

def lennardjones2dpbc(pos):
    x = pos[:, 0]

    y = pos[: ,1]

    ff = np.zeros((npar, 2))

    for i in range(npar):
        for j in range(i + 1, npar):
            dx = x[i] - x[j] - np.rint((x[i] - x[j])/l)*l

            dy = y[i] - y[j] - np.rint((y[i] - y[j])/l)*l
            
            if dy > l/2:
                dy -= l
            elif dy < -l/2:
                dy += l

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

def pbcvoltas(pos, contador):
    for i in range(npar):
        while pos[i, 0] > l:
            pos[i,0]-=l
            contador[i,0]+=1
        while pos[i, 0] < 0:
            pos[i,0]+=l
            contador[i,0]-=1
        while pos[i, 1] > l:
            pos[i,1]-=l
            contador[i,1]+=1
        while pos[i, 1] < 0:
            pos[i,1]+=l
            contador[i,1]-=1
    return pos, contador

#endregion

#region variaveis alteraveis
intervalo = int(
#DE QUANTOS EM QUANTOS O PROGRAMA SALVA OS DADOS (EVITA ARQUIVOS EXCESSIVAMENTE PESADOS PRA TEMPOS LONGOS)
#OU DTS PEQUENOS, 1 PRA USAR TODOS
2
)

pbcepotencial = (
#SIM OU NAO, NAO QUANDO NAO HA CAMPO POTENCIAL NEM PBC, SIM QUANDO TEM
"NAO"
)

l = (
#TAMANHO DA CAIXA DO PBC
20
)

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
1
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

xini = (
0
)

#endregion

c1 = np.exp(-gaminha*dt)

c2  = (np.sqrt(1 - np.exp(-2*gaminha*dt)))*(np.sqrt(m*kb*temp))

npassos = int(np.round(tmax/dt))

if int(npassos%intervalo) != 0:
    print(f"Combinação npassos com intervalo não funcional, cuidado pra que o intervalo seja um inteiro que divide npassos sem ter resto")
    exit(0)

nsalvos = int((npassos/intervalo) + 1)

aleatorios = np.random.normal(size = (npassos, npar, 2)) * c2

xy = np.zeros((nsalvos, npar, 2))

xy[0] = (np.random.rand(npar, 2) - 0.5) * 2 * rmax

pxy = np.zeros((nsalvos, npar, 2))

tempos = np.arange(0, tmax + dt, dt*intervalo)

pbccounter = np.zeros((nsalvos, npar, 2))

salvador = int(0)

if pbcepotencial == "NAO":
    xyatual = xy[0]
    pxyatual = pxy[0]
    for i in range(0, npassos):
        #BAOAB 2D SEM PBC COM CAMPO
        #B
        pxytemp = pxyatual + dt * (potencial(xyatual) + lennardjones2d(xyatual))/2
        #A
        xytemp = xyatual + dt*pxytemp/(2*m)
        #O
        pxylinha = c1*pxytemp + aleatorios[i]
        #A
        xyatual = xytemp + dt*pxylinha/(2*m)
        #B
        pxyatual = pxylinha + dt * (potencial(xyatual) + lennardjones2d(xyatual))/2
        #FIM DO BAOAB, HORA DE SALVAR
        salvador+=1
        if salvador%intervalo == 0:
            xy[int(salvador/intervalo)] = xyatual
            pxy[int(salvador/intervalo)] = pxyatual


elif pbcepotencial == "SIM":
    xyatual = xy[0]
    pxyatual = pxy[0]
    pbctemp = pbccounter[0]
    for i in range(0, npassos):
        #BAOAB 2D COM PBC E CAMPO
        #B
        pxytemp = pxyatual + dt*lennardjones2d(xyatual)/2
        #A
        xytemp = xyatual + dt*pxytemp/(2*m)
        xytemp, pbctemp = pbcvoltas(xytemp, pbctemp)
        #O
        pxylinha = c1*pxytemp + aleatorios[i]
        #A
        xyatual = xytemp + dt*pxylinha/(2*m)
        xyatual, pbctemp = pbcvoltas(xyatual, pbctemp)
        #B
        pxyatual = pxylinha + dt*lennardjones2d(xyatual)/2
        #FIM DO BAOAB, HORA DE SALVAR
        salvador+=1
        if salvador%intervalo == 0:
            xy[int(salvador/intervalo)] = xyatual
            pxy[int(salvador/intervalo)] = pxyatual
            pbccounter[int(salvador/intervalo)] = pbctemp

for i in range(0, nsalvos):
    plt.cla()
    plt.xlim(-5, 5)
    plt.ylim(-5, 5)
    plt.scatter(xy[i, :, 0], xy[i, :, 1], alpha = 0.2, color = "green")
    plt.pause(0.0001)
plt.show(block = False)