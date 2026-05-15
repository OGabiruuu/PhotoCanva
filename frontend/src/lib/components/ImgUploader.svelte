<script>
    import { imgPreviewManager, imgPreviewManagerActions } from "$lib/globalStates/uiStates.svelte.js";

    let { uploadDataHandler } = $props(); // Recebe uma função handler do upload pelo componente pai
    let file = $state(null);          // Estado para o input do arquivo pelo usuário

    // Handler do upload no frontend
    const uploadImg = async () => {
      if (!file)
        return;

      // Realizando o upload do que estava no outro estado
      const formData = new FormData();
      formData.append('file', file)

      const response = await fetch('http://localhost:3000/image', {
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
    <input type="file" onchange={(event) => {file = event.target?.files[0]}}>
    <button type="button" onclick={uploadImg}>Iniciar edição</button>
</div>
