from pydantic import BaseModel, ConfigDict
from typing import Optional
import numpy as np

class ImgCacheRegistry(BaseModel):
    """
    Define o registro interno do cache das imagens em memória
    """

    # Linha necessaria para o Pydantic aceitar np.ndarray como um tipo externo
    model_config = ConfigDict(arbitrary_types_allowed=True)

    img: np.ndarray
    extension: str
    preview: Optional[np.ndarray]
    #preview_1_geometric: Optional[np.ndarray]
    #preview_2_intensity: Optional[np.ndarray]
