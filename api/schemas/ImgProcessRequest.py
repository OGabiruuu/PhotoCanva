from typing import Union
from pydantic import BaseModel, Field
from typing_extensions import Annotated
from .transforms import IntensityLuminosity, Rotate, Scale, Translate
from .transforms import IntensityInvert, IntensityLog, IntensityGamma, IntensityContrast

# ------------------------------------------
# Macrolistas de cada tipo de transformação
# ------------------------------------------

GeometryFunctions = Annotated[
    Union[Rotate, Scale, Translate],
    Field(discriminator="type")
]

IntensityFunctions = Annotated[
    Union[IntensityLuminosity, IntensityInvert, IntensityLog, IntensityGamma, IntensityContrast],
    Field(discriminator="type")
]

# ------------------------------------------
# Tipo final do dado na requisição
# ------------------------------------------

class ImgProcessRequest(BaseModel):
    geometric: list[GeometryFunctions] = Field(default_factory=list)
    intensity: list[IntensityFunctions] = Field(default_factory=list)
    finalize: bool = False
