import requests

url = 'http://10.5.15.76:8080/save-request'
data = {
    "id": "1111",#id del servicio
    "e2e_service_id": "3333",
    "td_path_selection": {
        "path_id": "carretera1",
        "path_status": "provisioned",
        "involved_nodes": {
            "node_list": [
                {
                    "id": "WIFI_AP",
                    "node_resources": {
                        "resource_list": {}
                    }
                },
                {
                    "id": "WIFI_STA",
                    "node_resources": {
                        "resource_list": {}
                    }
                }
            ]
        }
    },
    "qos_characteristics": {
        "priority": 1,#type
        "td_reliability": 100,
        "td_packet_loss": 10,
        "td_delay": 1500,#latency_constraint
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
        "periodicity": True,
        "period": 50,#time
        "burst_size": 1000,#size
        "maximum_flow_bitrate": 5000
    }
}

# Enviar la solicitud POST
response = requests.post(url, json=data)

# Imprimir la respuesta del servidor
print("Código de estado:", response.status_code)
print("Respuesta del servidor:", response.text)
