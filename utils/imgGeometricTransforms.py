import imageio.v3 as iio
import numpy as np


#---------------------
# Funções auxiliares
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
# Matrizes de transformação corrigidas para evitar bordas escuras
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


def calculate_scale_factor_for_translation(og_w, og_h, ty, tx, old_scale=1.0):
    """
    Calcula as novas dimensões para aplicar a escala mínima que retiraria as bordas
    escuras resultantes da translação de uma imagem a partir das novos limites gerados
    """

    # Calculando o fator de escala faltante (isso se a escala anterior já não cobriu tudo)
    scale_factor = max(1 + (2 * abs(tx) / w), 1 + (2 * abs(ty) / h))

    # Verificando se as escalas anteriores já não impediram o surgimento das bordas
    if old_scale >= scale_factor:
        return 1.0

    # Se não, retornaremos o que faltou escalar
    return scale_factor / old_scale


def mat_translate_and_scale(img, ty, tx, old_scale=1.0):
    """
    Cria a matriz translação com a correção dos seus artefatos com escala (se necessário).

    Parâmetros:
        img: Imagem em np.array
        ty: Deslocamento no eixo Y
        tx: Deslocamento no eixo X
        old_scale: Produto de todas as escalas aplicadas anteriormente nessa imagem

    Retorno:
        Matrix de translação corrigida com a escala
    """

    # Obtendo as dimensões da imagem
    h, w = img.shape[:2]

    # Gerando a matriz de correção da escala (se necessário)
    required_scale = calculate_scale_factor_for_translation(w, h, ty, tx, old_scale)
    if required_scale != 1.0:
        mat = mat_inv_translation(-h/2, -w/2)
        mat = mat @ mat_inv_scale(required_scale, required_scale)
        mat = mat @ mat_inv_translation(h/2, w/2)
        mat = mat @ mat_inv_translation(ty, tx)
    else:
        mat = mat_inv_translation(ty, tx)

    return mat


def mat_rotate_and_scale(img, theta, old_scale=1.0):
    """
    Gera a matriz de rotação e corrige seus artefatos com uma escala (quando necessário).

    Parâmetros:
        img: Imagem em np.array
        theta: ângulo de rotação em graus
        old_scale: Produto de todas as escalas aplicadas anteriormente nessa imagem
    """

    # Obtendo as dimensões da imagem
    h, w = img.shape[:2]

    # Gerando a matriz de rotação no própxio eixo
    mat = mat_inv_translation(-h/2.0, -w/2.0)
    mat = mat @ mat_inv_rotation(theta)

    # Calculando o fator de escala para correção de borda e o aplicando se necessário
    scale_factor = calculate_scale_factor_for_rotation(w, h, theta, old_scale)

    print(scale_factor)

    if scale_factor != 1.0:
        mat = mat @ mat_inv_scale(scale_factor, scale_factor)

    # Deslocando a imagem de volta para o eixo original
    mat = mat @ mat_inv_translation(h/2.0, w/2.0)

    return mat


def mat_scale_from_center(img, sy, sx):
    """
    Aplica a escala em uma imagem a partir do seu centro pelo uso de translações.
    Possívelmente eu apagarei essa função no futuro...
    """

    # Obtendo as dimensões da imagem
    h, w = img.shape[:2]

    # Usando translações para gerar a matriz de escala correta
    mat = mat_inv_translation(-h/2.0, -w/2.0)
    mat = mat @ mat_inv_scale(sy, sx)
    mat = mat @ mat_inv_translation(h/2.0, w/2.0)

#---------------------
# Funções de aplicação da tranformação geométrica final
# --------------------

def apply_inverse_transform(img, matrix_inv):
    """
    Aplica a matriz de transformação afim em uma imagem, usando o método inverso.

    Parâmetros:
        img: Imagem em np.array
        matrix_inv: Matriz afim da transformação inversa

    Retorno:
        Imagem transformada
    """

    # Criando a nova imagem com 0s para evitar buracos
    new_img = np.zeros_like(img)
    h, w = img.shape[:2]

    # Para cara pixel da nova imagem, fazemos o endereçamento invertido
    for i in range(h):
        for j in range(w):
            pos_arr = np.array([i, j, 1])   # Pixel da nova imagem + coord. polar

            # Calculando as coordenadas dos pixeis correspondentes na matrix original
            pos_old = matrix_inv @ pos_arr
            old_i = int(np.round(pos_old[0]))
            old_j = int(np.round(pos_old[1]))

            # Verificando se a coordenada encontrada realmente pertence a imagem original
            if not ((old_i < 0) or (old_j < 0) or (old_i >= h) or (old_j >= w)):
                new_img[i, j] = img[old_i, old_j]

    return new_img



# --------------------
# Teste
# --------------------

if __name__ == "__main__":
    img = iio.imread("../testImgs/pompom_segredo.bmp")
    h, w = img.shape[:2]

    # Criando uma matriz de transformação de teste
    #mat = mat_inv_translation(-h/2, -w/2)
    #mat = mat @ mat_inv_scale(1.19, 1.19)
    #mat = mat @ mat_inv_translation(h/2, w/2)

    #mat = mat @ mat_inv_translation(0, 50)

    mat_final = mat_inv_translation(-h/2, -w/2)
    mat_final = mat_final @ mat_inv_scale(1.4, 1.4)
    mat_final = mat_final @ mat_inv_translation(h/2, w/2)


    mat = mat_rotate_and_scale(img, 50, 1.4)

    mat_final = mat_final @ mat

    # Aplicando a transformação e reescalando
    img = apply_inverse_transform(img, mat_final)
    iio.imwrite('../testImgs/out.jpg', img)
