import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os


def main():
    #   Recebe das imagens
    str_img1 = input("Insira o nome da imagem a ser analisada: ")
    img1 = cv.imread(str_img1)

    #   Copia das imagens para futura edicao
    img1_cp = img1.copy()  # copia da imagem 1

    #   Transforma imagem do espaço BGR em HSV
    hsv1 = cv.cvtColor(img1, cv.COLOR_BGR2HSV)

    # Faixa superior e inferior de verde claro
    lowerVc = np.array([35, 60, 130])
    upperVc = np.array([70, 255, 255])
    # Faixa superior e inferior de verde escuro
    lowerVe = np.array([35, 60, 35])
    upperVe = np.array([70, 255, 130])
    # Faixa superior e inferior de amarelo
    lowerAmc = np.array([25, 80, 100])
    upperAmc = np.array([35, 255, 255])
    # Faixa superior e inferior de marrom
    lowerMar = np.array([25, 80, 30])
    upperMar = np.array([35, 255, 100])
    # Faixa superior e inferior de branco
    lowerBra = np.array([0, 0, 60])
    upperBra = np.array([255, 100, 255])

    # Cria mascaras de cada faixa de cor para imagem 1
    maskVc1 = cv.inRange(hsv1, lowerVc, upperVc)  # Faixa de verde claro
    maskAmc1 = cv.inRange(hsv1, lowerAmc, upperAmc)  # Faixa de amarelo
    maskVe1 = cv.inRange(hsv1, lowerVe, upperVe)  # Faixa de verde escuro
    maskMar1 = cv.inRange(hsv1, lowerMar, upperMar)  # Faixa de marrom
    maskBra1 = cv.inRange(hsv1, lowerBra, upperBra)  # Faixa de marrom


    # Junta todas as faixas em uma máscara total
    maskUtil1 = maskBra1

    # Cria imagem sem o fundo
    img1_cp[np.where(maskUtil1 == 0)] = 0

    cv.imshow("Imagem original", img1)
    cv.imshow("Imagem cortada",img1_cp)
    cv.waitKey(0)

    return 0;

main()

