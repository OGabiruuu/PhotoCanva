from fastapi import FastAPI, UploadFile, HTTPException
import imageio as iio

app = FastAPI()

@app.get("/")
def test_root():
    return {"salute": "Hello world"}

@app.post("/image")
async def receive_image(file: UploadFile):
    """
    Obtem uma imagem a ser processada
    """

    # Verificando se o arquivo recebido é uma imagem
    file_type = file.content_type
    if not file_type or not file_type.startswith("image/"):
        raise HTTPException(415, "Tipo de mídia não suportado")

    # Lendo o conteúdo da imagem para um np.array
    data = await file.read()
    img = iio.imread(data)

    # Retornando o shape da imagem como teste para o sucesso da operação
    return {"status": "success", "shape": img.shape}
