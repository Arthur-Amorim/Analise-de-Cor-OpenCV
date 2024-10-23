import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os

#   O código abaixo recebe duas imagens de verduras,
#   descarto o fundo e realiza comparação da intensidade lab de cada uma
#   Funciona para extensões .jpg, .jpeg, .png, .pdf

# Esta versão corta o fundo da imagem deixando apenas verde, amarelo e marrom

def entrada():
    print("COLORIMETRO\n")
    print("Para dar prosseguimento à utilização do programa, escolha uma das opções abaixo:")
    print("1 - Instruções\n2 - Utilize o programa\n3 - Sair\n")
    opcao_bruta = input("Digito escolhido: ")
    opcao = opcao_bruta
    os.system('cls')

    while opcao not in [2,'2']:

        if opcao_bruta.isnumeric():
            opcao = int(opcao_bruta.strip())
        else:
            opcao = 0

        if opcao in [1, 3]:
            if opcao == 1:
                print("Para que o programa funcione adequadamente, siga as seguintes etapas:")
                print("1) Tire duas foto do vegetal que quer analisar")
                print(
                    "\n- As duas imagens devem possuir as mesmas características (dimensão, ângulo, ambiente de fundo, etc), logo, faça o procedimento de forma mais padrão possível. Opte por imagens com o fundo igual, de preferencia com o fundo preto ou branco")
                print(
                    "- OBS: Caso o ambiente possua tons verdes, amarelos ou marrons, a imagem analisada pode confundir a verdura com tons do ambiente\n")
                print("2) Deixe o programa na mesma pasta que as imagens a serem analisadas\n")
                print(
                    "3) Saiba as extensões das imagens analisadas. O programa funciona para as extensões .jpg, .jpeg, .png e .pdf\n")
                print(
                    "4) Execute o programa e indique o nome da imagem a ser analisada, de acordo com o exemplo:\n\tEXEMPLO1: manjericao_antes.jpg\n\tEXEMPLO2: manjericao_depois.png")
                input("Insira qualquer coisa para continuar e executar o programa:")
                os.system('cls')
                opcao = 2
            else:
                exit()
        else:
            print("Você não digitou um valor válido, por favor, escolha uma das opções abaixo:")
            print("1 - Instruções\n2 - Utilize o programa\n3 - Sair\n")
            opcao_bruta = input("Digito escolhido:")
            os.system('cls')

def limpar_terminal():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix/Linux/Mac
        os.system('clear')

#   Calcula medias dos valores de L, a e b da imagem 1
def calcular_stats(imagem_lab, mascara):
    l, a, b = cv.split(imagem_lab)
    pixels_validos = cv.findNonZero(mascara)

    l_raw = l[pixels_validos[:, 0, 1], pixels_validos[:, 0, 0]]
    l_validos = np.interp(l_raw, (0, 255), (0, 100)).astype(np.int32)

    a_raw = a[pixels_validos[:, 0, 1], pixels_validos[:, 0, 0]]
    a_validos = np.interp(a_raw , (0, 255), (-128, 127)).astype(np.int32)

    b_raw = b[pixels_validos[:, 0, 1], pixels_validos[:, 0, 0]]
    b_validos = np.interp(b_raw, (0, 255), (-128, 127)).astype(np.int32)

    l_mean = np.mean(l_validos)
    a_mean = np.mean(a_validos)
    b_mean = np.mean(b_validos)
    l_dp = np.std(l_validos)
    a_dp = np.std(a_validos)
    b_dp = np.std(b_validos)
    return l_mean, l_dp, a_mean, a_dp, b_mean, b_dp

# Imprimindo os resultados
def tabela(l_mean, l_dp, a_mean, a_dp, b_mean, b_dp):
    print("\tCanal\t\tMédia\t\tDesvio padrão")
    print("\t  L\t\t\t{:.2f}\t\t{:.2f}\t\t".format(l_mean, l_dp))
    print("\t  a\t\t\t{:.2f}\t\t{:.2f}\t\t".format(a_mean, a_dp))
    print("\t  b\t\t\t{:.2f}\t\t{:.2f}\t\t\n".format(b_mean, b_dp))


