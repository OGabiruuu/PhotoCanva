# Trabalho 1 - Meu editor de imagens genérico

* Disciplina: Processamento de Imagens

* Aluno: Gabriel Antunes Afonso de Araujo - 14571077

---

## Introdução ao projeto

`PhotoCanva` foi concebido como um editor de imagens em tempo real na Web, implementando todas as funcionalidades requeridas pelo trabalho por meio de uma interface gráfica e inputs simples para as funções.

O Frontend foi desenvolvido em `Svelte5` (um framework reativo para JavaScript), e o backend com `python3` e `FastAPI`. Para as funções de edição foi utilizado `Pyhton3` com `Numpy`, e todas elas estão implementadas e comentadas em `api/lib`. O orquestrador da aplicação das funcões recebe está em `api/adapter/imgTransformationProcessor.py`.

![Tela inicial](imgs/init.png)

#### Fluxo interno do software

Ao carregar uma imagem e iniciar a edição, está é enviada para a API, que gera um preview comprimido e guarda ele e a imagem original em um dicionário Python (que funciona como um banco em memória) e cria um identificador único para esse registro, retornando-o para o frontend.

Por sua vez, a cada alteração na imagem feita pelo usuário, o forntend usa esse id para mandar a mesnagem dizendo a função que será chamada e os parametros a serem aplicados, para uma rota com o mesmo ID do registro da imagem. Assim, a API cai em uma rotina comum que puxa o preview comprimido da imagem, atualiza o estado dos parâmetros da edição no dicionario e aplica tudo isso em `api/adapter/imgTransformationProcessor.py`, retornando o preview com as edições aplicadas até então para o frontend apresentar ao usuário.

Quanto terminada a edição, o frontend evnia uma mensagem para a API que aciona a rota que pega a imagem original, reaplica todas as edições que tiveram um efeito ao fim e retorna para o usuário a imagem editada em resolução original.

Para tornar a aplicação viável e responsíva, as seguintes estratégias foram aplicadas:

- Uso de dicionário em memória para guardar as imagens;
- Uso de preview comprimido da imagem durante a edição;
- Comunicação durante a edição por Websocket, para eliminar o overhead das mensagens de rede;
- Vetorização da função de aplicação das transformação geométricas (são o maior gargálo do projeto);
- Divisão de previews em 'geométrico' e 'final', para evitar repalicar as transformações geométricas a cada alteração na imagem.

![Entrando na edição](imgs/editing.png)

#### Fluxo de uso

1. Clique em 'carregar imagem' ao abrir o sitie, e escolhe a imagem a ser editada.

2. Clique em 'iniciar edição' para levar a imagem a pagina de edição.

3. No canto mais a esqurda, você verá uma barra lateral com ícones. Essa é a `Toolbar`, contendo os grupos de ferramentas de edição: Geométricas, transformações de intensidade e efeitos visuais, respectivamente

4. Va para o grupo de ferramentas e brinque com os inputs e parâmetros para fazer a sua edição!

5. Ao fim, clique em Download para terminar o processo. O site baixará a imagem para sua pasta `downloads` e voltará a página inicial.

![Editando](imgs/editing2.png)

## Dependências para rodar

* docker
* docker compose

## Como rodar

1. Inicialize o Docker na máquina (`systemctl start docker` no Linux, ou `open -a docker` no macOS)

2. Execute o Docker Compose para iniciar os serviços: `docker compose up`

3. Acesse a aplicação em `http://localhost:80`


#### Lista das principais funções

Aqui vale citar que para impedir os pixels vazios em transformações geométricas foi utilizada a técinca de esclara a imagem em relação ao seu centro por um fator mínio que elimine as bordas vazias.

* **Translação:** Translada em aplica o zoom necessário na imagem para impedir pixeis vaios, tanto em X quanto em Y.

* **Escala:** Aplica uma escala com fator x e y espressos pelo usuário 

* **Rotação**: Roda a imagem em até 360 graus

* **Luminosidade:** Converte a imagem RGB para tons de cinza.

* **Invert:** Inverte as cores de toda imagem em RGB ou tons de cinza.

* **Log:** Aumenta o birlho geral da imiagem pela transformação de intensidade logarítmica.

* **Gamma**: Ajusta o contraste de intensidades da imagem pela transformação gamma.

* **Contrast modulation:** Ajusta o contraste de intensidades da imagem pela transformação de modulação de contraste, recebendo dois intervalos

* **Efeito thermo image (função a mais adcionada nessa aplicação):** Aplica transformações simples para tirar uma imagem lúdica dos pontos com mais intensidade na imagem tendendno ao vermelho e os mais escuros tendendo ao azul, como se fosse uma visão de calor.


#### Exemplos de fotos editadas

- Aplicando rotação

![Passaro - original](imgs/originalImages/bird.jpg)

![Passaro - rotacionado](imgs/EditedImgs/bird.jpg)

- Escala e translação

![Cachorro - original](imgs/originalImages/dog.jpg)
![Cachorro - escalado e transladado](imgs/EditedImgs/dog.jpg)

- Mudando parametros da função Gamma

![Sol - original](imgs/originalImages/red-black.png)
![Sol - escurecido](imgs/EditedImgs/red-black.png)

- Aplicando o efeito `thermo image`

![Cyberpunk - original](imgs/originalImages/neon.jpg)
![Cyberpunk - thermo image](imgs/EditedImgs/neon.jpg)
