import imageio.v3 as iio
import numpy as np
from lib.intensity import luminosity_transform

def thermo_effect(light, applied):

    if(applied):
        # Obtendo a imagem em tons de cinza
        light_value = luminosity_transform(light, True)

        # Aplicando um verde alto apenas em áres quentes
        new_g = np.where(light_value >= 128, (light_value - 128) * 2, 0)

        # Aplicando um azul maior para zonas mais escuras
        new_b = np.where(light_value < 128, 255 - light_value, 0)

        # Vermelho ou não ocorre nas sonas frias, ou sobe para complementar ao verde
        new_r = np.where(light_value < 128, 0, 255)

        # Tirando overflows e empilhando de volta em uma imagem RGB
        r = np.clip(new_r, 0, 255)
        g = np.clip(new_g, 0, 255)
        b = np.clip(new_b, 0, 255)

        return np.uint8(np.dstack((r, g, b)))
    else:
        return light


# Auxiliar para criar as linhas escuras no crt_filter
def _apply_scan_lines(img, shadow_level):
    lines, cols = img.shape

    for i in range(0, lines, 2):
        img[i, :] *= (1.0 - shadow_level)

    return np.clip(img, 0.0, 255.0)

# Auxiliar para criar o efeito de shiado estático no crt_filter
def _apply_crt_noise(img, quantity):
    noise = np.random.normal(0, quantity, img.shape)

    noisy_img = img + noise
    return np.clip(noisy_img, 0.0, 255.0)

def crt_tv_effect(img, applied):
    if applied:
        float_img = img.astype(np.float32)

        # Convertendo a imagem para preto e branco
        lum_img = luminosity_transform(float_img, True).astype(np.float32)
        scan_img = _apply_scan_lines(lum_img, 0.8)
        crt_img = _apply_crt_noise(scan_img, 10)

        return crt_img.astype(np.uint8)
    else:
        return img


if __name__ == "__main__":
    img = iio.imread('/Documents/wallpappers/img.jpg')

    new_img = thermo_effect(img, True)

    print(np.shape(new_img))
    iio.imwrite('test.jpg', new_img)
