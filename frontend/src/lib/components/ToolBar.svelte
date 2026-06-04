<script>
    import {toolSetManager} from '$lib/globalStates/uiStates.svelte.js';
    import ToggleInput from './smartInputs/ToggleInput.svelte'
    import DoubleInput from './smartInputs/DoubleInput.svelte';
    import SliderInput from './smartInputs/SliderInput.svelte';
    import ChangeIntervalsInput from './smartInputs/ChangeIntervalsInput.svelte';
    import  { wsManagerActions } from '../wsLib.svelte'
    import {
      intensityConstrastMsg,
      intensityGammaMsg,
      intensityInvertMsg,
      intensityLogMsg,
      translateMsg,
      scaleMsg,
      rotateMsg
    } from '$lib/globalStates/processImgsMessages.svelte'


</script>

<div>
    {#if toolSetManager.activeTool == 'geometric'}
        <DoubleInput
            name={'Translação'}
            bind:externalState0={ translateMsg.params.tx }
            bind:externalState1={ translateMsg.params.ty }
            onApply = { () => wsManagerActions.sendProcessMsg('geometric', translateMsg) }
        />
        <DoubleInput
            name={'Escala'}
            minValue={1}
            bind:externalState0={ scaleMsg.params.sx }
            bind:externalState1={ scaleMsg.params.sy }
            onApply = { () => wsManagerActions.sendProcessMsg('geometric', scaleMsg) }
        />
        <SliderInput
            name={'rotação'}
            min={-180}
            max={180}
            step={0.1}
            debounceTime={15}
            bind:externalState={ rotateMsg.params.theta }
            onChange = {() => wsManagerActions.sendProcessMsg('geometric', rotateMsg)}
        />


    {:else if toolSetManager.activeTool == 'intensity'}
        <ToggleInput
            name={'Invert'}
            bind:externalState={ intensityInvertMsg.params.applied }
            onToggle = { () => wsManagerActions.sendProcessMsg('intensity', intensityInvertMsg) }
        />
        <ToggleInput
            name={'Log'}
            bind:externalState={ intensityLogMsg.params.applied }
            onToggle = { () => wsManagerActions.sendProcessMsg('intensity', intensityLogMsg) }
        />
        <SliderInput
            name={'Gamma'}
            min={0.0}
            max={1.0}
            step={0.01}
            debounceTime={15}
            bind:externalState={ intensityGammaMsg.params.gamma }
            onChange= {() => wsManagerActions.sendProcessMsg('intensity', intensityGammaMsg)}
        />
        <ChangeIntervalsInput
            name={'Modulação de contraste'}
            bind:entryIntervalState={ intensityConstrastMsg.params.entry_interval }
            bind:exitIntervalState={ intensityConstrastMsg.params.exit_interval }
            onApply={ () => wsManagerActions.sendProcessMsg('intensity', intensityConstrastMsg) }
        />
    {/if}

    <button onclick={ () => {wsManagerActions.sendProcessMsg("finalize", null)} }>Download</button>
</div>

<style>
    div {
        height: 100%;
        max-height: 100%;
        box-sizing: border-box;
        width: 28%;
        z-index: 0;

        padding: 2% 2% 0% 2%;
        /*padding: 6% 0% 0% 0%;*/

        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        gap: 1%;

        background-color: var(--clr-inner-box);
    }

    button {
        width: 50%;
        padding: 3%;
        margin-top: auto;
        margin-bottom: 5%;

        background-color: var(--clr-dtl-invt);
        box-shadow: 8px 6px 10px rgba(10, 10, 10, 0.4);
        border: none;
        border-radius: 10px;

        cursor: pointer;
        transition: margin 0.2s ease;
    }

    button:hover {
        margin-bottom: 8%;
    }

    /*para quando ele é clicado*/
    button:active {
        background-color: var(--clr-dtl-invt-shadowy);
        box-shadow: none;
        margin: auto 0% 5% 1%;
    }
</style>
