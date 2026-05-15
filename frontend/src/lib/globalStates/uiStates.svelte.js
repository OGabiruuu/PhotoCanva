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
  clean() {
    // Desalocando a URL da memória do navegador
    if (imgPreviewManager.url && imgPreviewManager.url !== '')
      URL.revokeObjectURL(imgPreviewManager.url);

    imgPreviewManager.url = '';
    imgPreviewManager.name = '';
    imgPreviewManager.extension = '';
  },

  set(file, url) {
    // Desalocando a antiga URL da memória do navegador
    if (imgPreviewManager.url)
      URL.revokeObjectURL(imgPreviewManager.url);

    imgPreviewManager.url = url;
    imgPreviewManager.name = file.name.split('.')[0];
    imgPreviewManager.extension = file.name.split('.')[1];
  }
});
