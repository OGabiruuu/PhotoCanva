<script>
    let {
      name,      // Nome do input na UI
      onToggle,  // Função handler dos botões
      externalState = $bindable()   // Estado booleno que externo que o botão controla
    } = $props();

    // Estados internos para o toggle dos botões
    let applied = $derived(externalState === true);
    let btnDisabled = $derived(applied);
    let twinBtnDisabled = $derived(!applied);

    // Função que executa a inversão no estado externo e chama o handler do componente
    const toggle = () => {
      externalState = !externalState
      onToggle();
    }
</script>


<div class="input-box">
    <p>{name}</p>
    <button disabled={btnDisabled} onclick={toggle}>Aplicar</button>
    <button disabled={twinBtnDisabled} onclick={toggle}>Desfazer</button>
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

    p {
        display: block;
        margin-bottom: 8%;

        font-size: 1.2rem;
    }

    button {
        padding: 3%;
        margin: 0% 0% 0% 8%;

        background-color: var(--clr-dtl);
        border: solid 1px var(--clr-dtl);
        border-radius: 5px;

        color: var(--clr-txt);
        font-size: 1em;
        font-weight: bold;
        cursor: pointer;
        transition: margin 0.2s ease;
    }

    button:enabled:hover {
        border: solid 1px var(--clr-dtl-weak);
    }

    button:active {
        background-color: var(--clr-dtl-shadowy);
    }

    button:disabled {
        background-color: var(--clr-dtl-shadowy);
        border-color: var(--clr-dtl-shadowy);
    }

</style>
