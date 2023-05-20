import numpy as np
import matplotlib.pyplot as plt
import os

codigo = (
#DIGITE O CÓDIGO AQUI
3427
)
framequetenho = (
#CASO JA TENHA RODADO O PROGRAMA ANTERIORMENTE, 0 PARA COMECAR DO PRIMEIRO
16550
)
colormapp = (
#ESCOLHER CORES NO SITE https://matplotlib.org/stable/tutorials/colors/colormaps.html#diverging
"Spectral"
)
pixelxpixel = (
#NUMERO DA RESOLUCAO DE 1 GRAFICO, VAI SER TRIPLICADO PARA PBC
#RECOMENDO 128 OU 256 QUANDO FAZENDO SEM PBC, E 256 OU 512 COM PBC
256
)
pbc = (
#SIM PRA PLOTAR UMA GRADE 3x3 DE GRÁFICOS, NAO PRO NORMAL
"NAO"
)
#DAQUI PRA BAIXO MELHOR NÃO MEXER

#region leitura dos arquivos
valores = np.load(f".\\{codigo}\\val{codigo}.npy")

normalizar, mediadesejada, seed,        gamma,      difd,       intervalo,  xmax,       t,          dt,         dx = (
valores[0], valores[1],    valores[2],  valores[3], valores[4], valores[5], valores[6], valores[7], valores[8], valores[9])

cc = np.load(f".\\{codigo}\\{codigo}.npy")

print(f"Array achado e carregado!")

framemax = len(cc)

#endregion

#region gerar frames e salvar com pbc
if pbc == "NAO":
    plt.figure(figsize = (1, 1))

    os.makedirs(f".\\{codigo}\\frames", exist_ok = True)

    print("Começando...")

    tatual = 0

    for i in range(framequetenho, framemax):
        plt.clf()
        ax = plt.axes([0,0,1,1])
        plt.imshow(cc[i], cmap = colormapp, vmin = -1, vmax = 1, interpolation = "none")
        plt.text(10, 100, f"Tempo atual: {dt*intervalo*framequetenho:.5f}", color = "white", fontsize=3, bbox=dict(facecolor='blue', alpha=0.3))
        ax.axis('off')
        plt.subplots_adjust(0, 0, 1, 1)
        plt.savefig(f".\\{codigo}\\frames\\frame{framequetenho+1}.png", dpi = pixelxpixel)
        print(f"Frame {framequetenho+1} de {framemax} feito e salvo com sucesso!")
        framequetenho+=1

if pbc == "SIM":
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(3,3)

    fig.set_size_inches(2, 2)

    ax1.axis('off')
    ax2.axis('off')
    ax3.axis('off')
    ax4.axis('off')
    ax5.axis('off')
    ax6.axis('off')
    ax7.axis('off')
    ax8.axis('off')
    ax9.axis('off')
    ax1.set_aspect('equal')
    ax2.set_aspect('equal')
    ax3.set_aspect('equal')
    ax4.set_aspect('equal')
    ax5.set_aspect('equal')
    ax6.set_aspect('equal')
    ax7.set_aspect('equal')
    ax8.set_aspect('equal')
    ax9.set_aspect('equal')

    plt.subplots_adjust(0, 0, 1, 1, wspace = 0, hspace = 0)

    tatual = round(framequetenho*dt*intervalo, int(-np.log10(dt*intervalo) + 3))
    os.makedirs(f".\\{codigo}\\framespbc", exist_ok = True)
    for i in range(framequetenho, framemax):
        ax5.clear()
        ax5.axis('off')
        ax5.set_aspect('equal')
        im1 = ax1.imshow(cc[i], cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
        im2 = ax2.imshow(cc[i], cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
        im3 = ax3.imshow(cc[i], cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
        im4 = ax4.imshow(cc[i], cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
        im5 = ax5.imshow(cc[i], cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
        im6 = ax6.imshow(cc[i], cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
        im7 = ax7.imshow(cc[i], cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')   
        im8 = ax8.imshow(cc[i], cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
        im9 = ax9.imshow(cc[i], cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
        texto = ax5.annotate(f"Tempo atual: {tatual:.5f}",(10, 100),  color = "white", fontsize=3, bbox=dict(facecolor='blue', alpha=0.3)) # add text
        plt.savefig(f".\\{codigo}\\framespbc\\frame{i+1}.png", dpi = pixelxpixel*3/2)
        print(f"Frame {i+1} de {framemax} feito e salvo com sucesso!")
        tatual = round(tatual + dt*intervalo, int(-np.log10(dt*intervalo) + 3))

#endregion