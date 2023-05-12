import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


img = cv.imread("exemplo1.jpg")
altura,largura,canais = np.shape(img)
scale = altura/largura
altura_n = 700
largura_n = altura_n / scale


hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

lowerVc = np.array([35, 60,130])
upperVc = np.array([70, 255, 255])
#
lowerVe = np.array([35, 60,35])
upperVe = np.array([70, 255, 130])
#
lowerAmc = np.array([25,80, 100])
upperAmc = np.array([35, 255, 255])
#
lowerMar = np.array([25, 80, 30])
upperMar = np.array([35, 255, 100])
#
maskVc = cv.inRange(hsv, lowerVc, upperVc)
maskAmc = cv.inRange(hsv, lowerAmc, upperAmc)
maskVe = cv.inRange(hsv, lowerVe, upperVe)
maskMar = cv.inRange(hsv, lowerMar, upperMar)
maskUtil = maskVe + maskVc + maskAmc + maskMar
#colorida = cv.cvtColor(maskUtil, cv.COLOR_BGR2HSV)

countVc = 0
countAmc = 0
countVe = 0
countMar = 0

for i in range(0,altura):
    for j in range(0,largura):
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
        else:
            hsv[i][j] = [0,0,0]

hsv_padrao = cv.resize(hsv,(int(largura_n),int(altura_n)))


n_pixels_uteis = countVc + countVe + countAmc + countMar

#cv.imshow("Image", hsv_padrao)
#cv.imshow("MaskVc", maskVc)
#cv.imshow("MaskAmc", maskAmc)
#cv.imshow("MaskVe", maskVe)
#cv.imshow("MaskMar", maskMar)
#cv.imshow("maskUtil", maskUtil)

porcVerde_claro = (countVc/n_pixels_uteis)*100
porcVerde_escuro = (countVe/n_pixels_uteis)*100
porcAmarelo_claro = (countAmc/n_pixels_uteis)*100
porcMarrom = (countMar/n_pixels_uteis)*100

print(" A figura apresenta {:.2f}% de Verde claro ".format(porcVerde_claro))
print(" A figura apresenta {:.2f}% de Verde escuro ".format(porcVerde_escuro))
print(" A figura apresenta {:.2f}% de Amarelo ".format(porcAmarelo_claro))
print(" A figura apresenta {:.2f}% de Marrom ".format(porcMarrom))

f, axs = plt.subplots(1,2)
axs[0].imshow(img)
axs[0].axis("off")
axs[1].imshow(hsv_padrao)
axs[1].axis("off")

#axs[1].legend(color = ([0,0,0],[1,1,1],[2,2,2],[3,3,3]), label = ("tes","te","to","mate"), bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )

plt.show()

cv.waitKey(0)


