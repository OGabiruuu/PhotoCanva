import imageio.v3 as iio
import numpy as np

# Lista das funções públicas exporáveis com "*"
__all__ = [
    'invert_transform',
    'log_transform',
    'gamma_transform',
    'contrast_modulation'
]

#-------------------------
# Transformações
#-------------------------

# Inverte completamente quais pixeis são mais claros e mais escuros
def invert_transform(light, applied):
    """
    Calcula a intensidade inversa da imagem.

    Parâmetros:
        light: Imagem em np.array com todos os canais de cores
        applied: Usado para controlar quando aplicar essa transformação

    Retorno:
        Imagem com cores invertidas no espectro de intensidade [0 - 255]
    """

    return 255 - light if applied else light


# Diminui o dynamic range da imagem bruscamente (ou seja, a diferença entre claros e escuros)
def log_transform(light, applied):
    """
    Aplica a transformação logritmica.

    Parâmetros:
        light: Imagem em np.array com todos os canais de cores
        applied: Usado para controlar quando aplicar essa transformação


    Retorno:
        Imagem com cores suavizadas pela aplicação de log
    """

    c = 255 / np.log(255 + 1)   # Fator de escala
    return np.uint8(c * np.log(np.float32(light) + 1)) if applied else light


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

    if(gamma == 0.0):
        return light

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
    new_light = np.nan_to_num(((np.float32(light) - a) * ((d-c)/(b-a))), nan=0.0, posinf=255.0, neginf=0.0)
    return np.uint8(new_light)


#-------------------------
# Testes
#-------------------------

if __name__ == "__main__":
    IMAGE_PATH = "../testImgs/ganesh.png"
    IMAGE_OUT = "../testImgs/out.png"

    img = iio.imread(IMAGE_PATH)
    #inv_img = contrast_modulation(img, (0, 255), (200, 255))
    inv_img = invert_transform(img, True)

    iio.imwrite(IMAGE_OUT, inv_img)
