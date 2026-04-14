// URL da API que deve ser jogada para um .env no futuro
const ApiUrl = 'ws://localhost:3000/'


// Estado global que armazena as informações da comunicação websocket com o cliente
export const wsManager = $state({
  sessionId: '',           // Armazena o ID da imagem na API
  instance: null,          // Objeto Websocket
  state: 'closed',         // Armazena textual do estado da conexão
  isProcessingMsg: false,  // Informa se esta processando o recibo ou envio de mensagens
});


// Objeto wrapper das funções do socketManager
export const wsManagerActions = {

  // Inicia a conexão, criando e configurando o objeto ws, e atualizando o estado wsManager
  connect(sessionId) {
    wsManager.state = 'connecting'
    const ws = new WebSocket(`${ApiUrl + sessionId}/edit`);

    ws.onopen = () => {
      wsManager.sessionId = sessionId;
      wsManager.state = 'open';
    }


    ws.onerror = (error) => {
      console.error(`ERRO AO CONECTAR O WS: ${error}`);
      //wsManager.state = 'closed';
    }

    // Limpa todo o estado ao fechar
    ws.onclose = () => {
      wsManager.sessionId = '';
      wsManager.state = 'closed';
      wsManager.instance = null;
    }

    ws.onmessage = (msg) => {
      console.log(`Mensagem recebida: ${msg.data}`)
    }

    // Salvando a isntancia
    wsManager.instance = ws;
  },

  // Formaliza a mensagem de processamento pelo tipo da operação e envia para a api com o wsManager
  sendProcessMsg(msgType, processData) {
    if (wsManager.instance?.readyState !== WebSocket.OPEN)
      console.error('Websocket não está aberto');

    // Atualizando manager para o estado de processamento
    wsManager.isProcessingMsg = true;

    // Formalizando a mensagem
    let msg = { geometric: [], intensity: [] };
    if (msgType === 'geometric')
      msg.geometric.push(processData);
    else if (msgType === 'intensity')
      msg.intensity.push(processData);

    // Enviando
    wsManager.instance.send(msg);
    wsManager.isProcessingMsg = false;
  }
}
