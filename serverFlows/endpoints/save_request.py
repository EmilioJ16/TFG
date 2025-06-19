from flask import request, jsonify
import json
from datetime import datetime
import requests
import glob
import subprocess
from data_store import stored_data, return_request_delete, stored_data_colas_estado,  evento_colas_estados_actualizadas

MACS = [ {"sender": "00:11:22:33:44:56", "receivers": ["66:77:88:99:AA:BC"]} ]

# Archivo inicial del historial
HISTORIAL_FILE = "flows_historial_*.txt"

# -------------------------------- Endpoint /save-request -----------------------------
def save_request():
    global HISTORIAL_FILE
    global stored_data, return_request_delete, stored_data_colas_estado # Declaramos que vamos a modificar la variable global
    

    return_request_delete.clear() 
    return_request_delete.update({"skip": False})
    data = request.get_json()
    stored_data.clear()
    stored_data.update(data)

    # Generar timestamp para el nombre del archivo
    timestamp = datetime.now().strftime('%d-%m-%Y_%H.%M.%S')

    # Crear un archivo separado para este flujo
    nuevo_archivo = f"flows_{timestamp}.txt"

    # Extraer datos del JSON
    id = data["id"]
    qos = data["qos_characteristics"]
    traffic = data["traffic_characteristics"]

    latency_constraint = str(qos["td_delay"])
    priority =str(qos["priority"])
    time_interval = str(traffic["period"])
    size = str(traffic["burst_size"])
     
    if priority == "7":
        traffic_type="TSN"
    else:
        traffic_type="BEST_EFFORT"  

    # Construir el flujo para este archivo
    flows = []
    for mac in MACS:
        flow = {
            "id": id,
            "sender": mac["sender"],
            "receivers": mac["receivers"],
            "creation_type": "MULTICAST" if len(mac["receivers"]) > 1 else "UNICAST",
            "latency_constraint": latency_constraint,
            "size": size,
            "time": time_interval,
            "type": traffic_type
        }
        flows.append(flow)

    # Guardar el flujo en un archivo separado
    with open(nuevo_archivo, "w") as f:
        json.dump(flows, f, indent=4, separators=(",", ": "))
        
    # Actualizar el nombre del historial para reflejar el nuevo timestamp
    historial_sin_id = guardar_historial(flows, HISTORIAL_FILE)

    #-------------------Ahora aqui enviar el archivo al Ap del wifi con un POST-------------------------------- 
    try:
        response = requests.post("http://10.5.100.10:8080", json=historial_sin_id)
        if response.status_code == 200:
            # Esperar que se actualicen las colas (espera bloqueante con timeout)
            evento_colas_estados_actualizadas.clear()# Antes de esperar, aseguramos que el evento esté limpio
            evento_disponible = evento_colas_estados_actualizadas.wait(timeout=5)
            if not evento_disponible:
                print("Timeout esperando datos de colas.")
                return jsonify({"error": "Timeout esperando datos de colas"}), 500
            else: 
                print("save-request")
                data_colas = stored_data_colas_estado.get("json")
                estado = stored_data_colas_estado.get("estado")
                print(f"Esto son las colas configuradas:  {data_colas}")
                print(f"Este es el estado de configuracion:  {estado}")
                return jsonify(data_colas), estado
        else:
            return jsonify({"error": "Error interno en save_request"}), 500
    except Exception as e:
        print(f"Error al enviar el historial: {e}")
        return jsonify({"error": "Error interno en save_request"}), 500

    

# -------------------------------- Función para actualizar y guardar el historial -----------------------------
def guardar_historial(nuevo_flow, historial_file):
    historial = []
    
    # Buscar archivos que coincidan con el patrón
    flow_historials = glob.glob(historial_file)
    
    if flow_historials:
        flow_historials_mas_reciente = flow_historials[0]
        with open(flow_historials_mas_reciente, "r") as f:
            try:
                historial = json.load(f)
                # Agregar el nuevo flujo al historial
                historial.extend(nuevo_flow)
            except json.JSONDecodeError:
                print("Error leyendo el historial, iniciando desde cero.")
                historial = []
    else:
        print("No se encontró historial existente, iniciando desde cero.")
        historial.extend(nuevo_flow)

    #Eliminar cualquier archivo que comience con `flows_historial_`
    try:
        comando = ["bash", "-c", "rm -f flows_historial_*.txt"]
        subprocess.run(comando, check=True)
        print("Archivos flows_historial_* eliminados correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al eliminar archivos: {e}")

    # Guardar el historial completo en el archivo actualizado
    timestamp = datetime.now().strftime('%d-%m-%Y_%H.%M.%S')
    flow_historials_mas_reciente = f"flows_historial_{timestamp}.txt"
    with open(flow_historials_mas_reciente, "w") as f:
        json.dump(historial, f, indent=4, separators=(",", ": "))

    # Preparar datos para enviar (sin ID)
    historial_sin_id = []
    for flujo in historial:
        if isinstance(flujo, dict):  # Verificar que flujo sea un diccionario
            flujo_sin_id = {key: value for key, value in flujo.items() if key != "id"}
            historial_sin_id.append(flujo_sin_id)


    print(f"Historial actualizado y guardado en {historial_file}.")

    return historial_sin_id
