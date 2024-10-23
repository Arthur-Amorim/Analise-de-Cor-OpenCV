import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import statistics as stcs

# Função para calcular média e desvio padrão dos pixels dentro das máscaras
def calcular_stats(imagem_lab, mascara):
    l, a, b = cv.split(imagem_lab)
    pixels_validos = cv.findNonZero(mascara)
    l_validos = l[pixels_validos[:, 0, 1], pixels_validos[:, 0, 0]]
    a_validos = a[pixels_validos[:, 0, 1], pixels_validos[:, 0, 0]]
    b_validos = b[pixels_validos[:, 0, 1], pixels_validos[:, 0, 0]]
    l_mean = np.mean(l_validos)
    a_mean = np.mean(a_validos)
    b_mean = np.mean(b_validos)
    l_dp = np.std(l_validos)
    a_dp = np.std(a_validos)
    b_dp = np.std(b_validos)
    return l_mean, l_dp, a_mean, a_dp, b_mean, b_dp

# Carregar as imagens
img1 = cv.imread("exemplo2.jpg")
img2 = cv.imread("exemplo1.jpg")

# Redimensionar as imagens (opcional)
# img1 = cv.resize(img1, (largura_desejada, altura_desejada))
# img2 = cv.resize(img2, (largura_desejada, altura_desejada))

# Converter as imagens para o espaço de cores HSV
hsv1 = cv.cvtColor(img1, cv.COLOR_BGR2HSV)
hsv2 = cv.cvtColor(img2, cv.COLOR_BGR2HSV)

# Definir faixas de cores
lowerVc = np.array([35, 60, 130])
upperVc = np.array([70, 255, 255])
lowerVe = np.array([35, 60, 35])
upperVe = np.array([70, 255, 130])
lowerAmc = np.array([25, 80, 100])
upperAmc = np.array([35, 255, 255])
lowerMar = np.array([25, 80, 30])
upperMar = np.array([35, 255, 100])

# Criar as máscaras
maskVc1 = cv.inRange(hsv1, lowerVc, upperVc)
maskAmc1 = cv.inRange(hsv1, lowerAmc, upperAmc)
maskVe1 = cv.inRange(hsv1, lowerVe, upperVe)
maskMar1 = cv.inRange(hsv1, lowerMar, upperMar)
maskVc2 = cv.inRange(hsv2, lowerVc, upperVc)
maskAmc2 = cv.inRange(hsv2, lowerAmc, upperAmc)
maskVe2 = cv.inRange(hsv2, lowerVe, upperVe)
maskMar2 = cv.inRange(hsv2, lowerMar, upperMar)

# Criar máscara total
maskUtil1 = maskVe1 + maskVc1 + maskAmc1 + maskMar1
maskUtil2 = maskVe2 + maskVc2 + maskAmc2 + maskMar2

# Converter as imagens para o espaço de cores LAB
img1_lab = cv.cvtColor(img1, cv.COLOR_BGR2LAB)
img2_lab = cv.cvtColor(img2, cv.COLOR_BGR2LAB)

# Calcular estatísticas das imagens
l1_mean, l1_dp, a1_mean, a1_dp, b1_mean, b1_dp = calcular_stats(img1_lab, maskUtil1)
l2_mean, l2_dp, a2_mean, a2_dp, b2_mean, b2_dp = calcular_stats(img2_lab, maskUtil2)

# Calcular as diferenças médias entre os canais das duas imagens
diff_l = abs(l1_mean - l2_mean)
diff_a = abs(a1_mean - a2_mean)
diff_b = abs(b1_mean - b2_mean)

# Imprimir os resultados
print("\tDados da imagem 1")
print("\tCanal\t\tMédia\t\tDesvio padrão\n")
print("\t  L\t\t\t{:.2f}\t\t{:.2f}\t\t".format(l1_mean, l1_dp))
print("\t  a\t\t\t{:.2f}\t\t{:.2f}\t\t".format(a1_mean, a1_dp))
print("\t  b\t\t\t{:.2f}\t\t{:.2f}\t\t\n".format(b1_mean, b1_dp))
print("\tDados da imagem 2")
print("\tCanal\t\tMédia\t\tDesvio padrão\n")
print("\t  L\t\t\t{:.2f}\t\t{:.2f}\t\t".format(l2_mean, l2_dp))
print("\t  a\t\t\t{:.2f}\t\t{:.2f}\t\t".format(a2_mean, a2_dp))
print("\t  b\t\t\t{:.2f}\t\t{:.2f}\t\t\n".format(b2_mean, b2_dp))
print("A diferença entre os canais L, a e b são: {:.2f}, {:.2f} e {:.2f}.".format(diff_l, diff_a, diff_b))

# Exibir as imagens
f, axs = plt.subplots(2, 3)
axs[0, 0].imshow(cv.cvtColor(img1, cv.COLOR_BGR2RGB))
axs[0, 0].axis("off")
axs[0, 1].imshow(cv.cvtColor(img1_lab, cv.COLOR_LAB2RGB))
axs[0, 1].axis("off")
axs[0, 2].imshow(cv.cvtColor(maskUtil1, cv.COLOR_GRAY2RGB))
axs[0, 2].axis("off")
axs[1, 0].imshow(cv.cvtColor(img2, cv.COLOR_BGR2RGB))
axs[1, 0].axis("off")
axs[1, 1].imshow(cv.cvtColor(img2_lab, cv.COLOR_LAB2RGB))
axs[1, 1].axis("off")
axs[1, 2].imshow(cv.cvtColor(maskUtil2, cv.COLOR_GRAY2RGB))
axs[1, 2].axis("off")
plt.show()
cv.waitKey(0)
