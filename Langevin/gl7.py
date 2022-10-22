import numpy as np
import matplotlib.pyplot as plt
import os

codigo = (
#DIGITE O CÓDIGO AQUI
54316
)
modo = (
#OPCOES: X, Y, PX, PY, P, POS, MSD, COEFDIF
"MSD"
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

if int((nsalvos - 1)) % divisoes != 0:
    exit()

if modo == "X":
    plt.scatter(tempos, xy[:,0])
    

if modo == "Y":
    plt.scatter(tempos, xy[:,1])
        
if modo == "PX":
    plt.hist(pxy[:,0], 50)
    plt.title(f"Momentum x\n" + r"$\gamma$ = " + f"{gaminha}, Temp. = {temp}, " + r'$\Delta t$ = '+f'{dt}, Instantes = {nsalvos}')
        
    

if modo == "PY":
    plt.hist(pxy[:,1], 50)
    plt.title(f"Momentum y\n" + r"$\gamma$ = " + f"{gaminha}, Temp. = {temp}, " + r'$\Delta t$ = '+f'{dt}, Instantes = {nsalvos}')
    

if modo == "P":
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
    

if modo == "POS":
    plt.scatter(xy[:,0], xy[:,1], color = "blue", s = 0.1)
    

if modo == "MSD":
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
    plt.scatter(eixox, desviodividido, s = 1)
    plt.xlabel(r'$log_{10}(t)$')
    plt.ylabel(r'$log_{10}(\left|\vec{r}\right|^{2})$')
    plt.ylim(-4, 5)
    plt.xlim(-4, 5)
    plt.legend(loc = 2)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title(f'MSD de uma partícula livre:\n'+
    r"$\gamma$ = " + f"{gaminha}, Temp. = {temp}, " + r'$\Delta t$ = '+f'{dt}, Fatias = {divisoes}')
    
if modo == "COEFDIF":
    novotamanho = int(1 + ((nsalvos-1)/divisoes))
    desviodividido = np.zeros(novotamanho)
    eixox = np.linspace(0, int(tmax/divisoes), int((nsalvos - 1)/divisoes) + 1)
    inicio = novotamanho - 1
    final = novotamanho - 1
    xx = xy[:, 0]
    yy = xy[:, 1]
    for i in range(divisoes):
        xini = xx[i*inicio]
        yini = yy[i*inicio]
        dx = xx[i*inicio : 1+(i+1)*final] - xini
        dy = yy[i*inicio : 1+(i+1)*final] - yini
        desviodividido += dx**2 + dy**2
    desviodividido = desviodividido/divisoes

    tempoinicial = 10/gaminha
    tempofinal = dt*len(desviodividido)
    desviodividido = desviodividido[int(tempoinicial/dt):]
    tempos = np.linspace(tempoinicial,tempofinal, len(desviodividido))
    dezao = np.mean(desviodividido/tempos)/4
    print(temp/gaminha, dezao)
    tempos = np.log10(tempos)
    desviodividido = np.log10(desviodividido)
    plt.axvline(-np.log10(gaminha) + 1)
    plt.scatter(tempos, desviodividido, s = 1)
    
os.makedirs(f".\\{modo}", exist_ok = True)
plt.savefig(f".\\{modo}\\{modo}#{codigo}.png")
print(f"Último código: {codigo}")
#plt.show()