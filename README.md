# PhotoCanva

Originalmente pensado como um pequeno projeto da disciplina SCC0251 - Processamento de imagens, essa é uma pequena aplicação Web interativa para editar imagens!

## Autor

* Gabriel Antunes Afonos de Araujo

* Nº USP: 14571077

## Estrutura do projeto

**API:** Pasta que contem a API em camadas do backend

**Frontend:** Pasta que contem o frontend da aplicação

## Funcionalidades do projeto

Esse projeto consiste em um pequeno editor de imagens em tempo real pela web, possuindo uma aplicação frontend que comunica cada alteração por mensagens individuais a API, a qual pega o último estado salvo da imagem e aplica as novas alterações seguindo um `pipeline` interno. Ao fim, é possível obter terminar a edição baixando a imagem final na resolução original.

#### Fluxo de edição

1. Clique em 'carregar imagem' ao abrir o sitie, e escolhe a imagem a ser editada.

2. Clique em 'iniciar edição' para levar a imagem a pagina de edição.

3. No canto mais a esqurda, você verá uma barra lateral com ícones. Essa é a `Toolbar`, contendo os grupos de ferramentas de edição: Geométricas, transformações de intensidade e efeitos visuais, respectivamente

4. Va para o grupo de ferramentas e brinque com os inputs e parâmetros para fazer a sua edição!

5. Ao fim, clique em Download para terminar o processo. O site baixará a imagem para sua pasta `downloads` e voltará a página inicial.

#### Lista das principais funções

* **Translação:** Translada em aplica o zoom necessário na imagem para impedir pixeis vaios, tanto em X quanto em Y.

* **Escala:** Aplica uma escala com fator x e y espressos pelo usuário 

* **Rotação**: Roda a imagem em até 360 graus

* **Luminosidade:** Converte a imagem RGB para tons de cinza.

* **Invert:** Inverte as cores de toda imagem em RGB ou tons de cinza.

* **Log:** Aumenta o birlho geral da imiagem pela transformação de intensidade logarítmica.

* **Gamma**: Ajusta o contraste de intensidades da imagem pela transformação gamma.

* **Contrast modulation:** Ajusta o contraste de intensidades da imagem pela transformação de modulação de contraste, recebendo dois intervalos

* **Efeito thermo image:** Aplica transformações simples para tirar uma imagem lúdica dos pontos com mais intensidade na imagem tendendno ao vermelho e os mais escuros tendendo ao azul, como se fosse uma visão de calor.

## Dependências para rodar

* docker
* docker compose

## Como rodar

1. Inicialize o Docker na máquina (`systemctl start docker` no Linux, ou `open -a docker` no macOS)

2. Execute o Docker Compose para iniciar os serviços: `docker compose up`

3. Acesse a aplicação em `http://localhost:80`
