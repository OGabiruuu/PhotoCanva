<script>
    import NavBar from '$lib/components/NavBar.svelte';
    import ToolBar from '$lib/components/ToolBar.svelte';
    import ImgUploader from '$lib/components/ImgUploader.svelte'
    import { wsManager, wsManagerActions } from '$lib/wsLib.svelte.js';
    import { imgPreviewManager, imgPreviewManagerActions } from '$lib/globalStates/uiStates.svelte';
    import { resetGeometricStates, resetIntensityStates } from '$lib/globalStates/processImgsMessages.svelte';

    let imagLoaded = $derived(imgPreviewManager.url === "" ? false : true);

    // Função que gerencia o fluxo de estados ao carregar uma imagem
    const handleSessionInit = (data) => {
      imgPreviewManagerActions.setMetadata(data.file);
      imgPreviewManagerActions.setUrl(data.url);
      wsManagerActions.connect(data.sessionId, editedImgHandler);
    }

    // Função de callback que gerencia a atualização de uma imagem
    const editedImgHandler = (imgBlob) => {
      const newUrl = URL.createObjectURL(imgBlob);
      imgPreviewManagerActions.setUrl(newUrl);
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

<div id="site-container">

    {#if !imagLoaded}
        <h1>PhotoCanva</h1>
        <ImgUploader uploadDataHandler={handleSessionInit}/>
    {:else}
        <NavBar />
        <ToolBar />
        <img src="{imgPreviewManager.url}" alt="foto carregada">
    {/if}
</div>
