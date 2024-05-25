# Stage 1: Build the application
FROM maven:3.8.4-openjdk-17 AS build
WORKDIR /app
COPY . .
RUN mvn clean package

# Stage 2: Create a minimal JRE image with the built artifact
FROM openjdk:17-jdk-slim
WORKDIR /app
COPY --from=build /app/target/Calculator-*.jar app.jar
EXPOSE 8080
CMD ["java", "-jar", "app.jar"]
