from flask import Flask, request
from waitress import serve
from datetime import datetime
import json

app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle_post():
    
    try:
        data = request.get_json()
        if data is None:
            return "Formato JSON no válido", 400

        timestamp = datetime.now().strftime('%d-%m-%Y_%H.%M.%S')
        filename = f"Flows/flows_{timestamp}.txt"

        with open(filename, "w") as f:
            json.dump(data, f, indent=4, separators=(",", ": "))

        return f"Historial recibido y guardado en {filename}", 200
    

    except Exception as e:
        return f"Error procesando la solicitud: {e}", 400



if __name__ == '__main__':
    serve(app, host='10.5.100.10', port=8080)