import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
import csv

def main():

    #   Versão final.
    #   O código abaixo recebe duas imagens,descarta o fundo branco e realiza comparação da intensidade lab de cada uma.
    #   Funciona para extensões .jpg, .jpeg, .png, .pdf.

    str_img1, str_img2 = obter_nomes_imagens()

    if not (os.path.isfile(str_img1) or os.path.isfile(str_img2)):
        print("Erro: Arquivos das imagens não encontrados.")
        input("Pressione Enter para voltar ao menu.")
        entrada()
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

    # Faixa superior e inferior de branco
    lowerBra = np.array([0, 0, 60])
    upperBra = np.array([255, 100, 255])

    # Cria mascaras de cada faixa de cor para imagem 1 e 2
    maskBra1 = cv.inRange(hsv1, lowerBra, upperBra)  # Faixa de branco
    maskBra2 = cv.inRange(hsv2, lowerBra, upperBra)

    maskUtil1 = cv.bitwise_not(maskBra1)
    maskUtil2 = cv.bitwise_not(maskBra2)

    # Cria imagem sem o fundo
    img1_cp[np.where(maskUtil1 == 0)] = 0
    img2_cp[np.where(maskUtil2 == 0)] = 0

    # A partir daqui, sera feita analise LAB das imagens

    # Convertendo as imagens para o espaço de cores LAB
    img1_lab = cv.cvtColor(img1, cv.COLOR_BGR2LAB)
    img2_lab = cv.cvtColor(img2, cv.COLOR_BGR2LAB)

    l1_mean, l1_dp, a1_mean, a1_dp, b1_mean, b1_dp = calcular_stats(img1_lab, maskUtil1)
    l1_mean, a1_mean, b1_mean = calibracao(l1_mean,a1_mean,b1_mean)
    l2_mean, l2_dp, a2_mean, a2_dp, b2_mean, b2_dp = calcular_stats(img2_lab, maskUtil2)
    l2_mean, a2_mean, b2_mean = calibracao(l2_mean, a2_mean, b2_mean)


    # Calculando as diferenças médias entre os canais das duas imagens
    diff_l = abs(l1_mean - l2_mean)
    diff_a = abs(a1_mean - a2_mean)
    diff_b = abs(b1_mean - b2_mean)

    print("\tDados da imagem 1")
    tabela(l1_mean, l1_dp, a1_mean, a1_dp, b1_mean, b1_dp)
    print("\tDados da imagem 2")
    tabela(l2_mean, l2_dp, a2_mean, a2_dp, b2_mean, b2_dp)
    print("A diferença entre os canais L,a e b são respectivamente: {:.2f}; {:.2f}; {:.2f}.".format(diff_l, diff_a, diff_b))

    arquivo_csv(l1_mean, l1_dp, a1_mean, a1_dp, b1_mean, b1_dp, l2_mean, l2_dp, a2_mean, a2_dp, b2_mean, b2_dp,'csv_lab.csv')
    return 0

def obter_nomes_imagens():
    str_img1 = input("Nome da primeira imagem:")
    str_img2 = input("Nome da segunda imagem:")
    return str_img1, str_img2

def entrada():
    while True:
        print("COLORIMETRO\n")
        print("Escolha uma das opções abaixo:")
        print("1 - Utilize o programa\n2 - Instruções\n3 - Especificações do programa\n4 - Sair\n")
        opcao_bruta = input("Digite o número da opção desejada: ")
        os.system('cls')

        if opcao_bruta == '1':
            main()
            exit()
        elif opcao_bruta == '2':
            print("Instruções:")
            print("Para que o programa funcione adequadamente, siga as seguintes etapas:\n")
            print("1) Tire duas fotos do elemento a ser analisado")
            print("- As duas imagens devem possuir o elemento a ser analisado com o fundo da imagem branco. Sugestão: "
                  "tire a foto sobre uma folha sulfite, cartulina ou pano branco. Dê preferência a locais bem iluminados "
                  "sem focos de iluminação que causem grandes reflexos")
            print("2) Deixe o programa na mesma pasta que as imagens a serem analisadas")
            print("3) Saiba as extensões das imagens analisadas. O programa funciona para as extensões .jpg, .jpeg, .png e .pdf")
            print("4) Execute o programa e indique o nome da imagem a ser analisada juntamente com sua extensão, de acordo com o exemplo:\n\tEXEMPLO1: manjericao_antes.jpg\n\tEXEMPLO2: manjericao_depois.png")
            print("5) Como o programa foi feito para cortar o fundo branco das imagens, pode ser que imagens muito claras apresentem erros")
            input("\nPressione Enter para voltar ao menu.")
            os.system('cls')
        elif opcao_bruta == '3':
            print("Especificações do programa:\n")
            print("O programa foi construido em python através das bibliotecas: cv2, numpy, matplotlib.pyplot, os e csv utilizada na versão 3.10 de python.\nA calibração dos resultados foi realizada através do Spectrofotômetro (colorímetro) modelo CM-600d.\nIncerteza:6 ; 5 ; 5 para os resultados dos canais L,a e b, respectivamente\n\nAutor:\t\t\t\t Arthur Amorim\t\t\t(FEM - Unicamp);\nColaborações:\t\t Douglas Barbin\t\t\t(FEA - Unicamp);\n\t\t\t\t     Vivaldo Silveira\t\t(FEA - Unicamp);\n\t\t\t\t     Hércules Montenegro\t(FEA - Unicamp);\n\t\t\t\t     Carlos Parreira\t\t(FEA - Unicamp);\n\t\t\t\t     Renilson de Luna\t\t(IC - Unicamp);\nData:\t\t\t\t Julho/2023\nInstituição:\t\t FEA - Unicamp")
            input("\nPressione Enter para voltar ao menu.")
            os.system('cls')
        elif opcao_bruta == '4':
            print("Saindo...")
            exit()
        else:
            print("Opção inválida. Digite novamente.\n")
            os.system('cls')

