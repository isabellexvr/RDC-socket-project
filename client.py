import flet as ft
import socket
import psutil
import time
import threading

def get_system_data():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    gpu_usage = 45.5  # Simulação de uso de GPU
    return f"{cpu_usage}|{ram_usage}|{gpu_usage} aaaaa"

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
        output_text.value = "Você agora está compartilhando seus dados do sistema...\n"
        output_text.update()
        try:
            while True:
                system_data = get_system_data()
                send_system_data(client_socket, system_data, output_text)
                time.sleep(5)
        except KeyboardInterrupt:
            output_text.value = "Compartilhamento interrompido.\n"
            output_text.update()
            client_socket.close()
    else:
        output_text.value = "Falha ao registrar o username. Tente novamente.\n"
        output_text.update()
        client_socket.close()

def send_system_data(client_socket, system_data, output_text):
    client_socket.send(system_data.encode())
    output_text.value = f"Enviando: {system_data}\n"
    output_text.update()

def request_sharer_data(client_socket, sharer_username, output_text):
    client_socket.send("2".encode())  # Send "2" for requester
    response1 = client_socket.recv(1024).decode()
    print("Response after sending '2':", response1)

    print("Sending username:", sharer_username)
    client_socket.send(sharer_username.encode())
    response2 = client_socket.recv(1024).decode()
    print("Response after sending username:", response2)

 

def main(page: ft.Page):
    page.title = "System Data Sharing Client"
    
    
    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("MSI de Probe"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.ElevatedButton("Iniciar", on_click=lambda _: page.go("/server_ip")),
                ],
            )
        )
        if page.route == "/as_sharer":
            username_input = ft.TextField(label="Username")
            output_text = ft.Text()
            
            def on_register_click(e):
                register_as_sharer(client_socket, username_input.value, output_text)
            
            register_button = ft.ElevatedButton(text="Register as Sharer", on_click=on_register_click)
            page.views.append(
                ft.View(
                    "/as_sharer",
                    [
                        ft.AppBar(title=ft.Text("Register as Sharer"), bgcolor=ft.colors.SURFACE_VARIANT),
                        username_input,
                        register_button,
                        output_text,
                    ],
                )
            )
        if page.route == "/requester":
            sharer_username_input = ft.TextField(label="Sharer Username")
            output_text = ft.Text()
            
            def on_request_click(e):
                request_sharer_data(client_socket, sharer_username_input.value, output_text)
                page.go("/show_data")
            
            request_button = ft.ElevatedButton(text="Request Sharer Data", on_click=on_request_click)
            page.views.append(
                ft.View(
                    "/requester",
                    [
                        ft.AppBar(title=ft.Text("Request Sharer Data"), bgcolor=ft.colors.SURFACE_VARIANT),
                        sharer_username_input,
                        request_button,
                        output_text,
                    ],
                )
            )
        if page.route == "/home":
            sharer_button = ft.ElevatedButton("Register as Sharer", on_click=lambda _: page.go("/as_sharer"))
            requester_button = ft.ElevatedButton("Request Sharer Data", on_click=lambda _: page.go("/requester"))
            page.views.append(
                ft.View(
                    "/home",
                    [
                        ft.AppBar(title=ft.Text("Choose Role"), bgcolor=ft.colors.SURFACE_VARIANT),
                        sharer_button,
                        requester_button,
                    ],
                )
            )
        if page.route == "/server_ip":
            ip_input = ft.TextField(label="Server IP")
            alert_text = ft.Text(color=ft.colors.RED)
            
            def submit_ip(ip):
                ip_value = ip
                try:
                    print("passou\n")
                    global client_socket
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((ip_value, 12345))
                    page.go("/home")
                except Exception as e:
                    alert_text.value = f"Erro ao conectar: {e}"
                    alert_text.update()
                
            submit_button = ft.ElevatedButton("Submit", on_click=lambda _: submit_ip(ip_input.value))
            #home_button = ft.ElevatedButton("Vai", on_click=lambda _: page.go())
            page.views.append(
            ft.View(
                "/server_ip",
                [
                ft.AppBar(title=ft.Text("Enter Server IP"), bgcolor=ft.colors.SURFACE_VARIANT),
                ip_input,
                submit_button,
                alert_text,
                ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                ],
            )
            )
        if page.route == "/show_data":
            output_text = ft.Text()
            page.views.append(
            ft.View(
                "/show_data",
                [
                ft.AppBar(title=ft.Text("System Data"), bgcolor=ft.colors.SURFACE_VARIANT),
                output_text,
                ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                ],
            )
            )
            def receive_data():
                try:
                    while True:
                        data = client_socket.recv(4096).decode()
                        teste = data.split("|")
                        
                        print(teste)
                        output_text.value = f"{data}\n"
                        output_text.update()
                        
                        #print(output_text.value)
                        
                        if not data:
                            output_text.value = f"Conexão encerrada com {client_socket.sharer_username}.\n"
                            output_text.update()
                            break
                except KeyboardInterrupt:
                    client_socket.close()
            
            threading.Thread(target=receive_data, daemon=True).start()
        page.update()
    
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)