FROM node:20-alpine

WORKDIR /app

# Copia os arquivos de pacotes e instala tudo
COPY package*.json ./
RUN npm ci

# Copia o restante do código
COPY . .

# Compila o projeto (Gera a pasta .svelte-kit)
RUN npm run build

# Expõe a porta padrão que o SvelteKit usa em produção (normalmente 3000 ou 4173)
EXPOSE 4173

# Comando para rodar o servidor de produção do SvelteKit
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0"]
