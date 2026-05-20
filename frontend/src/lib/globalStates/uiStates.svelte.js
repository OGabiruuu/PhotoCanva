// Estado Que gerencia a lista de ferramenta e seus componentes ativos
export const toolSetManager = $state({
  activeTool: 'geometric'
});

// Estado que guarda as informações do último preview gerado da imagem em edição
export const imgPreviewManager = $state({
  url: '',
  name: '',
  extension: ''
});

export const imgPreviewManagerActions = $state({

  // Tira toda a informação de estado da imagem ao fim de uma edição
  clean() {
    // Desalocando a URL da memória do navegador
    if (imgPreviewManager.url && imgPreviewManager.url !== '')
      URL.revokeObjectURL(imgPreviewManager.url);

    imgPreviewManager.url = '';
    imgPreviewManager.name = '';
    imgPreviewManager.extension = '';
  },

  // Salva os estados dos metadados de uma imagem a partir do objeto File
  setMetadata(file) {
    imgPreviewManager.name = file.name.split('.')[0];
    imgPreviewManager.extension = file.name.split('.')[1];
  },

  // Salva a URL criada de um novo estado da imagem corretamente.
  setUrl(url) {
    if (imgPreviewManager.url)
      URL.revokeObjectURL(imgPreviewManager.url);
    imgPreviewManager.url = url;
  },
});
