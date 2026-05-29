from pydantic import BaseModel, Field

# ------------------------------------------
#  Parâmetros das transformações geométricas
# ------------------------------------------

class RotateParams(BaseModel):
    theta: float

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
    entry_interval: tuple[int, int] = (0, 255)
    exit_interval: tuple[int, int] = (0, 255)
