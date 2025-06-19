import json
import glob
import subprocess
import requests
from flask import request, jsonify
from datetime import datetime
from data_store import return_request_delete, evento_colas_estados_actualizadas, stored_data_colas_estado, stored_data

HISTORIAL_FILE = "flows_historial_*.txt"

# -------------------------------- Endpoint /delete -----------------------------
def delete_request():

    data = request.get_json()
    return_request_delete.clear() 
    return_request_delete.update({"skip": True})# Actualizar la variable global para evitar reenviar desde return-request
    stored_data.clear()        # Vaciar el diccionario actual
    print(f"El valor de saltar el endpoint return es:{return_request_delete} ")


    id_to_delete = data["id"]
    print(f"Eliminando recursos con ID: {id_to_delete}")

    # Buscar el historial más reciente que coincida con el patrón
    flow_historials = glob.glob(HISTORIAL_FILE)
    if not flow_historials:
        return jsonify({"error": "No se encontró historial"}), 404
    
    # Cargar el historial del archivo más reciente
    flow_historials_mas_reciente = flow_historials[0]
    with open(flow_historials_mas_reciente, "r") as f:
        try:
            historial = json.load(f)
        except json.JSONDecodeError:
            return jsonify({"error": "Error leyendo el historial"}), 500

    # -------------------------------- Eliminar flujos con el ID proporcionado --------------------------------
    historial_actualizado = []
    id_count=0
    for flujo in historial:
        if isinstance(flujo, dict):
            # Es un diccionario, eliminar solo si el ID no coincide
            if flujo.get("id") != id_to_delete:
                historial_actualizado.append(flujo)
            else:
                id_count += 1
    if id_count==0:
        return jsonify(data), 404
    

    #Eliminar cualquier archivo que comience con `flows_historial_`
    try:
        comando = ["bash", "-c", "rm -f flows_historial_*.txt"]
        subprocess.run(comando, check=True)
        print("Archivos flows_historial_* eliminados correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al eliminar archivos: {e}")

    # -------------------------------- Guardar el historial actualizado --------------------------------
    # Generar un nuevo nombre de archivo con timestamp
    timestamp = datetime.now().strftime('%d-%m-%Y_%H.%M.%S')
    nuevo_historial_file = f"flows_historial_{timestamp}.txt"

    # Guardar el historial actualizado
    with open(nuevo_historial_file, "w") as f:
        json.dump(historial_actualizado, f, indent=4, separators=(",", ": "))

    print(f"Historial actualizado y guardado en {nuevo_historial_file}.")

    # Preparar datos para enviar (sin ID)
    historial_sin_id = []
    for flujo in historial_actualizado:
        if isinstance(flujo, dict):  # Verificar que flujo sea un diccionario
            flujo_sin_id = {key: value for key, value in flujo.items() if key != "id"}
            historial_sin_id.append(flujo_sin_id)
    
    #-------------------Ahora aqui enviar el archivo al Ap del wifi con un POST-------------------------------- 
    try:
        response = requests.post("http://10.5.100.10:8080", json=historial_sin_id)
        if response.status_code == 200:
            print("Historial enviado correctamente.")

            # Esperar que se actualicen las colas (espera bloqueante con timeout)
            evento_colas_estados_actualizadas.clear()# Antes de esperar, aseguramos que el evento esté limpio
            evento_disponible = evento_colas_estados_actualizadas.wait(timeout=5)
            if not evento_disponible:
                print("Timeout esperando datos de colas.")
                return jsonify({"error": "Timeout esperando datos de colas"}), 500
            else:
                print("delete-request")
                estado = stored_data_colas_estado.get("estado")
                print(f"Este es el estado de configuracion:  {estado}")
                return jsonify(data), estado
        else:
            return jsonify({"error": "Error interno en delete_request"}), 500
    except Exception as e:
        print(f"Error al enviar el historial: {e}")
