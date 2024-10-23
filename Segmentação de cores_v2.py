import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#   O código abaixo recebe duas imagens de verduras, descarto o fundo e realiza comparação da intensidade lab de cada uma
#   Funciona para extensões .jpg, .jpeg, .png, .pdf

#   Recebe das imagens
img1 = cv.imread("exemplo1.jpg")
img2 = cv.imread("exemplo2.jpg")

#   Copia das imagens para futura edicao
img1_cp = img1.copy()  # copia da imagem 1
img2_cp = img2.copy()  # copia da imagem 2

#   Obtem dimensao das imagens
altura1,largura1,canais1 = np.shape(img1)
altura2,largura2,canais2 = np.shape(img2)

#   Transforma imagem do espaço BGR em HSV
hsv1 = cv.cvtColor(img1, cv.COLOR_BGR2HSV)
hsv2 = cv.cvtColor(img2, cv.COLOR_BGR2HSV)

#   Define faixas de cores a serem mantidas na imagem

        # Faixa superior e inferior de verde claro
lowerVc = np.array([35, 60,130])
upperVc = np.array([70, 255, 255])

        # Faixa superior e inferior de verde escuro
lowerVe = np.array([35, 60,35])
upperVe = np.array([70, 255, 130])

        # Faixa superior e inferior de amarelo
lowerAmc = np.array([25,80, 100])
upperAmc = np.array([35, 255, 255])

        # Faixa superior e inferior de marrom
lowerMar = np.array([25, 80, 30])
upperMar = np.array([35, 255, 100])

#   Cria mascaras de cada faixa de cor para imagem 1 e 2
maskVc1 = cv.inRange(hsv1, lowerVc, upperVc)          # Faixa de verde claro
maskAmc1 = cv.inRange(hsv1, lowerAmc, upperAmc)       # Faixa de amarelo
maskVe1 = cv.inRange(hsv1, lowerVe, upperVe)          # Faixa de verde escuro
maskMar1 = cv.inRange(hsv1, lowerMar, upperMar)       # Faixa de marrom
maskVc2 = cv.inRange(hsv2, lowerVc, upperVc)
maskAmc2 = cv.inRange(hsv2, lowerAmc, upperAmc)
maskVe2 = cv.inRange(hsv2, lowerVe, upperVe)
maskMar2 = cv.inRange(hsv2, lowerMar, upperMar)

# Junta todas as faixas em uma máscara total
maskUtil1 = maskVe1 + maskVc1 + maskAmc1 + maskMar1
maskUtil2 = maskVe2 + maskVc2 + maskAmc2 + maskMar2

'''
countVc = 0
countAmc = 0
countVe = 0
countMar = 0
for i in range(0,altura1):
    for j in range(0,largura1):
        # O bloco abaixo é responsável por colorir as máscaras criadas acima, com o intuito de visualização das faixas
        # Mesmo trabalhando com o espaço de cor HSV, as cores indicadas entre chaves são em RGB
        # as variáveis cont<cor> são usadas para contar quantidade de pixeis de cada faixa para possível cálculo de porcentagem
        if maskVc[i][j] != 0:
            hsv[i][j] = [57,255,20]
            countVc += 1
        elif maskAmc[i][j] != 0:
            hsv[i][j] = [255,255,0]
            countAmc += 1
        elif maskMar[i][j] != 0:
            hsv[i][j] = [150,75,0]
            countMar += 1
        elif maskVe[i][j] != 0:
            hsv[i][j] = [50, 100, 50]
            countVe += 1
        # Elimina tudo na imagem que não está dentro das faixas detectadas (pinta fundo de preto)
        if maskUtil[i][j] == 0:
            img1_cp[i][j] = [0,0,0]
'''

#   Conta os pixeis uteis da imagem (verdura, sem o fundo preto)
#n_pixels_uteis = countVc + countVe + countAmc + countMar

#   Mostra as imagens: original, mascaras de cada cor e por ultima, a soma das mascaras
#cv.imshow("Image", img1)
#cv.imshow("MaskVc", maskVc)
#cv.imshow("MaskAmc", maskAmc)
#cv.imshow("MaskVe", maskVe)
#cv.imshow("MaskMar", maskMar)
#cv.imshow("maskUtil", maskUtil)

#   Calculo da porcentagem de cada faixa
'''
porcVerde_claro = (countVc/n_pixels_uteis)*100
porcVerde_escuro = (countVe/n_pixels_uteis)*100
porcAmarelo_claro = (countAmc/n_pixels_uteis)*100
porcMarrom = (countMar/n_pixels_uteis)*100
'''

