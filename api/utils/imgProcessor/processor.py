import io
import numpy as np
from PIL import Image
import imageio as iio
from .intensity import invert_transform, log_transform, gamma_transform, contrast_modulation

# Registro de todas as funções de processamento implementadas (injeção de dependências da arquitetura)
PROCESS_REGISTRY = {
    # Transformações geométricas
    "rotate": "set_mat_rotate_and_scale",
    "translate": "set_mat_translate_and_scale",
    "scale": "set_mat_scale_from_center",

    # Transformações de intensidade
    "intensity_invert": invert_transform,
    "intensity_log": log_transform,
    "intensisty_gamma": gamma_transform,
    "intensity_contrast": contrast_modulation,
}

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


def apply_pipeline(img, transformations, geo_processer):
    """
    Orquestrador que aplica corretamente a sequencia de processamentos informada.

    Parâmetros:
        img: Imagem em np.array
        transformations: Lista de Dicionários com as informações da transformação

    retorno:
        Imagem processada
    """


    if len(transformations['geometric']) != 0:
        for transform in transformations['geometric']:
            method_str = PROCESS_REGISTRY.get(transform['type'])
            if method_str:
                method = geo_processer.__getattribute__(method_str)
                method(img, **transform['params'])

        # Aplicando a transformação geométrica final
        img = geo_processer.apply_inverse_transform(img)

    # Aplicando as transformações de intensidade (Note que elas não guardam estadado. Logo, são funções comuns)
    for transform in transformations['intensity']:
        func = PROCESS_REGISTRY.get(transform["type"])
        if func:
            print(f"Aquiiii com {func}")
            img = func(img, **transform["params"])

    # Retornando a imagem final
    print(transformations)
    return img

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



# Anotação sobre como os dados devem ser passados no futuro:
#
# {
#   geometric: [
#       {type: "rotate", params: {...}} {type: "translate", params: {...}}
#   ]
#   intensity: []
# }
#
