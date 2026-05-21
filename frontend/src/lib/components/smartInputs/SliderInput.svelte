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

<div>
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
