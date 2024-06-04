import socket

SERVER_HOST = "localhost"  # IP del servidor
SERVER_PORT = 8080  # Puerto del servidor


def enviar_mensaje(mensaje):
    """
    Envia un mensaje al servidor.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    client_socket.sendall(mensaje.encode("utf-8"))
    client_socket.close()


if __name__ == "__main__":
    mensaje = input("Ingrese el mensaje a enviar al servidor: ")
    enviar_mensaje(mensaje)
