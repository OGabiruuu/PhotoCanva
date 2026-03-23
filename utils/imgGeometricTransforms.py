import imageio.v3 as iio
import numpy as np


#---------------------
# Funções auxiliares
# --------------------

def mat_inv_translation(ti, tj):
    return np.array([
        [1, 0, -ti],
        [0, 1, -tj],
        [0, 0, 1]
    ])

def mat_inv_rotation(theta):
    return np.array([
        [np.cos(theta), np.sin(theta), 0],
        [-np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]
    ])

def mat_inv_scale(si, sj):
    return np.array([
        [1.0/si, 0, 0],
        [0, 1.0/sj, 0],
        [0, 0, 1]
    ])


#---------------------
# Funções de aplicação das transformações corrigidas
# --------------------

def apply_inverse_transform(img, matrix_inv):
    """
    Dada uma matriz de transformação Afim, e uma imagem vetorizada com Numpy, aplica
    a transformação e retorna a imagem final.
    """

    # Criando a nova imagem com 0 para evitar buracos
    new_img = np.zeros_like(img)
    h, w, _ = img.shape

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
    img = iio.imread("../tests/img.jpg")
    h, w, _ = img.shape

    # Criando a matrix para rodar de ponta cabeça com a escala aumentada (de ponta cabeça)
    mat_inv = mat_inv_translation(-h/2.0, -w/2.0)
    mat_inv = mat_inv @ mat_inv_scale(5, 5)
    mat_inv = mat_inv @ mat_inv_rotation(np.radians(-180))

    # Para tornar seu centro o centro do eixo de coord.
    mat_inv = mat_inv @ mat_inv_translation(h/2.0, w/2.0)

    # Aplicando a transformação e reescalando
    img = apply_inverse_transform(img, mat_inv)
    iio.imwrite('../outImgs/out1.jpg', img)
