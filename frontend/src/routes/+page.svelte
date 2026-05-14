<script>
    import NavBar from '$lib/components/NavBar.svelte';
    import ToolBar from '$lib/components/ToolBar.svelte';
    import ImgUploader from '$lib/components/ImgUploader.svelte'
    import { wsManager, wsManagerActions } from '$lib/wsLib.svelte.js';
    import { imgPreviewManager, imgPreviewManagerActions } from '$lib/globalStates/uiStates.svelte';

    let imagLoaded = $derived(imgPreviewManager.url === "" ? false : true);

    // Limpar a sessão do previewManager caso a conexão Websocket caia
    //$effect(() => {
    //  if((!wsManager.instance) && (imgPreviewManager.url !== "")) {
    //    imgPreviewManagerActions.clean();
    //  }
    //});

</script>

<div id="site-container">

    {#if !imagLoaded}
        <h1>PhotoCanva</h1>
        <ImgUploader />
    {:else}
        <NavBar />
        <ToolBar />
        <img src="{imgPreviewManager.url}" alt="foto carregada">
    {/if}
</div>
