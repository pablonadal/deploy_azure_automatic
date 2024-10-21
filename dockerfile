# Utilizar una imagen base de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar Flask
RUN pip install flask

# Copiar el archivo de tu aplicación al contenedor
COPY menu_hola_mundo.py .

# Especificar el comando por defecto para ejecutar tu script
CMD ["python", "menu_hola_mundo.py"]
