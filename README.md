[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/imhTmAOP)

## Link da imagem do Dockerhub

    https://hub.docker.com/repository/docker/gustavotakahashi/f1club2024/general

## Rodar Projeto em usando a Imagem do Docker Hub

    Baixar imagem 
        $ docker pull gustavotakahashi/f1club2024:latest
        $ docker compose up -d
        $ docker exec -it f1club2024-web python manage.py migrate

    Backend  ficará disponível em http://localhost:8000


## Comandos

    Aplicar Migrações
        $ docker exec -it f1club2024-web python manage.py migrate

    Parar os Containers
        $ docker-compose down

    Reiniciar os Containers
        $ docker-compose up --build

    Acessar Logs
        $ docker-compose logs

    Criar Superusuário
        $ docker exec -it f1club2024-web python manage.py createsuperuser