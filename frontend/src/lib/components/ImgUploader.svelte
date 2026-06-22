<script>
    import { onMount, tick } from "svelte";

    let { uploadDataHandler } = $props(); // Recebe uma função handler do upload pelo componente pai
    let file = $state(null);              // Estado para o input do arquivo pelo usuário
    let fileInput;                        // Variável atrelada ao valor do input


    let fileLoaded = $derived(!file);    // Controla o enable dos inputs internos da UI desse componente
    let fileExtension = $derived(file ? file.name.split('.').pop()?.toUpperCase() : 'Carregar arquivo');

    //Garantindo que o campo de input está limpo a cada inicialização.
    // Ele demora para executar em reloads, mas isso parece ser um comportamento do navegador.
    onMount(() => {
      file = null;

      requestAnimationFrame(() => {
        fileInput.value = "";
      })
    });

    // Handler do upload no frontend
    const uploadImg = async () => {
      if (!file)
        return;

      // Realizando o upload do que estava no outro estado
      const formData = new FormData();
      formData.append('file', file)

      const response = await fetch('http://localhost:8000/image', {
        method: 'POST',
        body: formData
      });
      if (!response.ok) {
        throw new Error(`Um erro ocorreu ao enviar a imagem: ${response.status}`);
      }

      // Gerando a nova URL
      const imgBlob = await response.blob();
      const newUrl = URL.createObjectURL(imgBlob);

      // Obtendo os dados da seção pelo cabeçalho da imagem:
      const session = response.headers.get('X-Image-id');

      // Jogando os novos dados do upload para serem tratados pelo componente pai
      uploadDataHandler({url: newUrl, file: file, sessionId: session})
    }
</script>

<div>
    <!-- for liga a label ao id do input. Isso permite colocarmos ela por cima dele e ainda usar suas funções-->
    <label for="file">
        {file? `arquivo .${fileExtension} carregado` : 'Carregar arquivo'}
    </label>
    <input id="file" bind:this={fileInput} type="file" onchange={(event) => {file = event.target?.files[0]}}>
</div>

<button type="button" disabled={fileLoaded} onclick={uploadImg}><h3>Iniciar edição</h3></button>

<style>
    div {
        position: relative;
        padding: 5% 3% 3% 3%;
    }

    label {
        position: absolute;
        left: 25%;
        padding: 5%;

        background-color: var(--clr-inner-box);
        border-radius: 5px;
        box-shadow: 4px 3px 5px rgba(0, 0, 0, 0.4);

        cursor: pointer;
        transition: all 0.3s ease;
    }

    label:hover {
        border: 1px solid var(--clr-dtl);
        color: var(--clr-dtl);
    }

    input {
        opacity: 0;
        cursor: pointer;
        pointer-events: none; /*Impede ele de sobrepor o hover da label*/
        padding: 5%;
    }

    button {
        width: 100%;
        margin: inherit;
        padding-top: 5%;
        margin-bottom: 10%;

        border: none;
        border-top: 1px solid var(--clr-dtl);
        background-color: var(--clr-outer-box);
        color: var(--clr-txt);

        cursor: pointer;
        transition: border-color 1.0s ease, color 1.0s ease;
    }

    button:disabled {
        cursor: not-allowed;
        border-top-color: var(--clr-inner-box);
        color: var(--clr-txt-dsbl);
    }

    button h3 {
        margin: 0%;
    }
</style>
