from fastapi import FastAPI, UploadFile, HTTPException, WebSocket, WebSocketDisconnect
from utils.imgCache import ImgSessionsManager
from utils.imgProcessor import apply_pipeline, convert_img_to_bytes
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
    extension = file.filename.split(".")[1]

    # Salvando a imagem no registro da sessão
    img_id = img_registry.add_img(img, extension)

    # Retornando o shape da imagem como teste para o sucesso da operação
    return {"status": "success", "imgId":img_id, "shape": img.shape}


@app.websocket("/image/{img_session_id}/edit")
async def edit_image(ws: WebSocket, img_session_id: str):
    """
    Rota websocket que recebe continuamente transformações para aplicar na imagem e
    retorna o binário da imagem alterada
    """

    # Preparando o loop de comunicação
    await ws.accept()
    img = img_registry.get_img(img_session_id)
    extension = img_registry.get_extension(img_session_id)

    # Loop principal da comunicação
    try:
        while True:
            # Recebendo e convertendo o json para um dicionário válido
            transform_data = await ws.receive_json()

            # Aplicando as tranformações e preparando imagem
            img_data = apply_pipeline(img, transform_data)
            img_binary = convert_img_to_bytes(img_data, extension)

            # Enviando mensagem de resposta
            await ws.send_bytes(img_binary)

    except WebSocketDisconnect:
        print("Um erro ocorreu na conexão websocket")
