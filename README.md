# TFG
**Desarrollo de una Arquitectura de Plano de Control de Redes 6G para un Dominio WiFi**

Pasos a seguir para poder utilizarlo: Ejecutar el Servidor,  el AP_WiFi y el watchdogFlows no importa el orden, despues de esto ejecutar desde el cliente el comando python3 clienteEnvioJson-save.py para añadir una nueva configuración o python3 clienteEnvioJson-delete.py para eliminar una configuración.

- 1 En la maquina virtual del cliente hacer lo suguiente para poder enviar peticiones:
   - 1.1 Acceder a la carpeta cliente: cd cliente
   - 1.2 Para enviar peticiones para eliminar o añadir un nuevo recurso: python3 clienteEnvioJson-save.py, python3 clienteEnvioJson-delete.py(explicado más abajo).
- 2 En la maquina virtual del Servidor activar serverFlows de la siguiente manera :
   - 2.1 Activar el entorno virtual desde /home/emilio, comando:
     ```bash
     source venv/bin/activate
     ```
   - 2.2 Acceder a la carpeta serverFlows:
      ```bash
     cd serverFlows
      ```
   - 2.3 Activar el servidor:
     ```bash
     python3 serverFlows.py
     ```
- 3 En el AP_WiFi:
     - 3.1 Acceder a la carpeta:
        ```bash
       cd IntelWiFiConfigurator/AP_WiFi
        ```
     - 3.2 Activar el servidor:
       ```bash
       python3 AP.py
        ```
     - 3.3 Acceder a la carpeta Flows:
       ```bash
        cd Flows/
       ```
     - 3.4 Activar el watchdogFlows:
       ```bash
        python3 watchdogFlows.py
       ```

### Instrucciones para Añadir y Eliminar Servicios

### 1️ Añadir un Servicio

Para añadir una nueva configuración de servicio a la red WiFi, puedes utilizar el archivo de prueba `preparar_servicios_demo.txt`, donde encontrarás ejemplos de servicios que puedes usar como referencia.

El proceso consiste en:

1. Editar el archivo `clienteEnvioJson-save.py`, sustituyendo la sección `data = {}` con la configuración deseada.
2. Ejecutar el cliente con el siguiente comando:

```bash
python3 clienteEnvioJson-save.py
```
- Si se ha utilizado preparar_servicios_demo.txt, se puede verificar que los servicios se han añadido correctamente comparando la información recibida por el AP_WiFi con el contenido de servicios_demo.txt.

### 2 Eliminar un Servicio
Para eliminar una configuración de servicio a la red WiFi, edita `clienteEnvioJson-delete.py` y cambia el campo `"id"` por el del servicio que deseas eliminar. Luego ejecuta:
```bash
python3 clienteEnvioJson-delete.py
```

**Comandos interesantes:**
- Comandos para saber si los servidores están activos: ps aux | grep python3
- Para detener un servidor: kill -9 <PID_DEL_PROCESO>
