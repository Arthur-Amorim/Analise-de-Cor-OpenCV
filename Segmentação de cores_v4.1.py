import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import statistics as stcs
import os


def limpar_terminal():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix/Linux/Mac
        os.system('clear')

def escala_255_100(valor):
    return int(valor * (100/ 255));

def escala_255_128(valor):
    return int((valor - 127.5) * (127 / 127.5));

def main():

    #   Recebe das imagens
    img1 = cv.imread("maca.PNG")

    # Convertendo as imagens para o espaço de cores LAB
    imagem_lab = cv.cvtColor(img1, cv.COLOR_BGR2LAB)
    l, a, b = cv.split(imagem_lab)
    l_mean_raw = np.mean(l)
    a_mean_raw = np.mean(a)
    b_mean_raw = np.mean(b)

    l_mean = escala_255_100(l_mean_raw)
    a_mean = escala_255_128(a_mean_raw)
    b_mean = escala_255_128(b_mean_raw)

    print("Média do canal L: {}\nMédia do canal a: {}\nMédia do canal b: {}".format(l_mean,a_mean,b_mean))

main()

