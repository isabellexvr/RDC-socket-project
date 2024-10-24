import socket
import psutil  # Biblioteca para obter dados de uso de CPU, RAM, etc.
import time

# Função para obter dados do sistema (CPU, RAM e GPU simulada)
def get_system_data():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    gpu_usage = 45.5  # Simulação de uso de GPU
    return f"CPU: {cpu_usage}%, RAM: {ram_usage}%, GPU: {gpu_usage}%"

# Função para registrar como compartilhador
def register_as_sharer(client_socket):
    username = input("Escolha um username único para se cadastrar como compartilhador: ")
    client_socket.send(username.encode())
    
    response = client_socket.recv(1024).decode()
    print(response)
    
    if "sucesso" in response:
        print("Você agora está compartilhando seus dados do sistema...")
        try:
            while True:
                # Coleta e envia os dados do sistema a cada 5 segundos
                system_data = get_system_data()
                client_socket.send(system_data.encode())  # Envia os dados para o servidor
                print(f"Enviando: {system_data}")
                time.sleep(5)  # Intervalo de 5 segundos para envio dos dados
        except KeyboardInterrupt:
            print("Compartilhamento interrompido.")
            client_socket.close()
    else:
        print("Falha ao registrar o username. Tente novamente.")
        client_socket.close()

# Função para receber dados de um compartilhador específico
def request_sharer_data(client_socket):
    sharer_username = input("Digite o username do compartilhador cujos dados você quer acessar: ")
    client_socket.send(sharer_username.encode())

    try:
        while True:
            # Recebe os dados do servidor e exibe
            data = client_socket.recv(4096).decode()  # Aumente o buffer para 4096 bytes
            print(f"o que chegou do server {data}")
            if not data:
                print(f"Conexão encerrada com {sharer_username}.")
                break

            # Verifica se a mensagem está vazia ou não
            if data.strip():  # Verifica se os dados não são vazios
                print(data)  # Exibe os dados recebidos diretamente
            else:
                print(f"Nenhum dado recebido de {sharer_username}")
    except KeyboardInterrupt:
        print("Conexão encerrada.")
        client_socket.close()



# Função principal do cliente
def main():
    server_ip = input("Digite o IP do servidor: ")
    server_port = 12345  # Porta do servidor
    
    # Cria socket de conexão
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    # Recebe a mensagem inicial do servidor
    response = client_socket.recv(1024).decode()
    print(response)
    
    # Menu interativo
    option = input("Escolha (1) para cadastrar-se ou (2) para receber dados: ")
    client_socket.send(option.encode())

    if option == '1':
        register_as_sharer(client_socket)
    elif option == '2':
        request_sharer_data(client_socket)
    else:
        print("Opção inválida!")
        client_socket.close()

if __name__ == "__main__":
    main()
