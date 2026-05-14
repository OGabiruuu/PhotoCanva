<script>
    import { imgPreviewManager, imgPreviewManagerActions } from "$lib/globalStates/uiStates.svelte.js";

    let file = $state(null);

    // Handler do upload no frontend
    const uploadImg = async () => {
      if (!file)
        return;

      // Guardando a URL antiga
      let oldUrl = imgPreviewManager.url;

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

      // Atualizando o preview e a URL
      const imgBlob = await response.blob();
      const newUrl = URL.createObjectURL(imgBlob);
      imgPreviewManagerActions.set(file, newUrl);

      // Desalocando a antiga URL
      if(oldUrl) {
        URL.revokeObjectURL(oldUrl);
      }
    }
</script>

<div>
    <input type="file" onchange={(event) => {file = event.target?.files[0]}}>
    <button type="button" onclick={uploadImg}>Iniciar edição</button>
</div>
