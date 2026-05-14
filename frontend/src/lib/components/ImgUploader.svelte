<script>
    import { imgPreviewManager, imgPreviewManagerActions } from "$lib/globalStates/uiStates.svelte.js";

    let file = $state(null);

    $inspect(file)

    // Handler do upload no frontend
    const uploadImg = async () => {
      // Obtendo o arquivo enviado ao browser
      if (!file)
        return;

      // Apagando a url do preview anterior (se houver)
      if(imgPreviewManager.url !== "")
        URL.revokeObjectURL(imgPreviewManager.url);

      // Realizando o upload do que estava no outro estado
      const formData = new FormData();
      formData.append('file', file)

      const response = await fetch('http://localhost:3000/image', {
        method: 'POST',
        body: formData
      });
      if (!response.ok) {
        throw new Error('AAAAAAAAAAAAH');
      }

      const imgBlob = await response.blob();

      // Atualizando o preview e a URL
      const newUrl = URL.createObjectURL(imgBlob);
      imgPreviewManagerActions.set(file, newUrl);
    }
</script>

<div>
    <input type="file" onchange={(event) => {file = event.target.files[0]}}>
    <button onclick={uploadImg}>Iniciar edição</button>
</div>
