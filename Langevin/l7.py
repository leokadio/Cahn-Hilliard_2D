import numpy as np
import os

#baoab 1 par 2d unidades reduzidas com maior cuidado, salva em arquivos
#region funcoes
def potencial(pos):
    forca = np.zeros(2)
    forca[0] = -4*alfa*(pos[0]**3) + 2*beta*pos[0]
    forca[1] = -4*alfa*(pos[1]**3) + 2*beta*pos[1]
    return forca
#endregion

#region variaveis alteraveis
intervalo = int(
#DE QUANTOS EM QUANTOS O PROGRAMA SALVA OS DADOS (EVITA ARQUIVOS EXCESSIVAMENTE PESADOS PRA TEMPOS LONGOS)
#OU DTS PEQUENOS, 1 PRA USAR TODOS
1
)
#ALFA E BETA SÃO DO CAMPO POTENCIAL
alfa = (
0
)
beta = (
0
)
gaminha = (
#RELATIVO AO RUIDO ESTOCASTICO
0.1
)
temp = (
#TEMPERATURA, 1 É EQ A 118K +-
3
)
dt = (
10**-2
)
tmax = (
500000
)
npar = (
#NUMERO DE PARTICULAS
1
)
seedinicial = (
468884114
)
'''
SEEDS DA WIKI
2135489      DT -2 GAMINHA +1
87846354     DT -2 GAMINHA 0	
459618741    DT -2 GAMINHA -1
#TEMP = 2
54684135     DT -2 GAMINHA +1
84653987465  DT -2 GAMINHA 0
9776678878   DT -2 GAMINHA -1
#TEMP = 3
7984651 	 DT -2 GAMINHA +1
4646464      DT -2 GAMINHA 0
468884114    DT -2 GAMINHA -1
'''
#endregion

print("Indo calcular constantes...")

c1 = np.exp(-gaminha*dt)

c2  = (np.sqrt(1 - np.exp(-2*gaminha*dt)))*np.sqrt(temp)

print("Constantes calculadas, hora de ver se tem npassos certos.")

npassos = int(np.round(tmax/dt))

if int(npassos%intervalo) != 0:
    print(f"Combinação npassos com intervalo não funcional, cuidado pra que o intervalo seja um inteiro que divide npassos sem ter resto")
    exit(0)

print(f"Passos ok, passos que precisam ser calculados: {npassos}")

nsalvos = int((npassos/intervalo) + 1)

print(f"{nsalvos} serão salvos (contando o primeiro).")

aleatorios = np.random.normal(0, 1, size = (npassos, 2)) * c2

xy = np.zeros((nsalvos, 2))

checar = 0

pxy = np.zeros((nsalvos, 2))

tempos = np.arange(0, tmax + dt, dt*intervalo)

salvador = int(0)

print("Tudo pronto, hora de começar!")

xyatual = xy[0]

pxyatual = pxy[0]

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
        xy[int(salvador/intervalo)] = xyatual
        pxy[int(salvador/intervalo)] = pxyatual

print("Acabou, hora de salvar!")

estadoaleatorio = np.random.get_state()

np.random.seed()

codigo = int(np.random.rand(1)*10**6)

print(f"O código será {codigo}")

while os.path.isdir(f"{codigo}") == True:
    print("Deu igual! A chance disso é baixíssima, peço perdão por ter desperdiçado sua sorte!")
    print("O programa deve corrigir isso, se essa mensagem estiver sendo repitida, há um erro grave!")
    codigo+=1

os.makedirs(f".\\#{codigo}", exist_ok = True)

print(f"Pasta única criada! Nome {codigo}")

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