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

    // Garante que nenhum input nulo do usuário será enviado
    function sendInstantMessage(typeMsg, processData) {
      let isInputNull = Object.values(processData).some((attribute) => attribute === null )
      if(isInputNull) {
        console.log('input nulo detectado...')
        return;
      }

      console.log('Foiiiii')
      wsManagerActions.sendProcessMsg(typeMsg, processData);
    }

</script>

<div>
    {#if toolSetManager.activeTool == 'geometric'}
        <DoubleInput
            name={'Translação'}
            bind:externalState0={ translateMsg.params.tx }
            bind:externalState1={ translateMsg.params.ty }
            onApply= { () => sendInstantMessage('geometric', translateMsg) }
        />
        <DoubleInput
            name={'Escala'}
            bind:externalState0={ scaleMsg.params.sx }
            bind:externalState1={ scaleMsg.params.sy }
            onApply= { () => sendInstantMessage('geometric', scaleMsg) }
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
            onToggle={ () => sendInstantMessage('intensity', intensityInvertMsg) }
        />
        <ToggleInput
            name={'Log'}
            onToggle={ () => sendInstantMessage('intensity', intensityLogMsg)}
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
    {/if}

    <button>Download</button>
</div>
