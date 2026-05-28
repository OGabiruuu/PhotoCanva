from typing import Dict
import numpy as np
import uuid
from schemas.cacheRegistries import ImgCacheRegistry

# Constantes para referenciar os diferentes previews para cada etapa do pipeline
PREVIEW_SET_ALL = -1
PREVIEW_RAW = 0
PREVIEW_GEOMETRIC = 1
PREVIEW_INTENSITY = 2


# Classe no padrão Repository que Guarda e gerencia os caches das imagens e seus previews
class ImgRepository:
    _imgRepository: Dict[str, ImgCacheRegistry] = {}

    def add_img(self, img: np.ndarray, extension: str):
        """
        Cria um registro formalizado para a nova imagem e o adciona no cache global

        Parâmetros:
            img: Imagem em np.array

        Retorno: uudi do registro
        """

        img_id = str(uuid.uuid4())
        self._imgRepository[img_id] = ImgCacheRegistry(
            img=img,
            preview_raw=None,
            preview_geometric=None,
            preview_intensity=None,
            extension=extension
        )

        return img_id


    def get_img(self, id: str):
        try:
            return self._imgRepository[id].img
        except KeyError as e:
            print(f"Erro ao acessar imagem do registro {id}: {e}")
            raise


    def get_extension(self, id: str):
        try:
            return self._imgRepository[id].extension
        except KeyError as e:
            print(f"Erro ao acessar imagem do registro {id}: {e}")
            raise

    def get_img_preview(self, id: str, which_preview: int):
        """
        Busca no dicionário um preview específico para um dos registros de imagem existentes

        Parâmetros:
            id: Identificador da imagem no dicionario.
            which_preview: Constante que referência um dos previews gerados pelo pipeline de edição

        Retorno: np.ndarray do preview ou None
        """

        try:
            if which_preview == PREVIEW_RAW:
                return self._imgRepository[id].preview_raw
            elif which_preview == PREVIEW_GEOMETRIC:
                return self._imgRepository[id].preview_geometric
            elif which_preview == PREVIEW_INTENSITY:
                return self._imgRepository[id].preview_intensity
            else:
                return None
        except KeyError as e:
            print(f"Erro ao obter o registro {id} no ImgRepository: {e}")
            raise


    def remove_img(self, id: str):
        """
        Remove um registro do cache, propragando erros para a aplicação principal

        Parâmteros:
            id: Identificador da imagem no dicionario.
        """

        try:
            del self._imgRepository[id]
        except KeyError as e:
            print(f"Erro ao deletar o registro {id} no ImgRepository: {e}")
            raise


    def set_img_preview(self, id: str,img_preview: np.ndarray, which_preview=PREVIEW_SET_ALL):
        """
        Atualiza o preview da imagem reduzida dentro do registro já criado

        Parâmetros:
            id: Identificador da imagem no dicionario.
            which_preview: Constante que referência um dos previews gerados pelo pipeline de edição
        """

        try:
            if(which_preview == PREVIEW_RAW):
                self._imgRepository[id].preview_raw = img_preview
            elif(which_preview == PREVIEW_GEOMETRIC):
                self._imgRepository[id].preview_geometric = img_preview
            elif(which_preview == PREVIEW_INTENSITY):
                self._imgRepository[id].preview_intensity = img_preview
            elif(which_preview == PREVIEW_SET_ALL):
                self._imgRepository[id].preview_raw = img_preview
                self._imgRepository[id].preview_geometric = img_preview
                self._imgRepository[id].preview_intensity = img_preview

        except KeyError as e:
            print(f"Erro ao acessar o registro {id} no ImgRepository: {e}")
            raise

    def set_img_previews_from(self, id, new_previews, first_prev_idx):
        """
        Auxiliar para setar todos os previews das diferentes etapas que o pipeline retorna, considerando
        o estado de partida da ultima transformação

        Parâmetros:
            id: Identificador da imagem no dicionario.
            new_previews: Lista com todos os previews que o pipeline retorna
            first_prev_idx: Index que indica de qual preview o pipeline iniciou a alteração
        """

        # Loopando por todos os previews gerados a partir do índice daquele
        # sobre o qual o pipeline iniciou a edição.
        # Se de raw --> idx será 0; se de geo, será 1 e assim por diante
        # É preciso somar 1 nesse idx para igualar as constantes da interface desse registro
        # com a do pipeline
        try:
            for idx, preview in enumerate(new_previews[first_prev_idx:], start=first_prev_idx):
                self.set_img_preview(id, preview, idx + 1)
        except KeyError as e:
            print(f"Erro ao acessar o registro {id} no ImgRepository: {e}")

#----------------------------
#  Testes
# ---------------------------

if __name__ == "__main__":
    you_think_this_is_an_image = np.array([
        [1, 3, 4],
        [2, 2, 2],
        [5, 7, 8],
        [1, 8, 1]
    ])

    img_registry = ImgRepository()

    id = img_registry.add_img(you_think_this_is_an_image, "actually_a_test")
    img_registry.set_img_preview(id, you_think_this_is_an_image[0:2, 0:1])
    img_registry.remove_img(id)

    try:
        img_registry.get_img(id)
    except KeyError:
        print("O erro foi propagado!")

    print("Tudo executado corretamente!")
