<script>
    let {name, externalState = $bindable()} = $props();

    // Estados internos para o toggle dos botões
    let btnDisabled= $state(false);
    let twinBtnDisabled = $derived(!btnDisabled);

    // Função que executa a inversão tando nos botões quanto no estado externo
    const toggle = () => {
      btnDisabled = !btnDisabled;
      externalState = !externalState;
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
