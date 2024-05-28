# Usar uma imagem base oficial do Python
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /usr/src/app

# Copiar o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt ./

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação
COPY . .

# Expor a porta que a aplicação irá rodar
EXPOSE 5000

# Comando para rodar a aplicação usando Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]