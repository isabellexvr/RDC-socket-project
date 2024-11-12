import flet as ft
import socket
import psutil
import time
import threading

def get_system_data():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    gpu_usage = 45.5  # Simulação de uso de GPU
    return f"CPU: {cpu_usage}%, RAM: {ram_usage}%, GPU: {gpu_usage}%"

def register_as_sharer(client_socket, username, output_text):
    print("Sending '1' for sharer registration")
    client_socket.send("1".encode())  # Send "1" for sharer
    response1 = client_socket.recv(1024).decode()
    print("Response after sending '1':", response1)
    
    # Send the username immediately after receiving response1
    print("Sending username:", username)
    client_socket.send(username.encode())
    response2 = client_socket.recv(1024).decode()
    print("Response after sending username:", response2)
    
    # Ensure response is correctly referenced
    if "sucesso" in response2:
        print("entrou no if")
        output_text.value = "Você agora está compartilhando seus dados do sistema...\n"
        output_text.update()
        try:
            while True:
                system_data = get_system_data()
                client_socket.send(system_data.encode())
                output_text.value = f"Enviando: {system_data}\n"
                output_text.update()
                time.sleep(5)
        except KeyboardInterrupt:
            output_text.value = "Compartilhamento interrompido.\n"
            output_text.update()
            client_socket.close()
    else:
        output_text.value = "Falha ao registrar o username. Tente novamente.\n"
        output_text.update()
        client_socket.close()

def request_sharer_data(client_socket, sharer_username, output_text):
    client_socket.send("2".encode())  # Send "2" for requester
    response1 = client_socket.recv(1024).decode()
    print("Response after sending '2':", response1)

    print("Sending username:", sharer_username)
    client_socket.send(sharer_username.encode())
    response2 = client_socket.recv(1024).decode()
    print("Response after sending username:", response2)
    try:
        while True:
            data = client_socket.recv(4096).decode()
            output_text.value = f"{data}\n"
            output_text.update()
            if not data:
                output_text.value = f"Conexão encerrada com {sharer_username}.\n"
                output_text.update()
                break
    except KeyboardInterrupt:
        client_socket.close()

def main(page: ft.Page):
    page.title = "System Data Sharing Client"
    
    username_input = ft.TextField(label="Username")
    sharer_username_input = ft.TextField(label="Sharer Username")
    output_text = ft.Text()
    
    def on_register_click(e):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 12345))
        register_as_sharer(client_socket, username_input.value, output_text)

    def on_request_click(e):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 12345))
        request_sharer_data(client_socket, sharer_username_input.value, output_text)

    register_button = ft.ElevatedButton(text="Register as Sharer", on_click=on_register_click)
    request_button = ft.ElevatedButton(text="Request Sharer Data", on_click=on_request_click)
    
    page.add(username_input, register_button, sharer_username_input, request_button, output_text)

ft.app(target=main)