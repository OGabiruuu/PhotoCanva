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
            bind:externalState0={ scaleMsg.params.sx }
            bind:externalState1={ scaleMsg.params.sy }
            onApply = { () => wsManagerActions.sendProcessMsg('geometric', scaleMsg) }
        />
        <SliderInput
            name={'rotação'}
            min={-180}
            max={180}
            step={0.1}
            debounceTime={50}
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
            debounceTime={30}
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
