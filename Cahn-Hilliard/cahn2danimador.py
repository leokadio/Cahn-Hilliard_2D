import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

codigo = (
#DIGITE O CÓDIGO AQUI
3427
)
fpss = (
#FRAMESPORSEGUNDO
10
)
frameskipper = (
#USAR SÓ FRAMES DE N em N, DESCARTA OS QUE SOBRAM NO FINAL
600
)
pbc = (
#SIM PRA PLOTAR UMA GRADE 3x3 DE GRÁFICOS, NAO PRO NORMAL
"SIM"
)
pixelxpixel = (
#NUMERO DA RESOLUCAO DE 1 GRAFICO, VAI SER TRIPLICADO PARA PBC
#RECOMENDO 128 OU 256 QUANDO FAZENDO SEM PBC, E 256 OU 512 COM PBC
128
)
colormapp = (
#ESCOLHER CORES NO SITE https://matplotlib.org/stable/tutorials/colors/colormaps.html#diverging
"Spectral"
)
tmax = (
#TEMPO MAXIMO PRA LIMITAR COMPRIMENTO DO GIF, BOTAR VALOR MAIOR QUE O TEMPO DO ARQUIVO PRA FAZER COMPLETO
10
)
#DAQUI PRA BAIXO MELHOR NÃO MEXER

#region leitura dos arquivos
valores = np.load(f".\\{codigo}\\val{codigo}.npy")

normalizar, mediadesejada, seed,        gamma,      difd,       intervalo,  xmax,       t,          dt,         dx = (
valores[0], valores[1],    valores[2],  valores[3], valores[4], valores[5], valores[6], valores[7], valores[8], valores[9])

cc = np.load(f".\\{codigo}\\{codigo}.npy")

print(f"Array achado e carregado!")

#endregion

#region fazer gif solitário
if pbc == "NAO":
    fig, ax = plt.subplots()

    fig.set_size_inches(1, 1)

    ax.axis('off')

    plt.subplots_adjust(0, 0, 1, 1, wspace = None, hspace = None)

    ims = []

    tatual = 0
    if frameskipper == 0:
        for c in cc:
            im = ax.imshow(c, aspect = "equal", cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
            texto = ax.annotate(f"Tempo atual: {tatual:.5f}",(10, 100),  color = "white", fontsize = 4.5, bbox=dict(facecolor='blue', alpha=0.3)) # add text
            ims.append([im, texto])
            tatual = round(tatual + dt*intervalo, int(-np.log10(dt*intervalo) + 3))
            if tatual > tmax:
                break
    else: 
        for i in range(int((len(cc)/frameskipper) + 1)):
            im = ax.imshow(cc[int(i*(frameskipper))], aspect = "equal", cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
            texto = ax.annotate(f"Tempo atual: {tatual:.5f}",(10, 100),  color = "white", fontsize = 4.5, bbox=dict(facecolor='blue', alpha=0.3)) # add text
            ims.append([im, texto])
            tatual = round(tatual + frameskipper*dt*intervalo, int(-np.log10(dt*intervalo) + 3))
            if tatual > tmax:
                break
    ani = animation.ArtistAnimation(fig, ims, interval = 1/fpss, blit=True)

    ani.save(f'.\\{codigo}\\{codigo}fskip{frameskipper}.gif', fps = fpss, dpi = pixelxpixel)
    print("Animação salva em gif na pasta!")
#endregion

#region gif pbc
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

    ims = []

    tatual = 0
    if frameskipper == 0:
        for c in cc:
            im1 = ax1.imshow(c, cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
            im2 = ax2.imshow(c, cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
            im3 = ax3.imshow(c, cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
            im4 = ax4.imshow(c, cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
            im5 = ax5.imshow(c, cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
            im6 = ax6.imshow(c, cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
            im7 = ax7.imshow(c, cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
            im8 = ax8.imshow(c, cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
            im9 = ax9.imshow(c, cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
            texto = ax5.annotate(f"Tempo atual: {tatual:.5f}",(10, 100),  color = "white", fontsize=3, bbox=dict(facecolor='blue', alpha=0.3)) # add text
            ims.append([im1, im2, im3, im4, im5, im6, im7, im8, im9, texto])
            tatual = round(tatual + dt*intervalo, int(-np.log10(dt*intervalo) + 3))
            if tatual > tmax:
                break
    else: 
        for i in range(int((len(cc)/frameskipper) + 1)):
            im1 = ax1.imshow(cc[int(i*(frameskipper))], cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
            im2 = ax2.imshow(cc[int(i*(frameskipper))], cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
            im3 = ax3.imshow(cc[int(i*(frameskipper))], cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
            im4 = ax4.imshow(cc[int(i*(frameskipper))], cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
            im5 = ax5.imshow(cc[int(i*(frameskipper))], cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
            im6 = ax6.imshow(cc[int(i*(frameskipper))], cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
            im7 = ax7.imshow(cc[int(i*(frameskipper))], cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')   
            im8 = ax8.imshow(cc[int(i*(frameskipper))], cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
            im9 = ax9.imshow(cc[int(i*(frameskipper))], cmap = colormapp, vmin = -1, vmax = 1, interpolation = 'none')
            texto = ax5.annotate(f"Tempo atual: {tatual:.5f}",(10, 100),  color = "white", fontsize=3, bbox=dict(facecolor='blue', alpha=0.3)) # add text
            ims.append([im1, im2, im3, im4, im5, im6, im7, im8, im9, texto])
            tatual = round(tatual + frameskipper*dt*intervalo, int(-np.log10(dt*intervalo) + 3))
            if tatual > tmax:
                break
    ani = animation.ArtistAnimation(fig, ims, interval = 1/fpss, blit=True)
    print("Salvando...")
    ani.save(f'.\\{codigo}\\{codigo}fskip{frameskipper}pbc.gif', fps = fpss, dpi = pixelxpixel*3/2)
    print("Animação salva em gif na pasta!")
#endregion