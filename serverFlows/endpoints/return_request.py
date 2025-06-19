from flask import request
import requests
from data_store import stored_data, return_request_delete, stored_data_colas_estado, evento_colas_estados_actualizadas # Importar la variable global
import re

def return_request():
    """
    Endpoint que recibe el estado y configuración de colas para actualizar el JSON almacenado en `stored_data`,
    luego lo reenvía al cliente.
    """
    global stored_data
    global return_request_delete
    global stored_data_colas_estado

    data_colas_estado = request.get_json()

    data_colas = data_colas_estado.get("salida", "")
    estado = data_colas_estado.get("estado", 0)
    print("return-request")
    print(f"Recibido estado HTTP de comandos: {estado}")
    print(f"Salida del comando:\n{data_colas}")

    print(f"El valor de saltar el endpoint return es:{return_request_delete} ")

    if return_request_delete.get("skip", True):#Si es una petecion de delete hacemos esto.

        print("Se ha eliminado un recurso.")
        return_request_delete.clear()  # Restablecer flag después de usarlo
        return_request_delete.update({"skip": False})
        if data_colas=="":
            estado=500
        else:
            data_colas=200
        datos_configuracion = {
            "json": "",
            "estado": estado
        }
        stored_data_colas_estado.clear()
        stored_data_colas_estado.update(datos_configuracion) 
        evento_colas_estados_actualizadas.set()
        return "OK", 200
    else:#Si es una peticion de save hacemos esto.
        
        print(f"Se ha añadido un recurso")
        valores_interval = re.findall(r'interval (\d+)', data_colas)
        print(valores_interval)

        node_list = stored_data["td_path_selection"]["involved_nodes"]["node_list"]

        # Guardar la lista completa de intervalos en todos los nodos, FUNCIONA
        for idx, nodo in enumerate(node_list):
            for i, valor in enumerate(valores_interval):
                # Se asigna cada valor en su posición correspondiente en la lista resource_list del nodo.
                nodo["node_resources"]["resource_list"][f"c{i}"] = valor

        
        datos_configuracion = {
            "json": stored_data,
            "estado": estado
        }
        
        stored_data_colas_estado.clear()
        stored_data_colas_estado.update(datos_configuracion)   # Actualizar con los nuevos datos
        print(datos_configuracion.get("json"))        
        # Activar el evento
        evento_colas_estados_actualizadas.set()
        return "OK", 200
