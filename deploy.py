from dotenv import load_dotenv
import os
import subprocess
import random

# Cargar las variables desde el archivo .env
load_dotenv()

# Obtener variables desde el entorno
IMAGE_NAME = os.getenv("IMAGE_NAME")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")
IMAGE_TAG = os.getenv("IMAGE_TAG")
RESOURCE_GROUP = os.getenv("RESOURCE_GROUP")
LOCATION = os.getenv("LOCATION")
ACR_NAME = os.getenv("ACR_NAME")
PORT_CONTAINER = int(os.getenv("PORT_CONTAINER"))

# Crear Grupo de Recursos
subprocess.run(["az", "group", "create", "--name", RESOURCE_GROUP, "--location", LOCATION])

# Crear Registro de Contenedores en Azure (ACR)
subprocess.run(["az", "acr", "create", "--resource-group", RESOURCE_GROUP, "--name", ACR_NAME, "--sku", "Basic"])
subprocess.run(["az", "acr", "login", "--name", ACR_NAME])

# Obtener ID del Registro de ACR
ACR_REGISTRY_ID = subprocess.run(["az", "acr", "show", "--name", ACR_NAME, "--query", "id", "--output", "tsv"], capture_output=True, text=True).stdout.strip()

# Crear Identidad de Servicio
SERVICE_PRINCIPAL_NAME = "universidad"
USER_NAME = subprocess.run(["az", "ad", "sp", "list", "--display-name", SERVICE_PRINCIPAL_NAME, "--query", "[].appId", "--output", "tsv"], capture_output=True, text=True).stdout.strip()
PASSWORD = subprocess.run(["az", "ad", "sp", "create-for-rbac", "--name", SERVICE_PRINCIPAL_NAME, "--scopes", ACR_REGISTRY_ID, "--role", "acrpull", "--query", "password", "--output", "tsv"], capture_output=True, text=True).stdout.strip()


# Construir, Etiquetar y Publicar la Imagen Docker
subprocess.run(["docker", "build", "-t", f"{IMAGE_NAME}:{IMAGE_TAG}", "."])
subprocess.run(["docker", "tag", f"{IMAGE_NAME}:{IMAGE_TAG}", f"{ACR_NAME}.azurecr.io/{IMAGE_NAME}:{IMAGE_TAG}"])
subprocess.run(["docker", "push", f"{ACR_NAME}.azurecr.io/{IMAGE_NAME}:{IMAGE_TAG}"])

# Listar Repositorios en ACR
subprocess.run(["az", "acr", "repository", "list", "--name", ACR_NAME, "--output", "table"])

# Crear y Desplegar Contenedor en Azure
dns_name_label = f"dns-um-{random.randint(1000, 9999)}"
subprocess.run([
    "az", "container", "create", 
    "--resource-group", RESOURCE_GROUP, 
    "--name", CONTAINER_NAME, 
    "--image", f"{ACR_NAME}.azurecr.io/{IMAGE_NAME}:{IMAGE_TAG}", 
    "--cpu", "1", 
    "--memory", "1", 
    "--registry-login-server", f"{ACR_NAME}.azurecr.io", 
    "--ip-address", "Public", 
    "--location", LOCATION, 
    "--registry-username", USER_NAME, 
    "--registry-password", PASSWORD, 
    "--dns-name-label", dns_name_label, 
    "--ports", str(PORT_CONTAINER)
])
