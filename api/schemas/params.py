from pydantic import BaseModel, Field

# ------------------------------------------
#  Parâmetros das transformações geométricas
# ------------------------------------------

class RotateParams(BaseModel):
    angle: float

class TranslateParams(BaseModel):
    tx: float
    ty: float

class ScaleParams(BaseModel):
    sx: float
    sy: float


# ------------------------------------------
#  Parâmetros das transformações de intensidade
# ------------------------------------------

class IntensityGammaParams(BaseModel):
    gamma: float

class IntensityContrastParams(BaseModel):
    entry_interval: tuple = Field(min_length=2, max_length=2)
    exit_interval: tuple = Field(min_length=2, max_length=2)
