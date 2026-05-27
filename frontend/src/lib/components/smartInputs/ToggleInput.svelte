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


<div>
    <p>{name}</p>
    <button disabled={btnDisabled} onclick={toggle}>Aplicar</button>
    <button disabled={twinBtnDisabled} onclick={toggle}>Desfazer</button>
</div>

<style>
    div {
        background-color: gray;
    }
</style>
