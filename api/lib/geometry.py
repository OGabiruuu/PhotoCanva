import imageio.v3 as iio
import numpy as np
from .geometryPrimitives import mat_inv_rotation, mat_inv_scale, mat_inv_translation
from .geometryPrimitives import calculate_scale_factor_for_rotation, calculate_scale_factor_for_translation

class GeometryHandler:

    def __init__(self, scale_factor=1.0):
        self.afim_matrix = np.eye(3)        # Matriz de transformação que será calculada
        self.scale_factor = scale_factor    # Guarda o fator de escala atual da imagem
        self.angle = 0                      # Guarda o angulo atual da imagem em graus


    def set_mat_translate_and_scale(self, img, ty=0, tx=0):
        """
        Cria a matriz translação com a correção dos seus artefatos com escala (se necessário).

        Parâmetros:
            img: Imagem em np.array
            ty: Deslocamento no eixo Y
            tx: Deslocamento no eixo X
            old_scale: Produto de todas as escalas aplicadas anteriormente nessa imagem

        Retorno:
            Matrix de translação corrigida com a escala
            fator de escala usado
        """

        # Retornando caso os parâmetros passados sejam elementos neutros da translação
        if tx == 0 and ty == 0:
            return

        # Obtendo as dimensões da imagem
        h, w = img.shape[:2]

        # Gerando a matriz de correção da escala (se necessário)
        required_scale = calculate_scale_factor_for_translation(w, h, ty, tx, self.angle, self.scale_factor)
        print(f"Required: {required_scale}")
        if required_scale != 1.0:
            self.afim_matrix @= mat_inv_translation(-h/2, -w/2)
            self.afim_matrix @= mat_inv_scale(required_scale, required_scale)
            self.afim_matrix @= mat_inv_translation(h/2, w/2)
            self.afim_matrix @= mat_inv_translation(ty, tx)

            # Atualizando o estado da escala
            self.scale_factor *= required_scale
        else:
            self.afim_matrix @= mat_inv_translation(ty, tx)



    def set_mat_rotate_and_scale(self, img, theta=0.0):
        """
        Gera a matriz de rotação e corrige seus artefatos com uma escala (quando necessário).

        Parâmetros:
            img: Imagem em np.array
            theta: ângulo de rotação em graus
            old_scale: Produto de todas as escalas aplicadas anteriormente nessa imagem

        Retorno:
            Imagem transformada
            fator de escala aplicado
        """

        # Retornando caso o theta passado seja o valor neutro da operação
        if theta == 0.0:
            return

        # Obtendo as dimensões da imagem
        h, w = img.shape[:2]

        # Gerando a matriz de rotação no própxio eixo
        self.afim_matrix @= mat_inv_translation(-h/2.0, -w/2.0)
        self.afim_matrix @= mat_inv_rotation(theta)

        # Calculando o fator de escala para correção de borda e o aplicando se necessário
        required_scale = calculate_scale_factor_for_rotation(w, h, theta, self.scale_factor)

        if required_scale != 1.0:
            self.afim_matrix @= mat_inv_scale(required_scale, required_scale)
            self.scale_factor *= required_scale
            print(f"Updated scale at rotation: {self.scale_factor}")
        self.angle = theta

        # Deslocando a imagem de volta para o eixo original
        self.afim_matrix @= mat_inv_translation(h/2.0, w/2.0)



    def set_mat_scale_from_center(self, img, sy, sx):
        """
        Aplica a escala em uma imagem a partir do seu centro pelo uso de translações.
        Possívelmente eu apagarei essa função no futuro...

        Old_scale só está aqui para manter a interface comum com o orquestrador
        """

        # Retornando caso os valores sejam os elementos neutros
        if sy == 1 and sx == 1:
           return

        # Obtendo as dimensões da imagem
        h, w = img.shape[:2]

        # Usando translações para gerar a matriz de escala correta
        self.afim_matrix @= mat_inv_translation(-h/2.0, -w/2.0)
        self.afim_matrix @= mat_inv_scale(sy, sx)
        self.afim_matrix @= mat_inv_translation(h/2.0, w/2.0)

        # Atualizando o fator de escala
        self.scale_factor *= max(sx, sy)


    #---------------------
    # Methodo de aplicação da tranformação geométrica final
    # --------------------

    def apply_inverse_transform(self, img):
        """
        Aplica a matriz de transformação afim em uma imagem, usando o método inverso.

        Parâmetros:
            img: Imagem em np.array
            matrix_inv: Matriz afim da transformação inversa

        Retorno:
            Imagem transformada
        """

        # Retornando caso a matriz de transformação não tenha sido alterada
        if np.array_equal(self.afim_matrix, np.eye(3)):
            return img

        # Criando a nova imagem com 0s para evitar buracos
        new_img = np.zeros_like(img)
        h, w = img.shape[:2]

        # Para cara pixel da nova imagem, fazemos o endereçamento invertido
        for i in range(h):
            for j in range(w):
                pos_arr = np.array([i, j, 1])   # Pixel da nova imagem + coord. polar

                # Calculando as coordenadas dos pixeis correspondentes na matrix original
                pos_old = self.afim_matrix @ pos_arr
                old_i = int(np.round(pos_old[0]))
                old_j = int(np.round(pos_old[1]))

                # Verificando se a coordenada encontrada realmente pertence a imagem original
                if not ((old_i < 0) or (old_j < 0) or (old_i >= h) or (old_j >= w)):
                    new_img[i, j] = img[old_i, old_j]

        self.afim_matrix = np.eye(3)
        return new_img



# --------------------
# Teste
# --------------------

if __name__ == "__main__":
    img = iio.imread("../testImgs/pompom_segredo.bmp")
    h, w = img.shape[:2]

    handler = GeometryHandler()

    handler.set_mat_scale_from_center(img, 1.9, 1.9)
    handler.set_mat_rotate_and_scale(img, 45)
    print(f"Scale after rotation: {handler.scale_factor}")
    handler.set_mat_translate_and_scale(img, 10, 4)
    #handler.set_mat_scale_from_center(img, 1.04, 1.04)
    print(f"Scale after translation: {handler.scale_factor}")

    # Criando uma matriz de transformação de teste
    #mat = mat_inv_translation(-h/2, -w/2)
    #mat = mat @ mat_inv_scale(1.19, 1.19)
    #mat = mat @ mat_inv_translation(h/2, w/2)

    #mat = mat @ mat_inv_translation(0, 50)

    #mat_final, _ = mat_inv_translation(-h/2, -w/2)[0]
    #mat_final = mat_final @ mat_inv_scale(1.4, 1.4)[0]
    #mat_final = mat_final @ mat_inv_translation(h/2, w/2)[0]


    #mat = mat_rotate_and_scale(img, 50, 1.4)

    #mat_final = mat_final @ mat

    # Aplicando a transformação e reescalando
    img = handler.apply_inverse_transform(img)
    iio.imwrite('../testImgs/out.jpg', img)
