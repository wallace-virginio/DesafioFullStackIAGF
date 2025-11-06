# Usa a imagem oficial do Node
FROM node:18-alpine

WORKDIR /app

# Instala o Angular CLI globalmente
RUN npm install -g @angular/cli

# Copia o package.json e instala as dependências
COPY package*.json ./
RUN npm install

# Copia o resto do código da aplicação
COPY . .

# Expõe a porta do Angular
EXPOSE 4200