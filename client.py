import flet as ft
import socket
import psutil
import time
import threading

def get_system_data():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    gpu_usage = 45.5  # Simulação de uso de GPU
    disk_usage = psutil.disk_usage('/')
    total_disk = disk_usage.total / (1024 ** 3)
    used_disk = disk_usage.used / (1024 ** 3)
    percent_disk = disk_usage.percent
    
     
    return f"{cpu_usage}|{ram_usage}|{gpu_usage}|{total_disk}|{used_disk}|{percent_disk}"

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
    page.vertical_alignment = ft.VerticalAlignment.CENTER
    page.horizontal_alignment = ft.alignment.center
    page.theme_mode = ft.ThemeMode.DARK
    
    # Inicializando os componentes de texto para CPU, RAM, e GPU
    cpu_text = ft.Text("40%", font_family="Space Grotesk", weight=ft.FontWeight.BOLD, size=20)
    ram_text = ft.Text("60%", font_family="Space Grotesk", weight=ft.FontWeight.BOLD, size=20)
    gpu_text = ft.Text("60%", font_family="Space Grotesk", weight=ft.FontWeight.BOLD, size=20)
    disk_total_text = ft.Text("0", font_family="Space Grotesk")
    disk_usage_text = ft.Text("0", font_family="Space Grotesk")
    disk_percent_text = ft.Text("50", font_family="Space Grotesk", weight=ft.FontWeight.BOLD, size=20)
    
    
    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("MSI de Probe"), bgcolor=ft.colors.SURFACE_VARIANT),
                    
                    ft.Row(
                        [
                            ft.Container(
                                width=400,
                                height=400,  # Define a altura para o container
                                content=ft.Image(
                                    src="home.png",  # Nome da imagem no mesmo diretório
                                )
                            ),
                            ft.Column(
                                [
                                    ft.Column(
                                        [
                                            ft.Text("Bem-vindo ao MSI de Probe!", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE, font_family="Space Grotesk"),
                                            ft.Text("Compartilhe seus dados de sistema com outros usuários ou solicite dados de outros usuários.", size=15, color=ft.colors.WHITE, width=400, no_wrap=False, text_align=ft.TextAlign.RIGHT),
                                        ]
                                    ),                                      
                                ]
                            ),

                        ],
                        alignment=ft.MainAxisAlignment.CENTER,  # Centraliza o Row
                    ),

                    ft.ElevatedButton("Iniciar", on_click=lambda _: page.go("/server_ip")),
                ],
                
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        if page.route == "/as_sharer":
            username_input = ft.TextField(label="Username", border_color="#0c8ce9", width=500)
            output_text = ft.Text()
            
            def on_register_click(e):
                register_as_sharer(client_socket, username_input.value, output_text)
            
            register_button = ft.ElevatedButton(text="Register as Sharer", on_click=on_register_click, bgcolor="#0c8ce9")
            page.views.append(
                ft.View(
                    "/as_sharer",
                    [
                        ft.AppBar(title=ft.Text("Register as Sharer"), bgcolor=ft.colors.SURFACE_VARIANT),
                        username_input,
                        register_button,
                        output_text,
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        if page.route == "/requester":
            sharer_username_input = ft.TextField(label="Sharer Username", border_color="#0c8ce9", width=500)
            output_text = ft.Text()
            
            def on_request_click(e):
                request_sharer_data(client_socket, sharer_username_input.value, output_text)
                page.go("/show_data")
            
            request_button = ft.ElevatedButton(text="Request Sharer Data", on_click=on_request_click, bgcolor="#0c8ce9")
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
            ip_input = ft.TextField(label="Server IP", width=500, border_color="#0c8ce9")
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
                
            submit_button = ft.ElevatedButton("Submit", on_click=lambda _: submit_ip(ip_input.value), bgcolor="#0c8ce9")
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
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
            )
        if page.route == "/show_data":
            output_text = ft.Text()
            disk_progress_bar = ft.ProgressBar(border_radius=4, bar_height=8, value=0, width=410)
            page.views.append(
            ft.View(
                "/show_data",
                [
                    ft.AppBar(title=ft.Text("System Data"),
                    bgcolor=ft.colors.SURFACE_VARIANT),
                    
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                output_text,
                                disk_percent_text,
                            ],
                        ),
                        visible=False  # Define o container como invisível
                    ),
                    ft.Stack(
                        [
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text("CPU Usage", size=15),
                                        cpu_text,
                                    ],  # Adicionando os textos ao Column
                                ),
                                width=200,
                                height=100,
                                bgcolor="#293038",
                                left=0,  # Position at the start of the Stack
                                top=0,
                                border_radius=12,
                                padding=15,
                            ),  
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text("Memory Usage", size=15),
                                        ram_text,
                                    ],# Adicionando os textos ao Column
                                ),
                                width=200,
                                height=100,
                                bgcolor="#293038",
                                left=210,  # Position this container next to the first
                                top=0,
                                border_radius=12,
                                padding=15,
                            ),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text("GPU Usage", size=15),
                                        gpu_text,
                                    ],# Adicionando os textos ao Column
                                ),
                                width=410,
                                height=100,
                                bgcolor="#293038",
                                top=120,  # Position this container next to the first
                                left=0,
                                border_radius=12,
                                padding=15,
                            ),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                ft.Text("Storage", size=15),
                                                ft.Row(
                                                    controls=[
                                                        disk_usage_text,
                                                        ft.Text("/"),
                                                        disk_total_text,
                                                    ],
                                                    width=200,
                                                )
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Maximiza o espaço entre os textos
                                            width=400,
                                        ),
                                        disk_progress_bar,
                                    ],
                                ),
                                left=0,
                                top=240,
                            )
                        ],
                        width=420,  # Set width of Stack to fit both containers
                        height=320,
                    ),
                    ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
            )
            def receive_data():
                try:
                    while True:
                        data = client_socket.recv(4096).decode()
                        cpu, ram, gpu, disk_total, disk_used, disk_percent = data.split("|")
                        
                        print(f"CPU: {cpu}%\nRAM: {ram}%\nGPU: {gpu}%\n[DISCO: {disk_used}/{disk_total}/{disk_percent}%]")                        
                         
                        cpu_text.value = f"{cpu}%"
                        ram_text.value = f"{ram}%"
                        gpu_text.value = f"{gpu}%"
                        disk_usage_text.value = f"{float(disk_used):.2f} GB"
                        disk_total_text.value = f"{float(disk_total):.2f} GB"
                        disk_percent_text.value = f"{disk_percent}"

                        disk_progress_bar.value = float(disk_percent) / 100  # Converte o valor em fração
                        disk_progress_bar.update()
  
                        output_text.value = f"{data}\n"
                        output_text.update()
                        cpu_text.update()
                        ram_text.update()
                        gpu_text.update()
                        disk_usage_text.update()
                        disk_total_text.update()
                        disk_percent_text.update()

                        
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