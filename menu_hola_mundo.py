from flask import Flask, request, jsonify

app = Flask(__name__)

def imprimir_mensaje(opcion):
    if opcion == 1:
        return "Hola Mundo"
    elif opcion == 2:
        return "Hello World"
    elif opcion == 3:
        return "Ciao Mondo"
    else:
        return "Opción no válida"

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

@app.route('/hola_mundo', methods=['POST'])
def hola_mundo():
    data = request.json
    opcion = data.get('opcion', 0)
    mensaje = imprimir_mensaje(opcion)
    return jsonify({"message": mensaje})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
