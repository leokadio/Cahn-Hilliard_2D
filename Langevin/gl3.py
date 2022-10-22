import numpy as np
import matplotlib.pyplot as plt

#o que tem que fazer aqui? MSD, animação

codigo = (
#DIGITE O CÓDIGO AQUI
2215
)
modo = (
#OPCOES: MSD, ANIMACAO, X, Y, PX, PY, XY (DIST DA ORIGEM), POS, COMPARE
"COMPARE"
)
divisoes = int(
10
)

valores = np.load(f".\\#{codigo}\\val#{codigo}.npy")
(
intervalo,      pbcoupotencial,  l,              alfa,            beta,          gaminha,       temp,
dt,             tmax,           npar,            respalhamento,   rcorte,        seedinicial,   distmin
) = (
valores[0],     valores[1],     valores[2],     valores[3],     valores[4],     valores[5],     valores[6],
valores[7],     valores[8],     valores[9],     valores[10],    valores[11],    valores[12],    valores[13]
)

npar = int(npar)

estadoaleatorio = tuple(np.load(f".\\#{codigo}\\state#{codigo}.npy", allow_pickle = True))

xy = np.load(f".\\#{codigo}\\xy#{codigo}.npy")

pxy = np.load(f".\\#{codigo}\\pxy#{codigo}.npy")

pbccounter = np.load(f".\\#{codigo}\\pbccounter#{codigo}.npy")

npassos = int(np.round(tmax/dt))

nsalvos = int((npassos/intervalo) + 1)

tempos = np.linspace(0, tmax, nsalvos)

if int((nsalvos - 1)) % divisoes != 0:
    exit()

if modo == "X":
    for i in range(npar):
        plt.plot(tempos, xy[:,i,0])
    plt.show()

if modo == "Y":
    for i in range(npar):
        plt.plot(tempos, xy[:,i,1])
        
    plt.show()

if modo == "PX":
    for i in range(npar):
        plt.plot(tempos, pxy[:,i,0])
        
    plt.show()

if modo == "PY":
    for i in range(npar):
        plt.plot(tempos, pxy[:,i,1])
        
    plt.show()

if modo == "XY":
    alfas = np.linspace(0, 1, nsalvos)
    for i in range(npar):
        distorigem = np.sqrt(xy[:, :, 0]**2 + xy[:, :, 1]**2)
        plt.plot(tempos, distorigem[:,i])
    plt.show()

if modo == "MSD":
    alfas = np.linspace(0, 1, nsalvos)
    for i in range(npar):
        distorigem = (xy[:, :, 0] - xy[0, :, 0])**2 + (xy[:, :, 1] - xy[0, :, 1])**2
        plt.plot(tempos, distorigem[:,i])
        plt.yscale('log')
        plt.xscale('log')
    plt.show()

if modo == "POS":
    alfas = np.linspace(0, 1, nsalvos)
    for i in range(npar):
        plt.scatter(xy[:,i,0], xy[:,i,1], color = "blue")
    plt.show()

if modo == "COMPARE":
    novotamanho = int(1 + ((nsalvos-1)/divisoes))
    divididos = np.zeros((divisoes, novotamanho, npar, 2))
    eixox = np.linspace(0, int(tmax/divisoes), novotamanho)
    for i in range(npar):
        for j in range(divisoes):
            print(int(((j+1)*(novotamanho-1)) + 1))
            divididos[j, :, i] = xy[int(j * (novotamanho - 1)) : int(((j+1)*(novotamanho-1)) + 1), i] - xy[int(j * (novotamanho - 1)), i]
    somados = np.zeros((novotamanho, npar))
    for i in range(npar):
        for j in range(divisoes):
            somados[:, i] = (divididos[j, :, i, 0]**2) + (divididos[j, :, i, 1]**2)
    eixox = np.linspace(0, int(tmax/divisoes), novotamanho)
    for i in range(npar):
        plt.plot(eixox, somados[:, i])
        plt.yscale('log')
        plt.xscale('log')
        plt.show()
        dezao = np.divide(somados[:, i],(4*eixox))
        plt.plot(eixox, dezao)
        plt.axhline(2*temp/(gaminha))
        plt.show()