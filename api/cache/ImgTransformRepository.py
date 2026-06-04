from typing import Dict
import copy
from .ImgRepository import PREVIEW_RAW, PREVIEW_GEOMETRIC

IMAGE_STATE = {
    "geometric": {
        "translate": {
            "tx": 0,
            "ty": 0
        },
        "scale": {
            "sx": 1,
            "sy": 1,
        },
        "rotate": {
            "theta": 0
        },
    },
    "intensity": {
        "intensity_luminosity": {
            "applied": False
        },
        "intensity_invert": {
            "applied": False
        },
        "intensity_log": {
            "applied": False
        },
        "intensity_gamma": {
            "gamma": 1.0
        },
        "intensity_contrast": {
            "entry_interval": (0, 255),
            "exit_interval": (0, 255)
        }
    },
    "effect": {
        "effect_thermo": {
            "applied": False
        },
    }
}

# Classe no padrão repository que guarda e gerência os dicionarios de estados para cada parâmetro
# editável das imagens registradas
class ImgTransformRepository:
    _transforms: Dict[str, Dict] = {}

    def add_registry(self, img_id):
        new_state_dict = copy.deepcopy(IMAGE_STATE)
        self._transforms[img_id] = new_state_dict

    def set_transform(self, img_id, transform_message) -> int:
        preview_to_change = -1

        if len(transform_message["geometric"]) != 0:
            self._transforms[img_id]["geometric"][transform_message["geometric"][0]["type"]] = transform_message["geometric"][0]["params"]
            preview_to_change = PREVIEW_RAW

        elif len(transform_message["intensity"]) != 0:
            self._transforms[img_id]["intensity"][transform_message["intensity"][0]["type"]] = transform_message["intensity"][0]["params"]
            preview_to_change = PREVIEW_GEOMETRIC

        elif len(transform_message["effect"]) != 0:
            self._transforms[img_id]["effect"][transform_message["effect"][0]["type"]] = transform_message["effect"][0]["params"]
            preview_to_change = PREVIEW_GEOMETRIC

        return preview_to_change

    def get_registry(self, img_id):
        try:
            return self._transforms[img_id]
        except KeyError as e:
            print(f"Erro ao acessar as transformações do registro {img_id}: {e}")
            raise

    def remove_registry(self, img_id):
        try:
            del self._transforms[img_id]
        except KeyError as e:
            print(f"Erro ao deletar o registro {img_id} no ImgTransformRepository: {e}")
            raise
