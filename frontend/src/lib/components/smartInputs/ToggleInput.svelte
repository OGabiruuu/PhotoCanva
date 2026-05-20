<script>
    let {name, onToggle} = $props();

    // Estados internos para o toggle dos botões
    let applied = $state(false);
    let btnDisabled = $derived(applied);
    let twinBtnDisabled = $derived(!btnDisabled);

    // Função que executa a inversão tando nos botões quanto no estado externo
    const toggle = () => {
      applied = !applied
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
