<script>
    import {toolSetManager} from '$lib/globalStates/uiStates.svelte'
</script>


<div id="navBar-container">
    <div id="title">
        <h1>PhotoCanva</h1>
        <!-- Imagem legal -->
    </div>

    <div id="navBar-options">
        <button onclick={() => {toolSetManager.activeTool = 'geometric'}}>
            Transformações geométricas
        </button>
        <button onclick={() => toolSetManager.activeTool = 'intensity'}>
            Transformações de intensidade
        </button>
    </div>
</div>
