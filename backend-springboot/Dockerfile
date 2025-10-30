# Estágio 1: Compila a aplicação com o Maven
FROM maven:3.8.5-openjdk-17 AS build

# Copia os fontes e o pom.xml
WORKDIR /app
COPY . .

# Compila e gera o .jar
RUN mvn clean package -DskipTests

# Estágio 2: Cria a imagem final (menor)
FROM openjdk:17-jdk-slim

# Copia o .jar gerado no estágio anterior
COPY --from=build /app/target/*.jar app.jar

# Expõe a porta que o Spring vai usar
EXPOSE 8080

# Comando para rodar a aplicação
ENTRYPOINT ["java", "-jar", "/app.jar"]