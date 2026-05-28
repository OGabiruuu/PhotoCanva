import io
import numpy as np
from PIL import Image
import imageio as iio

def generate_img_preview(img: np.ndarray, max_width: int = 350):
    """
    Gera um preview de baixa resolução da imagem para diminuir a latência da comunicação

    Prâmetros:
        img: np.ndarray da imagem original
        max_width: Largura máxima do preview em pixeis

    Retorno:
        np.ndarray da imagem redimensionada
    """

    h, w = img.shape[:2]
    if w <= max_width:
        return img

    # Calculando a nova altura mantendo o Aspect Ratio
    ratio = max_width / float(w)
    new_height = int(h * ratio)

    # Convertendo para Pilow image
    pil_img = Image.fromarray(img)

    # Redimensionando
    pil_img = pil_img.resize((max_width, new_height), resample=Image.Resampling.LANCZOS)

    # Converte de volta para numpy
    return np.array(pil_img)


def convert_img_to_bytes(img, img_extension):
    """
    Converte o np.ndarray de uma imagem em bytes de um arquivo adequado para o envio em rede

    Parâmetros:
        img: np.ndarray da imagem
        img_extension: string com a extensão do formato original da imagem

    retorno:
        buffer: Objeto Bytes contendo a imagem formatada
    """

    buffer = io.BytesIO()
    iio.imwrite(buffer, img, img_extension)

    return buffer.getvalue()
