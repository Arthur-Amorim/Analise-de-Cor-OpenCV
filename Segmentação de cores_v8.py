import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
import csv

def main():
    # O código abaixo recebe n imagens de uma pasta,
    # descarta o fundo branco e realiza comparação da intensidade LAB de cada uma
    # Funciona para extensões .jpg, .jpeg, .png, .pdf

    # Esta versão corta o fundo da imagem branco

    folder_path = input("Caminho da pasta das imagens:")
    image_files = os.listdir(folder_path)
    print("")
    os.system('cls')

    for image_file in image_files:
        # Recebe as imagens
        image_path = os.path.join(folder_path, image_file)
        img = cv.imread(image_path)

        # Copia da imagem para futura edição
        img_cp = img.copy()

        # Transforma imagem do espaço BGR em HSV
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        # Faixa superior e inferior de branco
        lowerBra = np.array([0, 0, 60])
        upperBra = np.array([255, 100, 255])

        # Cria máscara de faixa de cor para a imagem
        maskBra = cv.inRange(hsv, lowerBra, upperBra)

        maskUtil = cv.bitwise_not(maskBra)

        # Cria imagem sem o fundo
        img_cp[np.where(maskUtil == 0)] = 0

        # Cria imagem LAB sem o fundo
        img_lab_cut = cv.cvtColor(img_cp, cv.COLOR_BGR2LAB)

        # A partir daqui, será feita a análise LAB das imagens

        # Convertendo a imagem para o espaço de cores LAB
        img_lab = cv.cvtColor(img, cv.COLOR_BGR2LAB)

        l_mean, l_dp, a_mean, a_dp, b_mean, b_dp = calcular_stats(img_lab, maskUtil)
        l_mean, a_mean, b_mean = calibracao(l_mean, a_mean, b_mean)

        print("\tDados da imagem:", image_file)
        tabela(l_mean, l_dp, a_mean, a_dp, b_mean, b_dp)
        print("")

        '''
        img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img_lab_cut_rgb = cv.cvtColor(img_lab_cut, cv.COLOR_BGR2RGB)

     
        plt.figure()
        plt.subplot(1, 2, 1)
        plt.imshow(img_rgb)
        plt.axis("off")
        plt.title("Imagem\n{}".format(image_file))

        plt.subplot(1, 2, 2)
        plt.imshow(img_lab_cut_rgb)
        plt.axis("off")
        plt.title("Imagem LAB\nanalisada")

        plt.show()
        cv.waitKey(0)
        '''

        arquivo_csv(l_mean, l_dp, a_mean, a_dp, b_mean, b_dp, image_file)

    # Calculma regressao de l_arr
    # calcula regressao de a_arr
    # calculca regerassao de b_arr

    return 0

def entrada():
    # Entrada de dados e instruções de uso

    print("COLORIMETRO\n")
    print("Para dar prosseguimento à utilização do programa, escolha uma das opções abaixo:")
    print("1 - Instruções\n2 - Utilize o programa\n3 - Sair\n")
    opcao_bruta = input("Digito escolhido: ")
    os.system('cls')

    while opcao_bruta not in ['2']:
        if opcao_bruta.isnumeric():
            opcao = int(opcao_bruta.strip())
        else:
            opcao = 0

        if opcao in [1, 3]:
            if opcao == 1:
                print("Para que o programa funcione adequadamente, siga as seguintes etapas:\n")
                print("1) Coloque as imagens a serem analisadas em uma pasta.")
                print("2) Indique o caminho da pasta das imagens quando solicitado.")
                print("3) As imagens devem possuir o elemento a ser analisado com o fundo da imagem branco.")
                print("   Sugestão: tire a foto sobre uma folha sulfite, cartulina ou pano branco.")
                print("   Dê preferência a locais bem iluminados sem focos de iluminação que causem grandes reflexos.")
                print("4) As extensões suportadas são: .jpg, .jpeg, .png e .pdf.")
                print("5) O programa mostrará o resultado de cada imagem e salvará os dados em um arquivo CSV.")
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
    # Limpa o terminal quando uma mensagem exibida na tela chega ao fim

    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix/Linux/Mac
        os.system('clear')

def calibracao(l_mean, a_mean, b_mean):
    # Calibração dos valores calculados através de regressão linear
    # para serem compatíveis / próximos aos valores obtidos diretamente com o colorímetro

    l_calibrado = 0.9185*l_mean + 4.0113
    a_calibrado = 0.9772*a_mean - 0.1186
    b_calibrado = 0.9732*b_mean - 0.3492


    return l_calibrado, a_calibrado, b_calibrado

def calcular_stats(imagem_lab, mascara):
    # Calcula médias dos valores de L, a e b da imagem fornecida após obtenção da máscara na função main
    # A máscara se resume aos pixels úteis para análise (sem o fundo)

    l, a, b = cv.split(imagem_lab)
    pixels_validos = cv.findNonZero(mascara)

    l_raw = l[pixels_validos[:, 0, 1], pixels_validos[:, 0, 0]]
    l_validos = np.interp(l_raw, (0, 255), (0, 100)).astype(np.int32)

    a_raw = a[pixels_validos[:, 0, 1], pixels_validos[:, 0, 0]]
    a_validos = np.interp(a_raw, (0, 255), (-128, 128)).astype(np.int32)

    b_raw = b[pixels_validos[:, 0, 1], pixels_validos[:, 0, 0]]
    b_validos = np.interp(b_raw, (0, 255), (-128, 128)).astype(np.int32)

    l_mean = np.mean(l_validos)
    a_mean = np.mean(a_validos)
    b_mean = np.mean(b_validos)
    l_dp = np.std(l_validos)
    a_dp = np.std(a_validos)
    b_dp = np.std(b_validos)
    return l_mean, l_dp, a_mean, a_dp, b_mean, b_dp

def tabela(l_mean, l_dp, a_mean, a_dp, b_mean, b_dp):
    # Imprime os resultados em uma tabela no terminal

    print("\tCanal\t\tMédia\t\tDesvio padrão")
    print("\t  L\t\t\t{:.2f}\t\t{:.2f}\t\t".format(l_mean, l_dp))
    print("\t  a\t\t\t{:.2f}\t\t{:.2f}\t\t".format(a_mean, a_dp))
    print("\t  b\t\t\t{:.2f}\t\t{:.2f}\t\t\n".format(b_mean, b_dp))

def arquivo_csv(l_mean, l_dp, a_mean, a_dp, b_mean, b_dp, nome_imagem):
    nome_arquivo = 'csv_lab.csv'
    campos = ['Canal', 'Média', 'Desvio padrão', 'Imagem']
    dados = [
        ['L', '{:.2f}'.format(l_mean), '{:.2f}'.format(l_dp), nome_imagem],
        ['a', '{:.2f}'.format(a_mean), '{:.2f}'.format(a_dp), nome_imagem],
        ['b', '{:.2f}'.format(b_mean), '{:.2f}'.format(b_dp), nome_imagem]
    ]
    with open(nome_arquivo, 'a', newline='') as arquivo:
        escritor_csv = csv.writer(arquivo)
        escritor_csv.writerows(dados)
    print("\nOs dados foram salvos no arquivo CSV com sucesso!")
    return 0

entrada()
main()
