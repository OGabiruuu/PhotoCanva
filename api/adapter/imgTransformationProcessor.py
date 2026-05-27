
from lib.intensity import invert_transform, log_transform, gamma_transform, contrast_modulation
from lib.geometry import GeometryHandler

# Constantes para configurar o modo de edição
# isto é, de qual ponto reaplicaremos o pipeline
APPLY_FROM_RAW = 0
APPLY_FROM_GEOMTERIC = 1
APPLY_FROM_INTENSITY = 2


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


def apply_pipeline(img, state, mode):
    """
    Orquestrador que aplica corretamente a sequência de processamentos informada.

    Parâmetros:
        img: Imagem em np.array
        transformations: Lista de Dicionários com as informações da transformação

    retorno:
        Imagem processada
    """

    geo_processer = GeometryHandler()

    if(mode == APPLY_FROM_RAW):
        for transform, params in state["geometric"].items():
            method_str = PROCESS_REGISTRY.get(transform)
            if method_str:
                method = geo_processer.__getattribute__(method_str)
                method(img, **params)

        # Aplicando a transformação geométrica final
        img = geo_processer.apply_inverse_transform(img)

    # Sempre aplicamos as de intensidade ao fim
    for transform, params in state["intensity"].items():
        func = PROCESS_REGISTRY.get(transform)
        if func:
            img = func(img, **params)

    # Retornando a imagem final
    return img
