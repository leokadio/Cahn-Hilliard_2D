from binascii import b2a_hex
import numpy as np
import matplotlib.pyplot as plt

#o que tem que fazer aqui? MSD, animação

codigo = (
#DIGITE O CÓDIGO AQUI
4888
)
modo = (
#OPCOES: MSD, ANIMACAO, X, Y, PX, PY
"X"
)

valores = np.load(f".\\#{codigo}\\val#{codigo}.npy")
(
intervalo,      pbcoupotencial,  l,              alfa,            beta,          gaminha,        temp,
dt,             tmax,           npar,           respalhamento,  rcorte,         seedinicial
) = (
valores[0],     valores[1],     valores[2],     valores[3],     valores[4],     valores[5],     valores[6],
valores[7],     valores[8],     valores[9],     valores[10],    valores[11],    valores[12]
)

estadoaleatorio = tuple(np.load(f".\\#{codigo}\\state#{codigo}.npy", allow_pickle = True))

xy = np.load(f".\\#{codigo}\\xy#{codigo}.npy")

pxy = np.load(f".\\#{codigo}\\pxy#{codigo}.npy")

pbccounter = np.load(f".\\#{codigo}\\pbccounter#{codigo}.npy")

tempos = np.arange(0, tmax + dt, dt*intervalo)

if modo == "X":
    for i in range(int(npar)):
        plt.plot(tempos, xy[:,i,0])
        
    plt.show()