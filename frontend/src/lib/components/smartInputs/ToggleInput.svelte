<script>
    let {name, applied = $bindable()} = $props();

    // Estados internos para o toggle dos botões
    let btnDisabled = $derived(applied);
    let twinBtnDisabled = $derived(!btnDisabled);

    // Função que executa a inversão tando nos botões quanto no estado externo
    const toggle = () => {
      applied = !applied
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
