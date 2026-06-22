from fastapi import FastAPI, UploadFile, HTTPException, WebSocket, WebSocketDisconnect, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from dotenv import load_dotenv

from adapter.imgNetworkConvertions import generate_img_preview, convert_img_to_bytes
from adapter.imgTransformationProcessor import apply_pipeline, applly_entire_pipeline_optimized
from schemas.ImgProcessRequest import ImgProcessRequest
from cache.ImgTransformRepository import ImgTransformRepository
from cache.ImgRepository import ImgRepository

from concurrent.futures import ThreadPoolExecutor
import imageio as iio
import asyncio
import uvicorn
import os

#----------------------------
#  Instanciando a aplicação
# ---------------------------
app = FastAPI()
img_registry = ImgRepository()                      # Cache em RAM das imagens em edição
img_transform_registry = ImgTransformRepository()   # Cache em RAM do estado das imagens
img_worker = ThreadPoolExecutor(max_workers=4)  # Threads para processar a imagem final

# Lista de origens reconhecidas
origins = ['*']

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

            # Verificando se é uma mensagem de finalização
            if transform_data["finalize"]:
                # Obtendo a imagem original e seu estado do registro
                img = img_registry.get_img(img_session_id)
                img_state = img_transform_registry.get_registry(img_session_id)

                # Aplicando a transformação nas threads executras
                # Assim, impede-se que a API trave no caso de imagens com resolução alta
                final_img = await asyncio.get_running_loop().run_in_executor(
                    img_worker,
                    applly_entire_pipeline_optimized,
                    img,
                    img_state
                )
                final_img_bin = convert_img_to_bytes(final_img, extension)

                # Enviando e fechando a conexão
                await ws.send_bytes(final_img_bin)
                break

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
        print(f"ERRO: Formato de mensagem inválido: {e}")

    except WebSocketDisconnect:
        print("ERRO: Algo ocorreu e a conexão Websocket foi fechada...")

    finally:
        # Removendo os registros de chache
        img_registry.remove_registry(img_session_id)
        img_transform_registry.remove_registry(img_session_id)

        # Fechando a conexão de forma segura
        await ws.close(code=1000)



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
