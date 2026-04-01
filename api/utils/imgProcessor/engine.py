from .geometry import mat_rotate_and_scale, mat_translate_and_scale, mat_scale_from_center
from .intensity import invert_transform, log_transform, gamma_transform, contrast_modulation

# Registro de todas as funções de processamento implementadas (injeção de dependências da arquitetura)
REGISTRY = {
    # Transformações geométricas
    "rotate": mat_rotate_and_scale,
    "translate": mat_translate_and_scale,
    "scale": mat_scale_from_center,

    # Transformações de intensidade
    "intensity:invert": invert_transform,
    "intensity_log": log_transform,
    "intensisty_gamma": gamma_transform,
    "intensity_contrast": contrast_modulation,
}


def apply_pipeline():
    pass
