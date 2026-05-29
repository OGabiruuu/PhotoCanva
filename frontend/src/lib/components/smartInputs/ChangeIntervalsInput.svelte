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

<div>
    <label for="intv-2-intv-inpt">{name}</label>
    <p>(
        <input type="number" step="any" bind:value={entryIntervalState[0]}>
        <input type="number" step="any" bind:value={entryIntervalState[1]}>
    </p>

    <p>) para (
      <input type="number" step="any" bind:value={exitIntervalState[0]}>
      <input type="number" step="any" bind:value={exitIntervalState[1]}>
    </p>
    <p>)</p>

    <button onclick={handleApplyInput}>Aplicar</button>
</div>

<style>
    p {
        display: inline;
    }
</style>
