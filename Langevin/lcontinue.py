import numpy as np
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
#DIGITE O CÓDIGO AQUI
codigo = (
6081
)
#DIGITE O NOVO TEMPO MAXIMO AQUI
tmax = (
5000
)
#endregion

valores = np.load(f".\\#{codigo}\\val#{codigo}.npy")
(
intervalo,      pbcoupotencial,  l,              alfa,            beta,          gaminha,       temp,
dt,             t,               npar,           respalhamento,   rcorte,        seedinicial,   distmin
) = (
valores[0],     valores[1],     valores[2],     valores[3],     valores[4],     valores[5],     valores[6],
valores[7],     valores[8],     valores[9],     valores[10],    valores[11],    valores[12],    valores[13]
)

estadoaleatorio = tuple(np.load(f".\\#{codigo}\\state#{codigo}.npy", allow_pickle = True))

xyantigo = np.load(f".\\#{codigo}\\xy#{codigo}.npy")

pxyantigo = np.load(f".\\#{codigo}\\pxy#{codigo}.npy")

pbccounterantigo = np.load(f".\\#{codigo}\\pbccounter#{codigo}.npy")

npar = int(npar)

tfalta = tmax - t

npassos = int(np.round(tfalta/dt))

if int(npassos%intervalo) != 0:
    print(f"Combinação npassos com intervalo não funcional, cuidado pra que o intervalo seja um inteiro que divide npassos sem ter resto")
    exit(0)

print(f"Passos ok, passos que precisam ser calculados: {npassos}")

nsalvos = int((npassos/intervalo) + 1)

print(f"{nsalvos} serão salvos (contando o último do antigo).")

print("Indo calcular constantes...")

c1 = np.exp(-gaminha*dt)

c2  = (np.sqrt(1 - np.exp(-2*gaminha*dt)))*np.sqrt(temp)

print("Constantes calculadas.")

np.random.set_state(estadoaleatorio)

aleatorios = np.random.normal(size = (npassos, npar, 2)) * c2

xy = np.zeros((nsalvos, npar, 2))

xy[0] = xyantigo[-1]

pxy = np.zeros((nsalvos, npar, 2))

pxy[0] = pxyantigo[-1]

tempos = np.arange(0, tfalta + dt, dt*intervalo)

pbccounter = np.zeros((nsalvos, npar, 2))

pbccounter[0] = pbccounterantigo[-1]

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

xy = np.append(xyantigo, xy[1:], axis = 0)
pxy = np.append(pxyantigo, pxy[1:], axis = 0)
pbccounter = np.append(pbccounterantigo, pbccounter[1:], axis = 0)

informacoesleitura = (f"""Infos do código {codigo}
intervalo = int(
#DE QUANTOS EM QUANTOS O PROGRAMA SALVA OS DADOS (EVITA ARQUIVOS EXCESSIVAMENTE PESADOS PRA TEMPOS LONGOS
#OU DTS PEQUENOS), 1 PRA USAR TODOS
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

(
valores[0],     valores[1],     valores[2],     valores[3],     valores[4],     valores[5],     valores[6],
valores[7],     valores[8],     valores[9],     valores[10],    valores[11],    valores[12],    valores[13]
) = (
intervalo,      pbcoupotencial,  l,              alfa,            beta,          gaminha,       temp,
dt,             tmax,            npar,           respalhamento,   rcorte,        seedinicial,   distmin
)

estadoaleatorio = np.random.get_state()

print("Hora de salvar os arquivos...")

np.save(f".\\#{codigo}\\state#{codigo}.npy", estadoaleatorio, allow_pickle = True)

np.save(f".\\#{codigo}\\val#{codigo}.npy", valores)

np.save(f".\\#{codigo}\\xy#{codigo}.npy", xy)

np.save(f".\\#{codigo}\\pxy#{codigo}.npy", pxy)

np.save(f".\\#{codigo}\\pbccounter#{codigo}.npy", pbccounter)

arquivo = open(f".\\#{codigo}\\info#{codigo}.txt", "w")

arquivo.write(f"{informacoesleitura}")

arquivo.close()

print(f"Tudo certo! Lembrando, o código é {codigo}.")