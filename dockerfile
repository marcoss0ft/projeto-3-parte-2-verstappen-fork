# Usar Python como base
FROM python:3.10-slim

# Configurar o diretório de trabalho no container
WORKDIR /app

# Atualizar e instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean

# Copiar arquivos para o container
COPY . /app

# Atualizar pip e instalar dependências do Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expôr a porta do Django
EXPOSE 8000

# Comando para rodar o servidor do Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]