from fastapi import FastAPI, UploadFile, HTTPException, WebSocket, WebSocketDisconnect, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from dotenv import load_dotenv

from adapter.imgNetworkConvertions import generate_img_preview, convert_img_to_bytes
from adapter.imgTransformationProcessor import apply_pipeline
from schemas.ImgProcessRequest import ImgProcessRequest
from cache.ImgTransformRepository import ImgTransformRepository
from cache.ImgRepository import ImgRepository

import imageio as iio
import uvicorn
import os

#----------------------------
#  Instanciando a aplicação
# ---------------------------
app = FastAPI()
img_registry = ImgRepository()
img_transform_registry = ImgTransformRepository()

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
    allow_headers=["*"],
    # Expondo headers customizados
    expose_headers=["X-Image-Id", "X-Preview_Height", "X-Preview-Width", "X-Preview-Channels"]
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
    Obtem uma imagem a ser processada, salva seu registro em memória e retorna o preview gerado.
    """

    # Verificando se o arquivo recebido é uma imagem
    file_type = file.content_type
    if not file_type or not file_type.startswith("image/"):
        raise HTTPException(415, "Tipo de mídia não suportado")

    try:
        # Lendo o conteúdo da imagem para um np.array
        data = await file.read()
        img = iio.imread(data)

        # Salvando a imagem no registro da sessão
        extension = file.filename.split(".")[1]
        img_id = img_registry.add_img(img, extension)
        img_transform_registry.add_registry(img_id)

        # Gerando o preview
        img_preview = generate_img_preview(img)
        img_registry.set_img_preview(img_id, img_preview)

        # Retornando os dados binários no corpo da requisição e as outras informações em cabeçalhos
        preview_bytes = convert_img_to_bytes(img_preview, extension)
        return Response(
            content=preview_bytes,
            status_code=201,
            media_type=f"image/{extension}",
            headers={
                "X-Image-Id": img_id,
                "X-Preview-Height": str(img_preview.shape[0]),
                "X-Preview-Width": str(img_preview.shape[1]),
                "X-Preview-Channels": str(img_preview.shape[2])
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(500, f"Erro: {e}")



@app.websocket("/image/{img_session_id}/edit")
async def edit_image(ws: WebSocket, img_session_id: str):
    """
    Rota websocket que recebe continuamente transformações para aplicar na imagem e
    retorna o binário da imagem alterada
    """

    # Preparando o loop de comunicação
    await ws.accept()

    # Buscando a extensão da imagem para os envios contínuos
    extension = img_registry.get_extension(img_session_id)

    # Loop principal da comunicação
    try:
        while True:
            # Recebendo os dados em json e validando com o formato esperado
            transform_data = await ws.receive_json()
            ImgProcessRequest(**transform_data)

            # Salvando o novo estado e obtendo o preview certo
            preview_to_change_idx = img_transform_registry.set_transform(img_session_id, transform_data)
            img_preview = img_registry.get_img_preview(img_session_id, preview_to_change_idx)

            # Aplicando as tranformações
            img_state = img_transform_registry.get_registry(img_session_id)
            new_imgs = apply_pipeline(img_preview, img_state, preview_to_change_idx)

            # atualizando os previews necessários
            img_registry.set_img_previews_from(img_session_id, new_imgs, preview_to_change_idx)

            # Enviando mensagem de resposta
            final_img = new_imgs[-1]
            img_binary = convert_img_to_bytes(final_img, extension)
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
