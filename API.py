from flask import Flask, request
from AnaliseImagemLab import *

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_images():
    # Verifica se o formulário contém as imagens
    if 'image1' not in request.files or 'image2' not in request.files:
        return "Erro: As duas imagens não foram enviadas."

    # Obtém as imagens do formulário
    image1 = request.files['image1']
    image2 = request.files['image2']

    # Salva as imagens em variáveis
    image1_data = image1.read()
    image2_data = image2.read()

    lab1,lab2 = analise_imagem(image1_data, image2_data)

    # Retorna uma resposta com o tamanho das imagens
    return jsonify({"Média L da imagem 1": lab1[0], "Média a da imagem 1": lab1[1],"Média n da imagem 1": lab1[2],
                    "Média L da imagem 2": lab2[0], "Média a da imagem 2": lab2[1], "Média n da imagem 2": lab2[2]}), 200

if __name__ == '__main__':
    app.run(debug=True)