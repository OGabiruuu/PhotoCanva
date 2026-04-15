from fastapi import FastAPI, UploadFile, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware;
from pydantic import ValidationError
from schemas.ImgProcessRequest import ImgProcessRequest
from utils.imgProcessor.geometry import GeometryHandler
from utils.imgCache import ImgSessionsManager
from dotenv import load_dotenv
from utils.imgProcessor import generate_img_preview, apply_pipeline, convert_img_to_bytes
import imageio as iio
import uvicorn
import os

#----------------------------
#  Instanciando a aplicação
# ---------------------------
app = FastAPI()
img_registry = ImgSessionsManager()

# Lista de origens reconhecidas
origins = [
    "http://localhost:5173"
]

# Configurando o CORS da API
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

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

    # Gerando o preview
    img_preview = generate_img_preview(img)
    img_registry.set_img_preview(img_id, img_preview)

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
    local_geometry_handler = GeometryHandler()

    # Buscando a extensão da imagem para os envios contínuos
    img_preview = img_registry.get_img_preview(img_session_id)
    extension = img_registry.get_extension(img_session_id)

    # Obtendo a imagem original para o fim da edição
    #img = img_registry.get_img(img_session_id)

    # Loop principal da comunicação
    try:
        while True:
            # Recebendo os dados em json e validando com o formato esperado
            transform_data = await ws.receive_json()
            ImgProcessRequest(**transform_data)

            # Aplicando as tranformações e atualizando o cache
            img_preview = apply_pipeline(img_preview, transform_data, local_geometry_handler)
            img_registry.set_img_preview(img_session_id, img_preview)

            # Enviando mensagem de resposta
            img_binary = convert_img_to_bytes(img_preview, extension)
            await ws.send_bytes(img_binary)

    except ValidationError as e:
        print(f"Formato de mensagem inválido: {e}")

    except WebSocketDisconnect:
        # Removendo a imagem e o preview do registro
        img_registry.remove_img(img_session_id)


#----------------------------
#  Configurando o servidor para rodar com as variáveis de ambiente
# ---------------------------

if __name__ == "__main__":
    # Carregando variáveis de ambiente
    load_dotenv()
    host = os.getenv("HOST")
    port = os.getenv("PORT")

    # Rodando o servidor
    if port and host:
        uvicorn.run(app, host=host, port=int(port))
    else:
        print("Erro ao carregar variáveis de ambiente")
