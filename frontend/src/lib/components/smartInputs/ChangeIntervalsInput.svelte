<script>
    let {
      name,
      entryIntervalState = $bindable(), // Intervalo com os valores de entrada
      exitIntervalState = $bindable(),  // Intervalo dos valores da saída normalizada
      onApply,
    } = $props();

    const handleApplyInput = () => {
      // Verificando se os intervalos não estão fora do esperado
      if((entryIntervalState[0] > entryIntervalState[1]) || (exitIntervalState[0] > exitIntervalState[1])) {
        console.warn(`Intervalos com valores iniciais maiores que os finais`);
        return;
      }

      onApply();
    }
</script>

<div class="input-box">
    <label for="intv-2-intv-inpt">{name}</label>

    <div class="input-layer">
        <p>(
            <input type="number" step="any" bind:value={entryIntervalState[0]}>
            <input type="number" step="any" bind:value={entryIntervalState[1]}>
        )</p>
    </div>

    <div class="input-layer">
        <p> para </p>
        <br>
    </div>

    <div class="input-layer">
        <p>(
            <input type="number" step="any" bind:value={exitIntervalState[0]}>
            <input type="number" step="any" bind:value={exitIntervalState[1]}>
        )</p>
    </div>

    <button onclick={handleApplyInput}>Aplicar</button>
</div>

<style>
    p {
        margin: 0%;
        padding: 0%;
        display: inline;
    }

    label {
        display: block;
        margin-bottom: 8%;

        font-size: 1.1rem;
    }


    .input-box {
        padding: 8% 0% 8% 4%;
        margin-bottom: 2%;
        width: 92%;

        border-radius: 5px;
        background-color: var(--clr-outer-box);
        border: solid 1px var(--clr-background);
        transition: border-color 0.5s ease;
    }

    .input-box:hover {
        border-color: var(--clr-dtl);
    }

    .input-layer {
        margin-top: 5%;
        text-align: center;
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

    input {
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
        display: block;
        padding: 3%;
        margin-left: 33%;
        margin-top: 5%;

        background-color: var(--clr-dtl);
        border: solid 1px var(--clr-dtl);
        border-radius: 5px;

        color: var(--clr-txt);
        text-align: center;
        font-size: 1em;
        font-weight: bold;
        cursor: pointer;
        transition: margin 0.2s ease;
    }

    button:hover {
        border-color: var(--clr-dtl-weak);
    }

    button:active {
        border-color: var(--clr-dtl-shadowy);
        background-color: var(--clr-dtl-shadowy);
        margin-top: 5%;
    }
</style>
