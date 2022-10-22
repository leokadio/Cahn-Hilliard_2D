import numpy as np
import matplotlib.pyplot as plt
import os

codigo = (
#DIGITE O CÓDIGO AQUI
813447
)
divisoes = int(
#DIVISOES PRA FATIAR
1000
)

valores = np.load(f".\\#{codigo}\\val#{codigo}.npy")
(
intervalo,      alfa,           beta,           gaminha,        temp,
dt,             tmax,           npar,           seedinicial
) = (
valores[0],     valores[1],     valores[2],     valores[3],     valores[4],
valores[5],     valores[6],     valores[7],     valores[8]
)

tmax = int(tmax)

temp = int(temp)

estadoaleatorio = tuple(np.load(f".\\#{codigo}\\state#{codigo}.npy", allow_pickle = True))

xy = np.load(f".\\#{codigo}\\xy#{codigo}.npy")

pxy = np.load(f".\\#{codigo}\\pxy#{codigo}.npy")

npassos = int(np.round(tmax/dt))

nsalvos = int((npassos/intervalo) + 1)

tempos = np.linspace(0, tmax, nsalvos)

plt.figure(figsize = (6,6))

novotamanho = int(1 + ((nsalvos-1)/divisoes))
indice = novotamanho - 1
print(indice)
xx = xy[:, 0]
yy = xy[:, 1]
for i in range(divisoes):
    xini = xx[i*indice]
    yini = yy[i*indice]
    #plt.scatter(xx[i*indice : 10001+(i)*indice] - xini, yy[i*indice : 10001+(i)*indice] - yini, alpha = 0.025, s = 0.5)
    plt.title("Rastro das 1000 Partículas no Espaço\n" + r"Tempo efetivo: 500")
    plt.xlabel(r"$x$")
    plt.ylabel(r"$y$")
    plt.scatter(xx[i*indice : 1+(i+1)*indice:10] - xini, yy[i*indice : 1+(i+1)*indice:10] - yini, alpha = 0.025, s = 0.5)

plt.xlim(-150, 150)

plt.ylim(-150, 150)

plt.savefig(f".\\ANIMPOS\\{6}.png")

#plt.show()