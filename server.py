import socket
import threading
import time
import psutil

# Dicionário para armazenar os compartilhadores e seus dados
compartilhadores = {}

def handle_client(client_socket):
    try:
        client_socket.send("Você quer (1) Cadastrar-se ou (2) Receber dados? (Digite 1 ou 2)\n".encode())
        option = client_socket.recv(1024).decode().strip()

        if option == '1':
            username = client_socket.recv(1024).decode().strip()

            if username in compartilhadores:
                client_socket.send("Username já utilizado! Tente novamente.\n".encode())
            else:
                compartilhadores[username] = {
                    'socket': client_socket,
                    'dados': ''  # Inicializa os dados vazios
                }
                client_socket.send(f"Username {username} cadastrado com sucesso!\n".encode())
                client_socket.send("Agora seus dados estão sendo compartilhados...\n".encode())

                while True:
                    try:
                        # O compartilhador envia os dados ao servidor
                        data = client_socket.recv(4096).decode().strip()  # Espera dados do compartilhador
                        if not data:
                            print(f"O usuário {username} desconectou.")
                            break  # Sai do loop se a conexão for encerrada

                        print(f"dados recebidos: {data}")
                        compartilhadores[username]['dados'] = data  # Atualiza os dados do compartilhador

                    except (ConnectionResetError, BrokenPipeError):
                        print(f"O usuário {username} se desconectou de forma abrupta.")
                        break  # Sai do loop em caso de erro de conexão

                    time.sleep(1)  # Ajuste o tempo conforme necessário

        elif option == '2':
            username = client_socket.recv(1024).decode().strip()
            print(f"username inputado: {username}")

            if username in compartilhadores:
                client_socket.send(f"Conectado ao compartilhador {username}. Aguardando dados...\n".encode())
                while True:
                    dados = compartilhadores[username]['dados']
                    if dados:  # Verifica se há dados para enviar
                        client_socket.send(f"Dados de {username}: {dados}\n".encode())
                    time.sleep(5)  # Evita flood e envia os dados a cada 5 segundos
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
    # Inicia uma nova thread para lidar com cada cliente conectado
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
