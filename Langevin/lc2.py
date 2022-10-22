import numpy as np
import matplotlib.pyplot as plt
#region funcoes
def potencial(pos):
    forca = np.zeros(2)
    forca[0] = -4*alfa*(pos[0]**3) + 2*beta*pos[0]
    forca[1] = -4*alfa*(pos[1]**3) + 2*beta*pos[1]
    return forca
#endregion

codigo = (
#DIGITE O CÓDIGO AQUI
201446
)
tnovo = (
500000
)

valores = np.load(f".\\#{codigo}\\val#{codigo}.npy")
(
intervalo,      alfa,           beta,           gaminha,        temp,
dt,             tmax,           npar,           seedinicial
) = (
valores[0],     valores[1],     valores[2],     valores[3],     valores[4],
valores[5],     valores[6],     valores[7],     valores[8]
)

estadoaleatorio = tuple(np.load(f".\\#{codigo}\\state#{codigo}.npy", allow_pickle = True))

xy = np.load(f".\\#{codigo}\\xy#{codigo}.npy")

pxy = np.load(f".\\#{codigo}\\pxy#{codigo}.npy")

np.random.set_state(estadoaleatorio)

npassos = int(np.round((tnovo - tmax)/dt))

nsalvos = int((npassos/intervalo) + 1)

c1 = np.exp(-gaminha*dt)

c2  = (np.sqrt(1 - np.exp(-2*gaminha*dt)))*np.sqrt(temp)

aleatorios = np.random.normal(0, 1, size = (npassos, 2)) * c2

print("Tudo pronto, hora de começar!")

xyatual = xy[-1]

pxyatual = pxy[-1]

xynovo = np.zeros((nsalvos, 2))

pxynovo = np.zeros((nsalvos, 2))

salvador = int(0)

for i in range(0, npassos):
    #BAOAB 2D SEM PBC COM CAMPO
    #B
    pxytemp = pxyatual + dt * (potencial(xyatual))/2
    #A
    xytemp = xyatual + dt*pxytemp/2
    #O
    pxylinha = c1*pxytemp + aleatorios[i]
    #A
    xyatual = xytemp + dt*pxylinha/2
    #B
    pxyatual = pxylinha + dt * (potencial(xyatual))/2
    #FIM DO BAOAB, HORA DE SALVAR
    salvador+=1
    if salvador%intervalo == 0:
        xynovo[int(salvador/intervalo)] = xyatual
        pxynovo[int(salvador/intervalo)] = pxyatual

print("Acabou, hora de salvar!")

xy = np.append(xy, xynovo[1:], axis = 0)

pxy = np.append(pxy, pxynovo[1:], axis = 0)

estadoaleatorio = np.random.get_state()

print(f"O código será {codigo}")

tmax = tnovo

informacoesleitura = (f"""Infos do código {codigo}
intervalo = int(
#DE QUANTOS EM QUANTOS O PROGRAMA SALVA OS DADOS (EVITA ARQUIVOS EXCESSIVAMENTE PESADOS PRA TEMPOS LONGOS)
#OU DTS PEQUENOS, 1 PRA USAR TODOS
{intervalo}
)
#ALFA E BETA SÃO DO CAMPO POTENCIAL
alfa = (
{alfa}
)
beta = (
{beta}
)
gaminha = (
#RELATIVO AO RUIDO ESTOCASTICO
{gaminha}
)
temp = (
{temp}
)
dt = (
{dt}
)
t = (
{tmax}
)
seedinicial = (
#SÓ USE DE NOVO SE FOR PRA FAZER DO ZERO IGUAL
{seedinicial}
)""")

valores = np.zeros(9)
(
valores[0],     valores[1],     valores[2],     valores[3],     valores[4],
valores[5],     valores[6],     valores[7],     valores[8]
) = (
intervalo,      alfa,           beta,           gaminha,        temp,
dt,             tmax,           npar,           seedinicial
)

print("Hora de salvar os arquivos...")

np.save(f".\\#{codigo}\\state#{codigo}.npy", estadoaleatorio, allow_pickle = True)

np.save(f".\\#{codigo}\\val#{codigo}.npy", valores)

np.save(f".\\#{codigo}\\xy#{codigo}.npy", xy)

np.save(f".\\#{codigo}\\pxy#{codigo}.npy", pxy)

arquivo = open(f".\\#{codigo}\\info#{codigo}.txt", "w")

arquivo.write(f"{informacoesleitura}")

arquivo.close()

print(f"Tudo certo! Código {codigo}.")