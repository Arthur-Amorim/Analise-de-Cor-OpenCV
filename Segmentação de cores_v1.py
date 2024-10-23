import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

#   O código abaixo recebe duas imagens de verduras, descarta o fundo identifica faixas de cores indicadas
#   Funciona para extensões .jpg, .jpeg, .png, .pdf

#   Recebe das imagens
img1 = cv.imread("exemplo1.jpg")

#   Copia das imagens para futura edicao
img1_cp = img1.copy()  # copia da imagem 1

#   Obtem dimensao das imagens
altura1,largura1,canais1 = np.shape(img1)

#   Transforma imagem do espaço BGR em HSV
hsv1 = cv.cvtColor(img1, cv.COLOR_BGR2HSV)

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
maskVc = cv.inRange(hsv1, lowerVc, upperVc)          # Faixa de verde claro
maskAmc = cv.inRange(hsv1, lowerAmc, upperAmc)       # Faixa de amarelo
maskVe = cv.inRange(hsv1, lowerVe, upperVe)          # Faixa de verde escuro
maskMar = cv.inRange(hsv1, lowerMar, upperMar)       # Faixa de marrom

# Junta todas as faixas em uma máscara total
maskUtil1 = maskVe + maskVc + maskAmc + maskMar

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
            img1_cp[i][j] = [57,255,20]
            countVc += 1
        elif maskAmc[i][j] != 0:
            img1_cp[i][j] = [255,255,0]
            countAmc += 1
        elif maskMar[i][j] != 0:
            img1_cp[i][j] = [150,75,0]
            countMar += 1
        elif maskVe[i][j] != 0:
            img1_cp[i][j] = [50, 100, 50]
            countVe += 1
        # Elimina tudo na imagem que não está dentro das faixas detectadas (pinta fundo de preto)
        else:
            img1_cp[i][j] = [0,0,0]

#   Conta os pixeis uteis da imagem (verdura, sem o fundo preto)
n_pixels_uteis = countVc + countVe + countAmc + countMar

#   Calculo da porcentagem de cada faixa

porcVerde_claro = (countVc/n_pixels_uteis)*100
porcVerde_escuro = (countVe/n_pixels_uteis)*100
porcAmarelo_claro = (countAmc/n_pixels_uteis)*100
porcMarrom = (countMar/n_pixels_uteis)*100

#   Printa na tela a porcentagem de cada faixa

print(" A figura apresenta {:.2f}% de Verde claro ".format(porcVerde_claro))
print(" A figura apresenta {:.2f}% de Verde escuro ".format(porcVerde_escuro))
print(" A figura apresenta {:.2f}% de Amarelo ".format(porcAmarelo_claro))
print(" A figura apresenta {:.2f}% de Marrom ".format(porcMarrom))


f, axs = plt.subplots(1,2)
axs[0].imshow(img1)
axs[0].axis("off")

axs[1].imshow(img1_cp)
axs[1].axis("off")

plt.show()
cv.waitKey(0)