#   Printa na tela a porcentagem de cada faixa
'''
print(" A figura apresenta {:.2f}% de Verde claro ".format(porcVerde_claro))
print(" A figura apresenta {:.2f}% de Verde escuro ".format(porcVerde_escuro))
print(" A figura apresenta {:.2f}% de Amarelo ".format(porcAmarelo_claro))
print(" A figura apresenta {:.2f}% de Marrom ".format(porcMarrom))
'''

# A partir daqui, sera feita analise LAB das imagens

# Convertendo as imagens para o espaço de cores LAB
img1_lab = cv.cvtColor(img1, cv.COLOR_BGR2LAB)
img2_lab = cv.cvtColor(img2, cv.COLOR_BGR2LAB)

# Separando os canais L, a e b das imagens
l1, a1, b1 = cv.split(img1_lab)
l2, a2, b2 = cv.split(img2_lab)

#   Calcula medias dos valores de L, a e b da imagem 1
countUtil = 0
l1_mean = 0
a1_mean = 0
b1_mean = 0
for i in range(0,altura1):
    for j in range(0,largura1):
        # Utiliza apenas pixels dentro das faixas uteis para contabilizar média dos valores de L,a e b
        if maskUtil1[i][j] != 0:
            l1_mean += l1[i][j]
            a1_mean += a1[i][j]
            b1_mean += b1[i][j]
            countUtil += 1
        #   Gera imagem sem fundo -> funcao apenas grafica
        else:
            img1_cp[i][j] = [0,0,0]
l1_mean = l1_mean/countUtil
a1_mean = a1_mean/countUtil
b1_mean = b1_mean/countUtil

#   Calcula o desvio padrão dos valores de L, a e b da imagem 1

l1_dp = 0
a1_dp = 0
b1_dp = 0

for i in range(0,altura1):
    for j in range(0,largura1):
        # Utiliza apenas pixels dentro das faixas uteis para contabilizar média dos valores de L,a e b
        if maskUtil1[i][j] != 0:
            l1_dp += (l1[i][j] - l1_mean)^2
            a1_dp += (a1[i][j] - a1_mean)^2
            b1_dp += (b1[i][j] - b1_mean)^2
        l1_dp = sqrt(l1_dp/countUtil)
        a1_dp = sqrt(a1_dp/countUtil)
        b1_dp = sqrt(b1_dp/countUtil)

#   Calcula medias dos valores de L, a e b da imagem 2
countUtil = 0
l2_mean = 0
a2_mean = 0
b2_mean = 0
for i in range(0,altura2):
    for j in range(0,largura2):
        if maskUtil2[i][j] != 0:
            l2_mean += l1[i][j]
            a2_mean += a1[i][j]
            b2_mean += b1[i][j]
            countUtil += 1
        else:
            img2_cp[i][j] = [0,0,0]
l2_mean = l2_mean/countUtil
a2_mean = a2_mean/countUtil
b2_mean = b2_mean/countUtil

#   Calcula o desvio padrão dos valores de L, a e b da imagem 2

l2_dp = 0
a2_dp = 0
b2_dp = 0
for i in range(0,altura2):
    for j in range(0,largura2):
        # Utiliza apenas pixels dentro das faixas uteis para contabilizar média dos valores de L,a e b
        if maskUtil1[i][j] != 0:
            l2_dp += (l1[i][j] - l2_mean)^2
            a2_dp += (a1[i][j] - a2_mean)^2
            b2_dp += (b1[i][j] - b2_mean)^2
        l2_dp = sqrt(l2_dp/countUtil)
        a2_dp = sqrt(a2_dp/countUtil)
        b2_dp = sqrt(b2_dp/countUtil)


# Calculando as diferenças médias entre os canais das duas imagens
diff_l = abs(l1_mean - l2_mean)
diff_a = abs(a1_mean - a2_mean)
diff_b = abs(b1_mean - b2_mean)

# Imprimindo os resultados
print("Canal\t\tMédia\t\tDesvio padrão\t\t\n-------------------------------")
print("Diferença média no canal L: {:.2f}".format(diff_l))
print("Diferença média no canal a: {:.2f}".format(diff_a))
print("Diferença média no canal b: {:.2f}".format(diff_b))

f, axs = plt.subplots(2,3)
axs[0,0].imshow(img1)
axs[0,0].axis("off")

axs[0,1].imshow(img1_cp)
axs[0,1].axis("off")

axs[0,2].imshow(img1_lab)
axs[0,2].axis("off")

axs[1,0].imshow(img2)
axs[1,0].axis("off")

axs[1,1].imshow(img2_cp)
axs[1,1].axis("off")

axs[1,2].imshow(img2_lab)
axs[1,2].axis("off")

plt.show()

cv.waitKey(0)
