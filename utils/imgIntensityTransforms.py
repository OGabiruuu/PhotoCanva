import imageio.v3 as iio
import numpy as np

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


def contrast_modulation(light, entry_interval, exit_interval):
    a, b = entry_interval[:]
    c, d = exit_interval[:]

    print(a, b)
    print(c, d)

    new_light = np.clip(((np.float32(light) - a) * ((d-c)/(b-a)) ), 0, 255)
    return np.uint8(new_light)


#-------------------------
# Testes
#-------------------------

if __name__ == "__main__":
    IMAGE_PATH = "../testImgs/ze.jpg"
    IMAGE_OUT = "../testImgs/out.jpg"

    img = iio.imread(IMAGE_PATH)
    inv_img = contrast_modulation(img, (0, 255), (200, 255))
    #print(inv_img)

    iio.imwrite(IMAGE_OUT, inv_img)
