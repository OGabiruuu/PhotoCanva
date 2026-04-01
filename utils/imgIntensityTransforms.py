import imageio.v3 as iio
import numpy as np

IMAGE_PATH = "../testImgs/ze.jpg"
OUT_PATH = "../outImgs/out3.jpg"

#-------------------------
# Transformações
#-------------------------

# Inverte completamente quais pixeis são mais claros e mais escuros
def invert_transform(light):
    return 255 - light

# Diminui o dynamic range da imagem bruscamente (ou seja, a diferença entre claros e escuros)
def log_transform(light):
    c = 255 / np.log(255 + 1)   # Fator de escala
    return np.uint8(c * np.log(np.float32(light) + 1))

# Diminui o dynamic range mais suavemente
def gamma_transform(light, gamma=2.2):
    c = 255 / (255 ** (1/gamma))
    return np.uint8(c * (np.float32(light) ** (1/gamma)))

#-------------------------
# Testes
#-------------------------

img = iio.imread(IMAGE_PATH)
inv_img = gamma_transform(img)
iio.imwrite(OUT_PATH, inv_img)
