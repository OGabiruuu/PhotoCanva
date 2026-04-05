from pydantic import BaseModel, ConfigDict
from typing import Dict, Optional
import numpy as np
import uuid

class ImgCacheRegistry(BaseModel):
    """
    Define o registro interno do cache das imagens em memória
    """

    # Linha necessaria para o Pydantic aceitar np.ndarray como um tipo externo
    model_config = ConfigDict(arbitrary_types_allowed=True)

    img: np.ndarray
    extension: str
    preview: Optional[np.ndarray]


# Definindo a classe do registro
class ImgSessionsManager:
    _imgRegistry: Dict[str, ImgCacheRegistry] = {}

    def add_img(self, img: np.ndarray, extension: str):
        """
        Cria um registro formalizado para a nova imagem e o adciona no cache global

        Parâmetros:
            img: Imagem em np.array

        Retorno: uudi do registro
        """

        img_id = str(uuid.uuid4())
        self._imgRegistry[img_id] = ImgCacheRegistry(img=img, preview=None, extension=extension)

        return img_id


    def get_img(self, id: str):
        try:
            return self._imgRegistry[id].img
        except KeyError as e:
            print(f"Erro ao acessar imagem do registro {id}: {e}")
            raise


    def get_extension(self, id: str):
        try:
            return self._imgRegistry[id].extension
        except KeyError as e:
            print(f"Erro ao acessar imagem do registro {id}: {e}")
            raise


    def get_img_preview(self, id: str):
        try:
            return self._imgRegistry[id].preview
        except KeyError as e:
            print(f"Erro ao acessar o preview do registro {id}: {e}")
            raise



    def remove_img(self, id: str):
        """
        Remove um registro do cache, propragando erros para a aplicação principal

        Parâmteros:
            id: str
        """

        try:
            del self._imgRegistry[id]
        except KeyError as e:
            print(f"Erro ao deletar o registro {id}: {e}")
            raise


    def set_img_preview(self, id: str, img_preview: np.ndarray):
        """
        Atualiza o preview da imagem reduzida dentro do registro já criado
        """

        try:
            self._imgRegistry[id].preview = img_preview
        except KeyError as e:
            print(f"Erro ao acessar o registro {id}: {e}")
            raise


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

    img_registry = ImgSessionsManager()

    id = img_registry.add_img(you_think_this_is_an_image, "actually_a_test")
    img_registry.set_img_preview(id, you_think_this_is_an_image[0:2, 0:1])
    img_registry.remove_img(id)

    try:
        img_registry.get_img(id)
    except KeyError:
        print("O erro foi propagado!")

    print("Tudo executado corretamente!")
