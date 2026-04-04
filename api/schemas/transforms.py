from typing import Literal, Optional
from pydantic import BaseModel
from params import RotateParams, TranslateParams, ScaleParams
from params import IntensityContrastParams, IntensityGammaParams

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

class IntensityInvert(BaseModel):
    type: Literal["intensity_invert"]
    params: None

class IntensityLog(BaseModel):
    type: Literal["intensity_log"]
    params: None

class IntensityGamma(BaseModel):
    type: Literal["intensity_gamma"]
    params: Optional[IntensityGammaParams]

class IntensityContrast(BaseModel):
    type: Literal["intensity_contrast"]
    params: IntensityContrastParams
