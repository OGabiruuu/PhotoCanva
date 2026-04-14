<script>
    import {toolSetManager} from '$lib/globalStates/uiStates.svelte.js';
    import ToggleInput from './smartInputs/ToggleInput.svelte'
    import DoubleInput from './smartInputs/DoubleInput.svelte';
    import SliderInput from './smartInputs/SliderInput.svelte';

    // Estados da translação
    let tx = $state(0);
    let ty = $state(0);

    // Estados da escala
    let sx= $state(1);
    let sy = $state(1);

    // Estado da rotação
    let theta = $state(0);

    // Estados das transformações de intensidade
    let apply_invert = $state(false);
    let apply_log = $state(false);


</script>

<div>
    {#if toolSetManager.activeTool == 'geometric'}
        <DoubleInput name={'Translação'} bind:externalState0={tx} externalState1={ty}/>
        <DoubleInput name={'Escala'} bind:externalState0={sx} externalState1={sy}/>
        <SliderInput name={'rotação'} bind:externalState={theta}/>

    {:else if toolSetManager.activeTool == 'intensity'}
        <ToggleInput name={'Invert'} bind:externalState={apply_invert} />
        <ToggleInput name={'Log'} bind:externalState={apply_log} />
        <!-- <SliderInput /> -->
    {/if}

    <button>Download</button>
</div>
