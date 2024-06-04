import socket
import threading


class Servidor:
    """
    :Descripcion:
        Clase que genera una servidor para que distintos clientes se conecten a el.
    """

    def __init__(self, host, puerto):
        self.host = host
        self.puerto = puerto
        self.log_file = "server_log.txt"
        self.server_socket = None
        self.server_thread = None
        self.activo = False

    def registrar_log(self, mensaje):
        """
        Registra el mensaje en un log.
        """
        with open(self.log_file, "a") as log_file:
            log_file.write(f"{mensaje}\n")

    def iniciar_servidor(self):
        """
        Activa el servidor y el hilo que lo mantendra activo mientras hacemos otras tareas.
        """
        self.activo = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.puerto))
        self.server_socket.listen(1)
        print(
            "Servidor Activo. Esperando conexiones en: ",
            self.host,
            "puerto:",
            self.puerto,
        )
        self.server_thread = threading.Thread(target=self._escuchar)
        self.server_thread.start()

    def _escuchar(self):
        """
        Escuchara conexiones/mensajes de clientes mientras el servidor este activo.
        """
        while self.activo:
            try:
                client_socket, client_address = self.server_socket.accept()
                print("Conexión establecida desde", client_address)
                mensaje = client_socket.recv(1024).decode("utf-8")
                self.registrar_log(
                    f"Mensaje recibido desde {client_address}: {mensaje}"
                )
                if mensaje == "apagar":
                    self.apagar_servidor()
                    break
                client_socket.close()
            except OSError:
                if self.activo:
                    self.registrar_log("Error al aceptar conexion del cliente")
                else:
                    self.registrar_log("El servidor fue apagado")

    def apagar_servidor(self):
        """
        Finaliza el servidor y el hilo.
        """
        if self.activo:
            self.activo = False
            self.registrar_log("Servidor apagado")
            self.server_socket.close()
            self.server_thread.join()
            print("Servidor apagado")
