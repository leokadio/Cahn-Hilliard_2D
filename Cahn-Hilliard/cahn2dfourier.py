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

#CONSTANTES INICIAIS
seed = 8456

gamma = (0.01)**2

difd = 1

intervalo = 50

xmax = 1

tmax = 0.05

dt = 1.8*(10**-7)

dx = 1/128

#NORMALIZAR, 0 PRA NÃO, 1 PARA SIM
normalizar = 1

mediadesejada = 0.5
#DAQUI PRA BAIXO MELHOR NÃO MEXER

#region gerar frequências
np.random.seed(seed)

l = int((xmax/dx))

nx21 = int((l/2) + 1)

k1  = rfftfreq(l, dx/(2*np.pi))

k2 = fftfreq(l, dx/(2*np.pi))

r1, r2 = np.meshgrid(k1, k2)

p = r1**2 + r2**2

q = (p**2)*gamma
#endregion

#region cálculo de quantos arrays faltam
t = 0

u = 1

while t < tmax:#ver tamanho do array
    for i in range(intervalo):
        t = round(t + dt, int(-np.log10(dt) + 2))
    u+=1
#endregion

#region criar array e calcular média do frame inicial

cc = np.zeros((u, l, l))

cc[0] = np.random.rand(l, l)*2 - 1

media = np.sum(cc[0])/(l**2)
#endregion

#region normalizador
if normalizar == 1:
    cc[0] = (((cc[0] - media)/(1 + abs(media))) * (1-abs(mediadesejada))) + mediadesejada
else:
    mediadesejada = 10
#endregion

#region previsão de tempo
tempoini = time.time()
temp = cfourierini(cc[0], p, q)

for i in range(intervalo):
    temp = cfouriermid(temp, p, q)
temp = irfft2(temp)
tempofinal = time.time()
tempoestimado = tempofinal + (tempofinal - tempoini)*(u-1)
#endregion

#region parte que funciona salvando coisa no pc, sem plotar ao vivo

print(f"Será um total de {u} arrays. O primeiro já está feito. Hora estimada de término: {time.ctime(tempoestimado)}. Começando...")

#region calculos
temp = cfourierini(cc[0], p, q)

v = 1

t = 0

while t < tmax:#parte boa do programa
    for i in range(intervalo):
        temp = cfouriermid(temp, p, q)
        t = round(t + dt, int(-np.log10(dt) + 2))
    cc[v] = irfft2(temp)
    print(f"Array numero {v+1} de {u} feito!")
    v+=1

tempofinaleira = time.time()
diftempo = tempofinaleira - tempoestimado
print(f"Acabou!")
#endregion

#region salvar valores
np.random.seed()

codigo = int(np.random.rand(1)*10**4)

while os.path.isdir(f"{codigo}") == True:
    print("Deu igual!")
    codigo+=1

os.makedirs(f".\\{codigo}", exist_ok = True)

print(f"Pasta única criada! Nome {codigo}")

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

valores = np.zeros(10)

valores[0], valores[1],    valores[2], valores[3], valores[4], valores[5], valores[6], valores[7], valores[8], valores[9] = (
normalizar, mediadesejada, seed,       gamma,      difd,       intervalo,  xmax,       t,          dt,         dx)

np.save(f".\\{codigo}\\val{codigo}.npy", valores)

np.save(f".\\{codigo}\\{codigo}.npy", cc)

arquivo = open(f".\\{codigo}\\{codigo}.txt", "w")

arquivo.write(f"{informacoescopiaveis}")

arquivo.close()
#endregion

#endregion