def limpar_terminal():
    # Limpa o terminal quando uma mensagem exibida na tela chega ao fim

    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix/Linux/Mac
        os.system('clear')

def calibracao(l_mean, a_mean, b_mean):
    # calibração dos valores calculares através de regressão linear
    # para ser compatível / próximo a valores obtidos diretamente com colorímetro

    l_calibrado = 0.9185 * l_mean + 4.0113
    a_calibrado = 0.9772 * a_mean - 0.1186
    b_calibrado = 0.9732 * b_mean - 0.3492
    return l_calibrado, a_calibrado, b_calibrado

def calcular_stats(imagem_lab, mascara):
    #   Calcula medias dos valores de L, a e b da imagem fornecida após obtenção da máscara na função main
    #   A máscara se resume aos pixeis uteis para análise (sem o fundo)

    l, a, b = cv.split(imagem_lab)
    pixels_validos = cv.findNonZero(mascara)

    l_raw = l[pixels_validos[:, 0, 1], pixels_validos[:, 0, 0]]                 # pixels_validos[a,b,c], tal que     a: matrizes; b:linhas; c:coluna
                                                                                # de tal forma que ele cria l_raw varre todas as matrizes, pegandos as duplas de coordenadas
                                                                                # em todas as linhas (só tem uma linha)
    l_validos = np.interp(l_raw, (0, 255), (0, 100)).astype(np.int32)

    a_raw = a[pixels_validos[:, 0, 1], pixels_validos[:, 0, 0]]
    a_validos = np.interp(a_raw , (0, 255), (-128, 128)).astype(np.int32)

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
    # Imprimindo os resultados em uma tabela no terminal

    print("\tCanal\t\tMédia\t\tDesvio padrão")
    print("\t  L\t\t\t{:.2f}\t\t{:.2f}\t\t".format(l_mean, l_dp))
    print("\t  a\t\t\t{:.2f}\t\t{:.2f}\t\t".format(a_mean, a_dp))
    print("\t  b\t\t\t{:.2f}\t\t{:.2f}\t\t\n".format(b_mean, b_dp))

def arquivo_csv(l1_mean, l1_dp, a1_mean, a1_dp, b1_mean, b1_dp, l2_mean, l2_dp, a2_mean, a2_dp, b2_mean, b2_dp, nome_imagem):
    nome_arquivo = nome_imagem

    # Verificar se o arquivo já existe
    if os.path.exists(nome_arquivo):
        # Criar um nome alternativo com um número incremental
        nome_base, extensao = os.path.splitext(nome_imagem)
        contador = 1
        while os.path.exists(f"{nome_base}_{contador}{extensao}"):
            contador += 1
        nome_arquivo = f"{nome_base}_{contador}{extensao}"

    campos = ['Canal', 'Imagem 1', 'Desvio padrão 1', 'Imagem 2', 'Desvio padrão 2', 'Diferença']
    dados = [
        ['L', '{:.2f}'.format(l1_mean), '{:.2f}'.format(l1_dp), '{:.2f}'.format(l2_mean),
         '{:.2f}'.format(l2_dp), '{:.2f}'.format(abs(l1_mean - l2_mean))],
        ['a', '{:.2f}'.format(a1_mean), '{:.2f}'.format(a1_dp), '{:.2f}'.format(a2_mean),
         '{:.2f}'.format(a2_dp), '{:.2f}'.format(abs(a1_mean - a2_mean))],
        ['b', '{:.2f}'.format(b1_mean), '{:.2f}'.format(b1_dp), '{:.2f}'.format(b2_mean),
         '{:.2f}'.format(b2_dp), '{:.2f}'.format(abs(b1_mean - b2_mean))]
    ]
    with open(nome_arquivo, 'w', newline='') as arquivo:
        escritor_csv = csv.writer(arquivo)
        escritor_csv.writerow(campos)
        escritor_csv.writerows(dados)
    print("\nOs dados foram salvos no arquivo CSV com sucesso!")
    return 0

entrada()


