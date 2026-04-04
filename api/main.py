from fastapi import FastAPI, UploadFile, HTTPException
from utils.imgCache import ImgSessionsManager
import imageio as iio

#----------------------------
#  Instanciando a aplicação
# ---------------------------
app = FastAPI()
img_registry = ImgSessionsManager()


#----------------------------
#  Definindo as rotas HTTP
# ---------------------------

@app.get("/")
def test_root():
    return {"salute": "Hello world"}

@app.post("/image")
async def receive_image(file: UploadFile):
    """
    Obtem uma imagem a ser processada e a salva em um registro em memória.
    """

    # Verificando se o arquivo recebido é uma imagem
    file_type = file.content_type
    if not file_type or not file_type.startswith("image/"):
        raise HTTPException(415, "Tipo de mídia não suportado")

    # Lendo o conteúdo da imagem para um np.array
    data = await file.read()
    img = iio.imread(data)

    # Salvando a imagem no registro da sessão
    img_id = img_registry.add_img(img)

    # Retornando o shape da imagem como teste para o sucesso da operação
    return {"status": "success", "imgId":img_id, "shape": img.shape}
