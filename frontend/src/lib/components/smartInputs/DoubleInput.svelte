<script>
    let {
      name,
      externalState0 = $bindable(),   // Valor mais a esquerda
      externalState1 = $bindable(),   // Valor mais a direita
      onApply                         // Handler da aplicação dos valores registrado
    } = $props()

    // Envia o input para o handler externo garantindo que não há valores nulos
    const handleApplyInput = () => {
      if(externalState0 === null || externalState1 === null) {
        console.log(`input nulo detectado em ${name}`)
        return;
      }

      onApply();
    }

</script>

<div class="input-box">
    <label for="dbl-inpt">{name}</label>
    <input type="number" step="any" bind:value={externalState0}>
    <input type="number" step="any" bind:value={externalState1}>
    <button onclick={ handleApplyInput }>Apply</button>
</div>

<style>
    .input-box {
        padding: 8% 8% 8% 8%;
        width: 100%;

        border-radius: 5px;
        background-color: var(--clr-outer-box);
        border: solid 1px var(--clr-background);

        transition: border-color 0.5s ease;
    }

    .input-box:hover {
        border-color: var(--clr-dtl);
    }

    /* Removendo seta do input em Chromium-based browsers */
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
      -webkit-appearance: none;
      margin: 0;
    }

    /* Removendo a seta do input no Firefox */
    input[type=number] {
        appearance: textfield;
        -moz-appearance: textfield;
    }

    label {
        display: block;
        margin-bottom: 8%;

        font-size: 1.2rem;
    }

    input {
        margin: 2%;
        width: 15%;

        text-align: center;
        background-color: var(--clr-background);
        border: solid 2px var(--clr-background);

        color: var(--clr-txt);
        font-size: 1em;
    }

    input:focus {
        outline: solid 1px var(--clr-dtl);
    }

    button {
        padding: 3%;
        margin-left: 11%;

        background-color: var(--clr-dtl);
        border: none;
        border-radius: 5px;

        color: var(--clr-txt);
        font-size: 1em;
        font-weight: bold;
        cursor: pointer;
        transition: margin 0.2s ease;
    }

    button:hover {
        margin-left: 13%;
    }

    button:active {
        background-color: var(--clr-dtl-shadowy);
        margin: 0% 0% 0% 8%;
    }

</style>
