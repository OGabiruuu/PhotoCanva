<script>
    let {
      toolSetIconSrc,
      toolSetName,
      isActive,
      onClickHandler,
    } = $props();

</script>

<button class:active={isActive} title={toolSetName} onclick={onClickHandler}>
    <img
        src={toolSetIconSrc}
        class="navBar-icon"
        alt={toolSetName}
        title={toolSetName}
    >
</button>

<style>
    .navBar-icon {
        max-width: 100%;
        max-height: 100%;
        object-fit: cover;  /*Mantém a proporção da imagem*/
    }

    button {
        margin-bottom: 50%;
        padding: 20%;
        height: 35px;
        width: 35px;

        background-color: var(--clr-inner-box);
        border: solid 1px var(--clr-inner-box);
        border-radius: 3px;
        box-shadow: 8px 6px 10px rgba(0, 0, 0, 0.4);

        transition: all 0.8s ease, color 1.0s ease;
    }

    button:hover {
        border-color: var(--clr-dtl);
        height: 48px;
        width: 48px;
    }

    .active {
        border-color: var(--clr-dtl);
    }
</style>
