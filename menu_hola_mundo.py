from flask import Flask, request, jsonify
import logging
from healthcheck import HealthCheck

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.app_context().push()

# Configuración del HealthCheck
health = HealthCheck()

# Función de verificación de salud
def app_working():
    return True, "App is working"

# Añadir la verificación de salud
health.add_check(app_working)

# Configura el endpoint de healthcheck manualmente
app.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())

# Función para imprimir mensajes en diferentes idiomas
def imprimir_mensaje(opcion):
    if opcion == 1:
        return "Hola Mundo"
    elif opcion == 2:
        return "Hello World"
    elif opcion == 3:
        return "Ciao Mondo"
    else:
        return "Opción no válida"

# Endpoint para mostrar el menú de opciones
@app.route('/menu', methods=['GET'])
def mostrar_menu():
    return jsonify({
        "message": "Selecciona un idioma para imprimir 'Hola Mundo':",
        "options": {
            "1": "Español",
            "2": "Inglés",
            "3": "Italiano"
        }
    })

# Endpoint para mostrar el mensaje en el idioma seleccionado
@app.route('/hola_mundo', methods=['POST'])
def hola_mundo():
    data = request.json
    opcion = data.get('opcion', 0)
    mensaje = imprimir_mensaje(opcion)
    return jsonify({"message": mensaje})

# Endpoint de prueba
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
