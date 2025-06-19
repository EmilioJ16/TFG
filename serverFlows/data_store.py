from threading import Event

stored_data = {}# Variable compartida entre endpoints
stored_data_colas_estado = {}# Variable compartida entre endpoints
return_request_delete = {"skip": False}  # Variable para controlar si se envía o no el return-request
evento_colas_estados_actualizadas = Event()# Evento que se usará como semáforo
