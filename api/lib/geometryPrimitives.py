import numpy as np

#---------------------
# Funções auxiliares para geração das matrizes inversas de transformação
# --------------------

def mat_inv_translation(ty, tx):
    return np.array([
        [1, 0, -ty],
        [0, 1, -tx],
        [0, 0, 1]
    ])

def mat_inv_rotation(theta):
    # Convertendo para radianos, pois esse é o input padrão das funções np.sin() e np.cosin()
    angle = np.radians(theta)

    return np.array([
        [np.cos(angle), np.sin(angle), 0],
        [-np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])

def mat_inv_scale(sy, sx):
    return np.array([
        [1.0/sy, 0, 0],
        [0, 1.0/sx, 0],
        [0, 0, 1]
    ])



#---------------------
# Funções auxiliares para o cáculo das transformações corrigitas
# --------------------

def calculate_scale_factor_for_rotation(og_w, og_h, theta, old_scale=1.0):
    """
    Calcula as novas dimensões para aplicar a escala minima que retiraria as bordas
    escuras resultantes da rotação de uma imagem a partir das novos limites gerados
    """

    # Convertendo em radianos para o calculo da projeção
    angle = np.radians(theta)

    # Calculando as dimensões da nova caixa limitadora
    new_w = abs(og_h * np.sin(angle)) + abs(og_w * np.cos(angle))
    new_h = abs(og_h * np.cos(angle)) + abs(og_w * np.sin(angle))

    # Obendo como fator o maximo entre a razão da nova largura com a original
    # a da nova altura com a original
    scale_factor = max(new_h / og_h, new_w / og_w)

    # Verificando se as escalas anteriores já não corrigem o problema da borda
    if old_scale >= scale_factor:
        return 1.0

    return scale_factor / old_scale


def calculate_scale_factor_for_translation(og_w, og_h, ty, tx, theta, old_scale=1.0):
    """
    Calcula as novas dimensões para aplicar a escala mínima que retiraria as bordas
    escuras resultantes da translação de uma imagem a partir das novos limites gerados
    """

    # Convertendo o angulo para radianos (padrão das funções numpy)
    angle = np.radians(theta)

    # Recalculando as dimensões de escala da rotação atual
    # Note que optou-se por usar old_scale, pois outras escalas podem ter sido feitas pelo usuário
    new_w = abs(og_h * np.sin(angle)) + abs(og_w * np.cos(angle))
    new_h = abs(og_h * np.cos(angle)) + abs(og_w * np.sin(angle))
    rotation_scale_factor = max(new_h / og_h, new_w / og_w)

    # Calculando o fator de escala faltante para a translação
    proj_x = abs(tx * np.cos(angle)) + abs(ty * np.sin(angle))
    proj_y = abs(tx * np.sin(angle)) + abs(ty * np.cos(angle))
    translation_scale_factor = max(2 * proj_x / og_w, 2 * proj_y / og_h)

    # Calculando o fator de escala necessário final
    scale_factor = rotation_scale_factor + translation_scale_factor


    # Verificando se as escalas anteriores já não impediram o surgimento das bordas
    if old_scale >= scale_factor:
        return 1.0

    # Se não, retornaremos o que faltou escalar
    return scale_factor / old_scale
