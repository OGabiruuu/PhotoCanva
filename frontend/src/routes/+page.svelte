<script>
    import logoIcon from '$lib/assets/camera-retro-org.png'

    import NavBar from '$lib/components/NavBar.svelte';
    import ToolBar from '$lib/components/ToolBar.svelte';
    import ImgUploader from '$lib/components/ImgUploader.svelte'
    import { wsManager, wsManagerActions } from '$lib/wsLib.svelte.js';
    import { imgPreviewManager, imgPreviewManagerActions } from '$lib/globalStates/uiStates.svelte';
    import { resetGeometricStates, resetIntensityStates } from '$lib/globalStates/processImgsMessages.svelte';

    let imagLoaded = $derived(imgPreviewManager.url === "" ? false : true);

    // Função de callback que gerencia a atualização de uma imagem após o envio
    // de uma mensagem pelo websocket
    const editedImgHandler = (imgBlob) => {
      const newUrl = URL.createObjectURL(imgBlob);
      imgPreviewManagerActions.setUrl(newUrl);
    }

    // Função de callback que Faz o download da imagem em um fim voluntário da edição
    const handleImgDownloadAtClose = () => {
      const url = imgPreviewManager.url;      // Cópia para impedir erros do agendamento do click
      const a = document.createElement('a');

      // Criando um link efêmero e simulando um click nele para o download
      // Importante que não precisamos nos importar com os estados dado que o ws terá feito
      // isso no próprio onclose, e o $effect vai fazer isso para o imgPreviewManger
      a.href = imgPreviewManager.url;
      a.download = imgPreviewManager.name + '.' + imgPreviewManager.extension;

      // Colocando o link na página para garantir que o navegador executará o click antes
      // de limpar os estados (o que causaria erro no download)
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }

    // Função que gerencia o fluxo de estados ao carregar uma imagem
    const handleSessionInit = (data) => {
      imgPreviewManagerActions.setMetadata(data.file);
      imgPreviewManagerActions.setUrl(data.url);
      wsManagerActions.connect(data.sessionId, editedImgHandler, handleImgDownloadAtClose);
    }


    // Limpar a sessão do previewManager caso a conexão Websocket caia
    $effect(() => {
      if((!wsManager.instance) && (imgPreviewManager.url !== "")) {
        imgPreviewManagerActions.clean();

        // Resetando os estados dos parâmetros de edição
        resetGeometricStates();
        resetIntensityStates();
      }
    });

</script>

<!-- Adiconando título e icone no header -->
<svelte:head>
    <title>PhotoCanva</title>
    <link rel="icon" type="image/svg+xml" href="tabIcon.ico" />
</svelte:head>

<!-- HTML da página (em estilo SPA) -->
{#if !imagLoaded}
    <div id="upload-screen">
        <img src={logoIcon} alt="Logo do PhotoCanva">
        <h1>PhotoCanva</h1>
        <ImgUploader uploadDataHandler={handleSessionInit}/>
    </div>
{:else}
    <div id="edit-screen">
        <NavBar />
        <ToolBar />

        <div id="img-preview-container">
            <img src="{imgPreviewManager.url}" alt="foto carregada">
        </div>
    </div>
{/if}

<style>
    #upload-screen {
        margin: 8% 25% 0% 25%;
        padding: 8% 5% 0% 5%;
        border-radius: 10px;

        box-shadow: 8px 6px 10px rgba(0, 0, 0, 0.4);

        display: flex;
        flex-direction: column;
        align-items: center;

        background-color: var(--clr-outer-box);
        color: var(--clr-txt);

        /*Isso garante que elementos internos possam ser empurrados com auto*/
        min-height: 100px;
    }

    #upload-screen h1 {
        margin-top: 0%;
        font-size: 4em;
    }

    #upload-screen img {
        width: 15%;
        height: 15%;
        padding-bottom: 3%;
    }

    #edit-screen {
        width: 100%;
        height: 100%;

        display: flex;
        align-items:center;
        justify-content: flex-start;
    }

    #img-preview-container {
        margin: 0% 18% 0% 23%;
    }

    #img-preview-container img {
        object-fit: cover;
    }

</style>
