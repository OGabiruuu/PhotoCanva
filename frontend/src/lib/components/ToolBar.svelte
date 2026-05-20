<script>
    import {toolSetManager} from '$lib/globalStates/uiStates.svelte.js';
    import ToggleInput from './smartInputs/ToggleInput.svelte'
    import DoubleInput from './smartInputs/DoubleInput.svelte';
    import SliderInput from './smartInputs/SliderInput.svelte';
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

    function sendInstantMessage(typeMsg, processData) {
      console.log('aquiiii')
      wsManagerActions.sendProcessMsg(typeMsg, processData);
    }

    function sendDebouncedMessage() {

    }

</script>

<div>
    {#if toolSetManager.activeTool == 'geometric'}
        <DoubleInput
            name={'Translação'}
            bind:externalState0={ translateMsg.params.tx }
            bind:externalState1={ translateMsg.params.ty }
        />
        <DoubleInput
            name={'Escala'}
            bind:externalState0={ scaleMsg.params.sx }
            bind:externalState1={ scaleMsg.params.sy }
        />
        <SliderInput
            name={'rotação'}
            bind:externalState={ rotateMsg.params.theta }
        />

    {:else if toolSetManager.activeTool == 'intensity'}
        <ToggleInput
            name={'Invert'}
            //bind:applied={ intensityInvertMsg.params.active }
            onToggle={ () => sendInstantMessage('intensity', intensityInvertMsg) }
        />
        <ToggleInput
            name={'Log'}
            //bind:applied={ intensityLogMsg.params.active }
            onToggle={ () => sendInstantMessage('intensity', intensityLogMsg)}
            />
        <!-- <SliderInput /> -->
    {/if}

    <button>Download</button>
</div>
