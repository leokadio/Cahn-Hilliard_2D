import numpy as np
import matplotlib.pyplot as plt
import os

codigo = (
#DIGITE O CÓDIGO AQUI
813447
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

p = np.sqrt(pxy[:, 0]**2 + pxy[:, 1]**2)
#MOMENTUM MAIS COMUM
n, bins, patches = plt.hist(p, 500, histtype = "step",  density = True)
maior = np.argmax(n)
pcomum = (bins[maior + 1] + bins[maior])/2
plt.axvline(pcomum, color = "red", alpha = 0.4, label = f"Momentum mais provável: {pcomum:.3f}")
#MOMENTUM MEDIO
pmed = np.mean(p)
plt.axvline(pmed, c = "green", label = f"Momentum médio: {pmed:.3f}")
#MOMENTUM QUADRADO MEDIO
pqmed = np.sqrt(np.mean(p**2))
plt.axvline(pqmed, color = "purple", alpha = 0.4, label = f"Momentum rms: {pqmed:.3f}\n" + r"$\frac{p_{rms}}{\sqrt{T}}$" + f": {pqmed/np.sqrt(temp):.3f}")
plt.xlim(0, 7)
plt.ylim(0, 0.7)
plt.grid(alpha = 0.3)
plt.legend(loc = 1)
plt.title(f"Momentum em módulo\n" + r"$\gamma$ = " + f"{gaminha}, Temp. = {temp}, " + r'$\Delta t$ = '+f'{dt}, Instantes = {nsalvos}')
plt.ylabel(r'$P(x)$')
plt.xlabel(r'$\left|\vec{p}(t)\right|$')

plt.hist(p[:1000000001], 500, histtype = "step",  density = True, color = "orange", alpha = 0.5)

plt.savefig(f".\\ANIMPDF\\{1000000001}.png")