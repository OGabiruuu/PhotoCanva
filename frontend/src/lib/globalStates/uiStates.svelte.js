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
    imgPreviewManager.url = '';
    imgPreviewManager.name = '';
    imgPreviewManager.extension = '';
  },

  set(file, url) {
    imgPreviewManager.url = url;
    imgPreviewManager.name = file.name.split('.')[0];
    imgPreviewManager.extension = file.name.split('.')[1];
  }
});
