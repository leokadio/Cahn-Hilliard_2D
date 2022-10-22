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
desviodividido = np.zeros(novotamanho)
indice = novotamanho - 1
xx = xy[:, 0]
yy = xy[:, 1]
for i in range(divisoes):
    xini = xx[i*indice]
    yini = yy[i*indice]
    dx = xx[i*indice : 1+(i+1)*indice] - xini
    dy = yy[i*indice : 1+(i+1)*indice] - yini
    desviodividido += dx**2 + dy**2
desviodividido = (desviodividido/divisoes)[1:]
eixox = np.linspace(0, int(tmax/divisoes), int((nsalvos - 1)/divisoes) + 1)[1:]
difusivo = desviodividido[int(10/(dt*gaminha)):]
dezao = np.mean(difusivo/eixox[int(10/(dt*gaminha)):])/4
eixox = np.log10(eixox)
desviodividido = np.log10(desviodividido)
balistico = desviodividido[:int(1/(dt*gaminha))]
difusivo = desviodividido[int(10/(dt*gaminha)):]
bal = np.polyfit(eixox[:int(1/(dt*gaminha))], balistico, 1)
dif = np.polyfit(eixox[int(10/(dt*gaminha)):], difusivo, 1)
reta1 = bal[0]*eixox + bal[1]
reta2 = dif[0]*eixox + dif[1]
plt.text(2.15, -3, r"D" + f" analítico: {temp/gaminha}\n" + r"D" + f" calculado: {dezao:.3f}", bbox=dict(boxstyle='square', ec='k', color='white'))
plt.plot(eixox, reta1, color = "red", label = f"Inclinação da reta: {bal[0]:.2f}", alpha = 0.4)
plt.plot(eixox, reta2, color = "purple", label = f"Inclinação da reta: {dif[0]:.2f}", alpha = 0.4)
plt.axvline(-np.log10(gaminha) + 1, label = f"Início do regime\nnormalmente difusivo:\ntempo = {int(10/gaminha)}", c = "orange")
plt.grid()
#plt.scatter(eixox[:int(1000000000)], desviodividido[:int(1000000000)], s = 10)
plt.xlabel(r'$log_{10}(t)$')
plt.ylabel(r'$log_{10}(\left|\vec{r}\right|^{2})$')
plt.ylim(-4, 5)
plt.xlim(-4, 5)
plt.legend(loc = 2)
plt.gca().set_aspect('equal', adjustable='box')
plt.title(f'MSD de uma partícula livre:\n'+
r"$\gamma$ = " + f"{gaminha}, Temp. = {temp}, " + r'$\Delta t$ = '+f'{dt}, Fatias = {divisoes}')

plt.savefig(f".\\ANIMMSD\\{0}.png")