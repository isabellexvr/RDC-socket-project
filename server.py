import socket
import threading
import time
import psutil


compartilhadores = {}

def handle_client(client_socket):
    try:
        option = client_socket.recv(1024).decode().strip()
        print("sent option: ", option)

        if option == '1':
            client_socket.send("Envie seu username:\n".encode())
            username = client_socket.recv(1024).decode().strip()
            print("Received username:", username)
            if username in compartilhadores:
                client_socket.send("Username já utilizado! Tente novamente.\n".encode())
            else:
                compartilhadores[username] = {
                    'socket': client_socket,
                    'dados': ''
                }
                client_socket.send(f"sucesso!\n".encode())

                while True:
                    try:
                        data = client_socket.recv(4096).decode().strip()
                        if not data:
                            print(f"O usuário {username} desconectou.")
                            break
                        compartilhadores[username]['dados'] = data
                    except (ConnectionResetError, BrokenPipeError):
                        print(f"O usuário {username} se desconectou de forma abrupta.")
                        break
                    time.sleep(1)

        elif option == '2':
            client_socket.send("Envie seu username:\n".encode())
            username = client_socket.recv(1024).decode().strip()
            print("Received username:", username)
            if username in compartilhadores:
                client_socket.send(f"Conectado ao compartilhador {username}. Aguardando dados...\n".encode())
                while True:
                    dados = compartilhadores[username]['dados']
                    if dados:
                        client_socket.send(f"{dados}".encode())
                    time.sleep(5)
            else:
                client_socket.send("Username não encontrado.\n".encode())
    except Exception as e:
        print(f"Erro: {e}")
        client_socket.close()



# Configuração do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(5)
print("Servidor escutando na LAN...")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Conexão de {addr}")
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
