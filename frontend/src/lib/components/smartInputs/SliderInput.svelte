<script>
    let {name, externalState = $bindable()} = $props();
</script>

<div>
    <label for="slider-inpt">{name} : {externalState}</label>
    <br>
    <input type="range" name="slider-inpt" min="-180" max="180" bind:value={externalState}>
</div>
