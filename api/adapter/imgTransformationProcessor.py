
from utils.imgProcessor.intensity import invert_transform, log_transform, gamma_transform, contrast_modulation

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
            img = func(img, **transform["params"])

    # Retornando a imagem final
    return img





# Anotação sobre como os dados devem ser passados no futuro:
#
# {
#   geometric: [
#       {type: "rotate", params: {...}} {type: "translate", params: {...}}
#   ]
#   intensity: []
# }
#
