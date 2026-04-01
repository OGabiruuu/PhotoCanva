import imageio.v3 as iio
import numpy as np

#-------------------------
# Transformações
#-------------------------

# Inverte completamente quais pixeis são mais claros e mais escuros
def invert_transform(light):
    """
    Calcula a intensidade inversa da imagem.

    Parâmetros:
        light: Imagem em np.array com todos os canais de cores

    Retorno:
        Imagem com cores invertidas no espectro de intensidade [0 - 255]
    """

    return 255 - light


# Diminui o dynamic range da imagem bruscamente (ou seja, a diferença entre claros e escuros)
def log_transform(light):
    """
    Aplica a transformação logritmica.

    Parâmetros:
        light: Imagem em np.array com todos os canais de cores
        entry_interval: Extremidades da intensidade a serem modulados
        exit_interval: Intervalo de valores final da intensidade da imagem

    Retorno:
        Imagem modulada no mesmo formato do array
    """

    c = 255 / np.log(255 + 1)   # Fator de escala
    return np.uint8(c * np.log(np.float32(light) + 1))


# Diminui o dynamic range mais suavemente
def gamma_transform(light, gamma=2.2):
    """
    Aplica a transformação de intensidade gamma em uma imagem

    Parâmetros:
        light: Imagem em np.array com todos os canais de cores
        gamma: Parâmetro da função gamma

    Retorno:
        Imagem transformada no mesmo formado de array
    """

    c = 255 / (255 ** (1/gamma))
    return np.uint8(c * (np.float32(light) ** (1/gamma)))


# Parmite alterarmos livremente o contraste da imagem, tornando-o mais suave ou mais acentuado
def contrast_modulation(light, entry_interval, exit_interval):
    """
    Aplica a modulação de contraste em uma imagem.

    Parâmetros:
        light: Imagem em np.array com todos os canais de cores
        entry_interval: Extremidades da intensidade a serem modulados
        exit_interval: Intervalo de valores final da intensidade da imagem

    Retorno:
        Imagem modulada no mesmo formato do array
    """

    # Passando os intervalos para variáveis melhores, só para melhorar a
    # legibilidade mesmo
    a, b = entry_interval[:]
    c, d = exit_interval[:]

    # Aplicando a modulação com clip para garantir que nenhum valor estoure o range de 8 bits
    new_light = np.clip(((np.float32(light) - a) * ((d-c)/(b-a)) ), 0, 255)
    return np.uint8(new_light)


#-------------------------
# Testes
#-------------------------

if __name__ == "__main__":
    IMAGE_PATH = "../testImgs/ze.jpg"
    IMAGE_OUT = "../testImgs/out.jpg"

    img = iio.imread(IMAGE_PATH)
    inv_img = contrast_modulation(img, (0, 255), (200, 255))

    iio.imwrite(IMAGE_OUT, inv_img)
