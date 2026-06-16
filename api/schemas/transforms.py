from typing import Literal, Optional
from fastapi import params
from pydantic import BaseModel
from .params import RotateParams, TranslateParams, ScaleParams
from .params import IntensityContrastParams, IntensityGammaParams

# ------------------------------------------
#  Tipos das transformações geomátricas
# ------------------------------------------

class Rotate(BaseModel):
    type: Literal["rotate"]
    params: RotateParams

class Translate(BaseModel):
    type: Literal["translate"]
    params: TranslateParams

class Scale(BaseModel):
    type: Literal["scale"]
    params: ScaleParams



# ------------------------------------------
#  Parâmetros das transformações de intensidade
# ------------------------------------------

class IntensityLuminosity(BaseModel):
    type: Literal["intensity_luminosity"] = "intensity_luminosity"
    params: dict = {}

class IntensityInvert(BaseModel):
    type: Literal["intensity_invert"] = "intensity_invert"
    params: dict = {}

class IntensityLog(BaseModel):
    type: Literal["intensity_log"] = "intensity_log"
    params: dict = {}

class IntensityGamma(BaseModel):
    type: Literal["intensity_gamma"] = "intensity_gamma"
    params: Optional[IntensityGammaParams]

class IntensityContrast(BaseModel):
    type: Literal["intensity_contrast"] = "intensity_contrast"
    params: IntensityContrastParams



# ------------------------------------------
#  Parâmetros dos efeitos
# ------------------------------------------
#
class EffectThermo(BaseModel):
    type: Literal["effect_thermo"] = "effect_thermo"
    params: dict = {}

class EffectTvCrt(BaseModel):
    type: Literal["effect_tv_crt"] = "effect_tv_crt"
    params: dict = {}
