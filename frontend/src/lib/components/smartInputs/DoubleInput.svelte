<script>
    let {
      name,
      externalState0 = $bindable(),
      externalState1 = $bindable()
    } = $props()

</script>

<div>
    <label for="dbl-inpt">{name}</label>
    <input type="number" step="any" bind:value={externalState0}>
    <input type="number" step="any" bind:value={externalState1}>
    <button>Apply</button>
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