def main():
    str_img1 = input("Nome da primeira imagem:")
    str_img2 = input("Nome da segunda imagem:")
    print("")
    os.system('cls')

    #   Recebe das imagens
    img1 = cv.imread(str_img1)
    img2 = cv.imread(str_img2)

    #   Copia das imagens para futura edicao
    img1_cp = img1.copy()  # copia da imagem 1
    img2_cp = img2.copy()  # copia da imagem 2

    #   Transforma imagem do espaço BGR em HSV
    hsv1 = cv.cvtColor(img1, cv.COLOR_BGR2HSV)
    hsv2 = cv.cvtColor(img2, cv.COLOR_BGR2HSV)

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

    # Cria mascaras de cada faixa de cor para imagem 1 e 2
    maskVc1 = cv.inRange(hsv1, lowerVc, upperVc)  # Faixa de verde claro
    maskAmc1 = cv.inRange(hsv1, lowerAmc, upperAmc)  # Faixa de amarelo
    maskVe1 = cv.inRange(hsv1, lowerVe, upperVe)  # Faixa de verde escuro
    maskMar1 = cv.inRange(hsv1, lowerMar, upperMar)  # Faixa de marrom
    maskVc2 = cv.inRange(hsv2, lowerVc, upperVc)
    maskAmc2 = cv.inRange(hsv2, lowerAmc, upperAmc)
    maskVe2 = cv.inRange(hsv2, lowerVe, upperVe)
    maskMar2 = cv.inRange(hsv2, lowerMar, upperMar)

    # Junta todas as faixas em uma máscara total
    maskUtil1 = maskVe1 + maskVc1 + maskAmc1 + maskMar1
    maskUtil2 = maskVe2 + maskVc2 + maskAmc2 + maskMar2

    # Cria imagem sem o fundo
    img1_cp[np.where(maskUtil1 == 0)] = 0
    img2_cp[np.where(maskUtil2 == 0)] = 0

    # Cria imagem LAB sem o fundo
    img1_lab_cut = cv.cvtColor(img1_cp, cv.COLOR_BGR2LAB)
    img2_lab_cut = cv.cvtColor(img2_cp, cv.COLOR_BGR2LAB)

    # A partir daqui, sera feita analise LAB das imagens

    # Convertendo as imagens para o espaço de cores LAB
    img1_lab = cv.cvtColor(img1, cv.COLOR_BGR2LAB)
    img2_lab = cv.cvtColor(img2, cv.COLOR_BGR2LAB)

    l1_mean, l1_dp, a1_mean, a1_dp, b1_mean, b1_dp = calcular_stats(img1_lab, maskUtil1)
    l2_mean, l2_dp, a2_mean, a2_dp, b2_mean, b2_dp = calcular_stats(img2_lab, maskUtil2)

    # Calculando as diferenças médias entre os canais das duas imagens
    diff_l = abs(l1_mean - l2_mean)
    diff_a = abs(a1_mean - a2_mean)
    diff_b = abs(b1_mean - b2_mean)

    print("\tDados da imagem 1")
    tabela(l1_mean, l1_dp, a1_mean, a1_dp, b1_mean, b1_dp)
    print("\tDados da imagem 2")
    tabela(l2_mean, l2_dp, a2_mean, a2_dp, b2_mean, b2_dp)
    print("A diferença entre os canais L,a e b são respectivamente: {:.2f}; {:.2f}; {:.2f}.".format(diff_l, diff_a, diff_b))

    f, axs = plt.subplots(2, 3)
    axs[0, 0].imshow(img1)
    axs[0, 0].axis("off")
    axs[0, 1].imshow(img1_lab)
    axs[0, 1].axis("off")
    axs[0, 2].imshow(img1_lab_cut)
    axs[0, 2].axis("off")
    axs[1, 0].imshow(img2)
    axs[1, 0].axis("off")
    axs[1, 1].imshow(img2_lab)
    axs[1, 1].axis("off")
    axs[1, 2].imshow(img2_lab_cut)
    axs[1, 2].axis("off")
    plt.show()
    cv.waitKey(0)
    return 0

entrada()
main()

