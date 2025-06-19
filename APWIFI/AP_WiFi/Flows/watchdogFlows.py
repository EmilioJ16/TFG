import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import requests
import os

class WatchdogHandler(FileSystemEventHandler):
    def on_created(self, event):
        """
        Este método se llama cuando se crea un archivo en la carpeta monitoreada.
        """
        if event.is_directory:
            return 
        if event.src_path.endswith('.txt'):
            print(f"Nuevo archivo detectado: {event.src_path}")
            ultimo_fichero = os.path.basename(event.src_path)#nombre del fichero con los flujos
            try:
                # Leer el contenido del archivo y mostrarlo en pantalla
                with open(event.src_path, 'r') as f:
                    contenido = f.read()
                print(f"Contenido del archivo:\n{contenido}")
            except Exception as e:
                print(f"Error al leer el archivo: {e}")

            comando_1 = ["bash", "-c","python3 configurador.py -i wlp2s0 -u  --verbose"]
            comando_2 = ["bash", "-c",f"python3 configurador.py -i wlp2s0 -f {ultimo_fichero} --verbose"]
            comando_3 = ["bash","-c", "sudo tc -s qdisc show dev wlp2s0 | grep interval"]
            
            try:
                estado_http = 200
                resultado_1 = subprocess.run(comando_1, capture_output=True, text=True, check=False)
                if resultado_1.stdout.strip():
                    print(f"Salida de elimar la configuración actual:\n{resultado_1.stdout}.")
                else:
                    print(f"Al eliminar la configuración actual no se produjo ninguna salida.")

                resultado_2 = subprocess.run(comando_2, capture_output=True, text=True, check=False)
                if resultado_2.stdout.strip():
                    print(f"Salida de añadir la nueva configuración:\n{resultado_2.stdout}. Con comando: python3 configurador.py -i wlp2s0 -f \"{ultimo_fichero}\"t --verbose\n")
                else:
                    print(f"Salida al añadir la nueva configuracion: {resultado_2.stdout}\n"+
                          "El comando ejecutado es:"+f"python3 configurador.py -i wlp2s0 -f {ultimo_fichero} --verbose\n\n")

                resultado_3 = subprocess.run(comando_3, capture_output=True, text=True, check=False)
                salida_comando3 = resultado_3.stdout  # Extraer solo la salida (stdout)
                # Guardar la salida del tercer comando en un archivo
                timestamp = datetime.now().strftime('%d-%m-%Y_%H.%M.%S')
                nombre_archivo_salida = f"Colas/salida_comando_{timestamp}.txt"
                with open(nombre_archivo_salida, "w") as f:
                    f.write(salida_comando3)

                print(f"Salida del Comando 3 guardada en {nombre_archivo_salida}")
                print(salida_comando3)
                if resultado_2.returncode != 0:
                    estado_http = 500  # Error interno

                elif(salida_comando3==""):
                    estado_http = 422

                datos_post = {
                    "salida": salida_comando3,
                    "estado": estado_http
                }
                try:

                    #-------------------Ahora aqui enviamos el resultado de las colas a la vm/-------------------------------- 
                    response = requests.post("http://10.5.15.76:8080/return-request", json=datos_post)
                    if response.status_code == 200:
                        print("Historial enviado correctamente.")
                    else:
                        print(f"Error al enviar el historial: {response.status_code}")
                except Exception as e:
                    print(f"Error al enviar el historial: {e}")

            except subprocess.CalledProcessError as e:
                print(f"Error al ejecutar un comando: {e}")




def monitorear_carpeta(carpeta):
    """
    Configura el watchdog para monitorear una carpeta específica.
    """
    # Crear el observador
    observer = Observer()
    handler = WatchdogHandler()
    observer.schedule(handler, carpeta, recursive=False)

    # Iniciar el observador
    observer.start()
    print(f"Monitoreando la carpeta: {carpeta}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Deteniendo el observador...")
        observer.stop()

    observer.join()

if __name__ == "__main__":
    carpeta_a_monitorear = "/home/netcom/IntelWiFiConfigurator/AP_WiFi/Flows"
    monitorear_carpeta(carpeta_a_monitorear)
