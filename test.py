import flet as ft

def main(page: ft.Page):
    page.title = "Routes Example"

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
        if page.route == "/server_ip":
            ip_input = ft.TextField(label="Server IP")
            submit_button = ft.ElevatedButton("Submit", on_click=lambda _: submit_ip(ip_input.value))
            page.views.append(
                ft.View(
                    "/server_ip",
                    [
                        ft.AppBar(title=ft.Text("Enter Server IP"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ip_input,
                        submit_button,
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        page.update()

    def submit_ip(ip):
        print(f"Server IP submitted: {ip}")
        # Add your logic to handle the submitted IP here

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)