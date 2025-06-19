import requests

url = 'http://10.5.15.76:8080/delete-request'
data = {
    "id": "1112",#id del servicio para identificarlo y eliminarlo.
    "e2e_service_id": "33333",
    "td_path_selection": {
        "path_id": "carretera1",
        "path_status": "provisioned",
        "involved_nodes": {
            "node_list": [
                {
                    "id": "tractor",
                    "node_resources": {
                        "resource_list": {}
                    }
                },
                {
                    "id": "amarillo",
                    "node_resources": {
                        "resource_list": {}
                    }
                }
            ]
        }
    },
    "qos_characteristics": {
        "priority": 7,
        "td_reliability": 100,
        "td_packet_loss": 10,
        "td_delay": 50,
        "td_rtt": 300,
        "td_jitter": 42,
        "burst_arrival_time_window": {
            "t1": 5,
            "t2": 10
        },
        "burst_completion_time_window": {
            "t1": 6,
            "t2": 12
        }
    },
    "traffic_characteristics": {
        "direction": "bidirectional",
        "periodicity": False,
        "period": 50,
        "burst_size": 20,
        "maximum_flow_bitrate": 5000
    }
}

# Enviar la solicitud POST
response = requests.post(url, json=data)

# Imprimir la respuesta del servidor
print("Código de estado:", response.status_code)
print("Respuesta del servidor:", response.text)
