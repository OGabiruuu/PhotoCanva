<script>
    let {
      name,                        // Nome do componente
      externalState = $bindable(), // Estado externo a ser alterado pelo slider
      debounceTime = 0,            // Tempo do debounce
      min,                         // Valor mínimo do slider
      max,                         // Valor máximo do slider
      step = 1,                    // Passo por input
      onChange                     // Função handler do slide
    } = $props();

    // timer é uma variável interna para o controle do debounce
    let timer = null;

    // Debounce aplicado internamente para impedir chamadas excessívas
    const handleInputDebounced = () => {
      if(timer)
        clearTimeout(timer);

      timer = setTimeout(() => {
        console.log("Tempo passou")
        onChange();
        timer = null;
      }, debounceTime);
    }

</script>

<div class="input-box">
    <label for="slider-inpt">{name} : {externalState}</label>
    <br>
    <input
        type="range"
        name="slider-inpt"
        min={min}
        max={max}
        step={step}
        bind:value={externalState}
        oninput={handleInputDebounced}
    >
</div>

<style>
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

    label {
        display: block;
        margin-bottom: 8%;

        font-size: 1.2rem;
    }

    input {
        margin: 2%;

        text-align: center;
        background-color: var(--clr-outer-box);

        accent-color: var(--clr-dtl);
        color: var(--clr-txt);
        font-size: 1em;
    }

    input:hover {
        cursor: grab;
    }

    input:hover:active {
        cursor: grabbing;
    }

    /* Estilizando o botão (Thumb) no Firefox, Chromium e Safari */
    input[type=range]::-moz-range-thumb {
      background: var(--clr-dtl);
      border: none;

      accent-color: var(--clr-dtl);
    }

    input[type=range]::-webkit-slider-thumb {
      background: var(--clr-dtl);
      border: none;

      accent-color: var(--clr-dtl);
    }

    /* Estilizando a barra (Track) no Firefox , Chromium e Safari*/
    input[type=range]::-moz-range-track {
      background-color: var(--clr-background);
      accent-color: var(--clr-dtl);

    }

    input[type=range]::-webkit-slider-runnable-track {
      background-color: var(--clr-background);
      accent-color: var(--clr-dtl);

    }
</style>
