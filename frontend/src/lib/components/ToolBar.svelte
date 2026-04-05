<script>
    import {toolSetManager} from '$lib/globalStates.svelte.js';
</script>

<div>
    {#if toolSetManager.activeTool == 'geometric'}
        <p>Ferramentas geometricas legais</p>

    {:else if toolSetManager.activeTool == 'intensity'}
        <p>Ferramentas de cor ainda mais legais</p>
    {/if}

    <button>Download</button>
</div>
