import numpy as np
import os

#baoab n par lennard jones potencial 2d unidades reduzidas com maior cuidado, salva em arquivos
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
                a = 48*( ((1/r)**14) - ((1/r)**8)/2 )
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
                a = 48*( ((1/r)**14) - ((1/r)**8)/2 )
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
1
)
pbcoupotencial = (
#ESCREVER 0 SE TEM PBC, 1 SE TEM POTENCIAL
1
)
l = (
#TAMANHO DA CAIXA DO PBC (SE TEM, CASO CONTRÁRIO IGNORE)
20
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
0.5
)
temp = (
#TEMPERATURA, 1 É EQ A 118K +-
1
)
dt = (
10**-2
)
tmax = (
100000
)
npar = (
#NUMERO DE PARTICULAS
1
)
respalhamento = (
#RAIO DE ESPALHAMENTO DO INICIO ALEATORIO
0
)
rcorte = (
#RAIO DE CORTE DO LENNARD JONES
3
)
seedinicial = (
4854896418
)
distmin = (
2
)
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

aleatorios = np.random.normal(size = (npassos, npar, 2)) * c2

xy = np.zeros((nsalvos, npar, 2))

xyinicial = (np.random.rand(npar, 2) - 0.5) * 2 * respalhamento

checar = 0

while checar != 0:
    checar = 0
    for i in range(npar):
        for j in range(npar):
            dist = np.sqrt((xyinicial[i, 0]-xyinicial[j, 0])**2  + (xyinicial[i, 1]-xyinicial[j, 1])**2)
            if dist < distmin:
                checar = 1
            while dist < distmin:
                xyinicial[i] = (np.random.rand(2) - 0.5) * 2 * respalhamento
                dist = np.sqrt((xyinicial[i, 0]-xyinicial[j, 0])**2  + (xyinicial[i, 1]-xyinicial[j, 1])**2)

xy[0] = (np.random.rand(npar, 2) - 0.5) * 2 * respalhamento

pxy = np.zeros((nsalvos, npar, 2))

tempos = np.arange(0, tmax + dt, dt*intervalo)

pbccounter = np.zeros((nsalvos, npar, 2))

salvador = int(0)

print("Tudo pronto, hora de começar!")

if pbcoupotencial == 1:
    xyatual = xy[0]
    pxyatual = pxy[0]
    for i in range(0, npassos):
        #BAOAB 2D SEM PBC COM CAMPO
        #B
        pxytemp = pxyatual + dt * (potencial(xyatual) + lennardjones2d(xyatual))/2
        #A
        xytemp = xyatual + dt*pxytemp/2
        #O
        pxylinha = c1*pxytemp + aleatorios[i]
        #A
        xyatual = xytemp + dt*pxylinha/2
        #B
        pxyatual = pxylinha + dt * (potencial(xyatual) + lennardjones2d(xyatual))/2
        #FIM DO BAOAB, HORA DE SALVAR
        salvador+=1
        if salvador%intervalo == 0:
            xy[int(salvador/intervalo)] = xyatual
            pxy[int(salvador/intervalo)] = pxyatual


elif pbcoupotencial == 0:
    xyatual = xy[0]
    pxyatual = pxy[0]
    pbctemp = pbccounter[0]
    for i in range(0, npassos):
        #BAOAB 2D COM PBC E CAMPO
        #B
        pxytemp = pxyatual + dt*lennardjones2d(xyatual)/2
        #A
        xytemp = xyatual + dt*pxytemp/2
        xytemp, pbctemp = pbcvoltas(xytemp, pbctemp)
        #O
        pxylinha = c1*pxytemp + aleatorios[i]
        #A
        xyatual = xytemp + dt*pxylinha/2
        xyatual, pbctemp = pbcvoltas(xyatual, pbctemp)
        #B
        pxyatual = pxylinha + dt*lennardjones2d(xyatual)/2
        #FIM DO BAOAB, HORA DE SALVAR
        salvador+=1
        if salvador%intervalo == 0:
            xy[int(salvador/intervalo)] = xyatual
            pxy[int(salvador/intervalo)] = pxyatual
            pbccounter[int(salvador/intervalo)] = pbctemp

print("Acabou, hora de salvar!")

estadoaleatorio = np.random.get_state()

np.random.seed()

codigo = int(np.random.rand(1)*10**4)

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
pbcoupotencial = (
#ESCREVER 0 SE TEM PBC, 1 SE TEM POTENCIAL
{pbcoupotencial}
)
l = (
#TAMANHO DA CAIXA DO PBC
{l}
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
npar = (
#NUMERO DE PARTICULAS
{npar}
)
respalhamento = (
#RAIO DE ESPALHAMENTO DO INICIO ALEATORIO
{respalhamento}
)
rcorte = (
#RAIO DE CORTE DO LENNARD JONES
{rcorte}
)
seedinicial = (
#SÓ USE DE NOVO SE FOR PRA FAZER DO ZERO IGUAL
{seedinicial}
)
distmin = (
{distmin}
)""")

valores = np.zeros(14)
(
valores[0],     valores[1],     valores[2],     valores[3],     valores[4],     valores[5],     valores[6],
valores[7],     valores[8],     valores[9],     valores[10],    valores[11],    valores[12],    valores[13]
) = (
intervalo,      pbcoupotencial, l,              alfa,            beta,          gaminha,        temp,
dt,             tmax,           npar,            respalhamento,   rcorte,        seedinicial,   distmin
)

print("Hora de salvar os arquivos...")

np.save(f".\\#{codigo}\\state#{codigo}.npy", estadoaleatorio, allow_pickle = True)

np.save(f".\\#{codigo}\\val#{codigo}.npy", valores)

np.save(f".\\#{codigo}\\xy#{codigo}.npy", xy)

np.save(f".\\#{codigo}\\pxy#{codigo}.npy", pxy)

np.save(f".\\#{codigo}\\pbccounter#{codigo}.npy", pbccounter)

arquivo = open(f".\\#{codigo}\\info#{codigo}.txt", "w")

arquivo.write(f"{informacoesleitura}")

arquivo.close()

print(f"Tudo certo! Código {codigo}.")