import numpy as np

#region variaveis alteraveis
#DIGITE O CÓDIGO AQUI
codigo = (
8731
)

valores = np.load(f".\\#{codigo}\\val#{codigo}.npy")
(
intervalo,      pbcoupotencial,  l,              alfa,            beta,          gaminha,       temp,
dt,             t,               npar,           respalhamento,   rcorte,        seedinicial,   distmin
) = (
valores[0],     valores[1],     valores[2],     valores[3],     valores[4],     valores[5],     valores[6],
valores[7],     valores[8],     valores[9],     valores[10],    valores[11],    valores[12],    valores[13]
)

#alfa, beta = 0, 0

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
{t}
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
dt,             t,            npar,           respalhamento,   rcorte,        seedinicial,   distmin
)

arquivo = open(f".\\#{codigo}\\info#{codigo}.txt", "w")

arquivo.write(f"{informacoesleitura}")

arquivo.close()

print(f"Tudo certo! Lembrando, o código é {codigo}.")