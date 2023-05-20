import numpy as np
from scipy.fft import rfft2, irfft2, rfftfreq, fftfreq
import os
import time
#region função Fourier
def cfourierini(aa, kk2, kk4):#calculador da transformada inicial
    cct = rfft2(aa)
    cct3 = rfft2(aa**3)
    cct = cct + difd*dt*(-kk2*(cct3 - cct) - kk4*cct)
    return cct

def cfouriermid(aa, kk2, kk4):#calculador de cada passo
    cct = aa
    cct3 = rfft2(irfft2(aa)**3)
    cct = cct + difd*dt*(-kk2*(cct3 - cct) - kk4*cct)
    return cct
#endregion

#DIGITE O CÓDIGO AQUI
codigo = (
5002
)
#DIGITE O NOVO TEMPO MAXIMO AQUI
tmax = (
6
)
#DAQUI PRA BAIXO MELHOR NÃO MEXER

#region leitura dos arquivos
valores = np.load(f".\\{codigo}\\val{codigo}.npy")

normalizar, mediadesejada, seed,        gamma,      difd,       intervalo,       xmax,       t,          dt,         dx = (
valores[0], valores[1],    valores[2],  valores[3], valores[4], int(valores[5]), valores[6], valores[7], valores[8], valores[9])

ccoriginal = np.load(f".\\{codigo}\\{codigo}.npy")

print("Arquivo encontrado e carregado!")
#endregion

#region gerar frequências

l = int((xmax/dx))

nx21 = int((l/2) + 1)

k1  = rfftfreq(l, dx/(2*np.pi))

k2 = fftfreq(l, dx/(2*np.pi))

r1, r2 = np.meshgrid(k1, k2)

p = r1**2 + r2**2

q = (p**2)*gamma
#endregion

#region cálculo de quantos arrays faltam
u = 1

tini = t

while t < tmax:
    for i in range(intervalo):
        t = round(t + dt, int(-np.log10(dt) + 2))
    u+=1
#endregion

#region previsão de tempo

cc = np.zeros((u, l, l))

cc[0] = ccoriginal[-1]

temp = cfourierini(cc[0], p, q)

tempoini = time.time()
for i in range(intervalo):
    temp = cfouriermid(temp, p, q)
temp = irfft2(temp)
tempofinal = time.time()
tempoestimado = tempofinal + (tempofinal - tempoini)*(u-1)

print(f"Faltam {u-1} arrays pro tempo final. Tempo estimado: +{time.ctime(tempoestimado)}")
#endregion

#region parte importante
print("Começando...")

v = 1

t = tini

while t < tmax:
    for i in range(intervalo):
        temp = cfouriermid(temp, p, q)
        t = round(t + dt, int(-np.log10(dt) + 2))
    cc[v] = irfft2(temp)
    print(f"Array numero {v} de {u-1} feito!")
    v+=1

#endregion

if v != u:
    print("Algo deu errado! Não salvou.")
    exit()

#region salvar arquivo e infos
print("Acabou! Hora de appendar um ao outro!")

cc = np.append(ccoriginal, cc[1:], axis = 0)

print("Appendado com sucesso!")

os.makedirs(f".\\{codigo}", exist_ok = True)

print("Pasta criada!")

np.save(f".\\{codigo}\\{codigo}.npy", cc)

informacoescopiaveis = f"""#valores do codigo {codigo}, normalização {normalizar} em média {mediadesejada}. Este arquivo é para caso de perder o arquivo de valores
#ou ser necessário consultar os valores.

normalizar = {normalizar}

mediadesejada = {mediadesejada}

codigo = {codigo}

seed = {seed}

gamma = {gamma}

difd = {difd}

intervalo = {intervalo}

xmax = {xmax}

t = {t}

dt = {dt}

dx = {dx}"""

arquivo = open(f".\\{codigo}\\{codigo}.txt", "w")

arquivo.write(f"{informacoescopiaveis}")

arquivo.close()

valores[0], valores[1],    valores[2], valores[3], valores[4], valores[5], valores[6], valores[7], valores[8], valores[9] = (
normalizar, mediadesejada, seed,       gamma,      difd,       intervalo,  xmax,       t,          dt,         dx)

np.save(f".\\{codigo}\\val{codigo}.npy", valores)

print(f"Array impresso na pasta! Código: {codigo}")

#endregion
