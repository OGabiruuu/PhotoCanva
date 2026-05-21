<script>
    let {
      name,
      externalState0 = $bindable(),   // Valor mais a esquerda
      externalState1 = $bindable(),   // Valor mais a direita
      onApply                         // Handler da aplicação dos valores registrado
    } = $props()

</script>

<div>
    <label for="dbl-inpt">{name}</label>
    <input type="number" step="any" bind:value={externalState0}>
    <input type="number" step="any" bind:value={externalState1}>
    <button onclick={ onApply }>Apply</button>
</div>

<style>
    /* Removendo seta do input em Chromium-based browsers */
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
      -webkit-appearance: none;
      margin: 0;
    }

    /* Removendo a seta do input no Firefox */
    input[type=number] {
      -moz-appearance: textfield;
    }

</style>
