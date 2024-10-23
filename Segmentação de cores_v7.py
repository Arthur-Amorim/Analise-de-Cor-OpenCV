import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
import csv

# Esta versão não faz tratamento de imagem, apenas extrai os valores
# brutos médios dos canais Lab de uma imagemp

def tabela(l_mean, l_dp, a_mean, a_dp, b_mean, b_dp):
    # Imprimindo os resultados em uma tabela no terminal

    print("\tCanal\t\tMédia\t\tDesvio padrão")
    print("\t  L\t\t\t{:.2f}\t\t{:.2f}\t\t".format(l_mean, l_dp))
    print("\t  a\t\t\t{:.2f}\t\t{:.2f}\t\t".format(a_mean, a_dp))
    print("\t  b\t\t\t{:.2f}\t\t{:.2f}\t\t\n".format(b_mean, b_dp))

str_img1 = input("Nome da primeira imagem:")
os.system('cls')

#   Recebe das imagens
img1 = cv.imread(str_img1)

#   Copia das imagens para futura edicao
img1_cp = img1.copy()  # copia da imagem 1

# Cria imagem LAB sem o fundo
img1_lab_cut = cv.cvtColor(img1_cp, cv.COLOR_BGR2LAB)

# A partir daqui, sera feita analise LAB das imagens

# Convertendo as imagens para o espaço de cores LAB
img1_lab = cv.cvtColor(img1, cv.COLOR_BGR2LAB)

l, a, b = cv.split(img1_lab)

l = np.interp(l, (0, 255), (0, 100)).astype(np.int32)

a = np.interp(a, (0, 255), (-128, 128)).astype(np.int32)

b = np.interp(b, (0, 255), (-128, 128)).astype(np.int32)

l_mean = np.mean(l)
a_mean = np.mean(a)
b_mean = np.mean(b)
l_dp = np.std(l)
a_dp = np.std(a)
b_dp = np.std(b)

print("\tDados da imagem 1")
tabela(l_mean, l_dp, a_mean, a_dp, b_mean, b_dp)




