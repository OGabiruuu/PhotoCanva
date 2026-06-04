import imageio.v3 as iio
import numpy as np
from intensity import luminosity_transform

def thermo_effect(light, applied):
    # Obtendo a imagem em tons de cinza
    light_value = luminosity_transform(light, True)

    # Aplicando um verde alto apenas em áres quentes
    new_g = np.where(light_value >= 128, (light_value - 128) * 2, 0)

    # Aplicando um azul maior para zonas mais escuras
    new_b = np.where(light_value < 128, 255 - light_value, 0)

    # Aplicando o vermelho mais puro apenas entre 64 e 128. Depois, ele sobe
    # para 255 se misturando com o verde para criar amarelo e branco
    new_r = np.where(light_value < 128, 0, 255)

    # Tirando overflows e empilhando de volta em uma imagem RGB
    r = np.clip(new_r, 0, 255)
    g = np.clip(new_g, 0, 255)
    b = np.clip(new_b, 0, 255)

    return np.uint8(np.dstack((r, g, b)))


if __name__ == "__main__":
    img = iio.imread('/Users/ogabiruuu/Documents/wallpappers/niklas-garnholz-CT8JAmljGC0-unsplash.jpg')

    new_img = thermo_effect(img, True)

    print(np.shape(new_img))
    iio.imwrite('test.jpg', new_img)
