import flet as ft
from map_base import view_mapa
from mapv2 import view_map2
from login import view_login
from register import view_register

def main(page: ft.Page):
    def route_change(e):
        page.views.clear()
        if page.route == "/":
            notas_container = ft.Container(
                content=ft.Column([
                    ft.Text("Notas de la última sesión:", style="headlineSmall"),
                    ft.Text("Aquí aparecerán las notas tomadas...", style="bodyMedium"),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
                ),
                bgcolor="#8b9597",
                border_radius=10,
                width=400,
                alignment=ft.alignment.center
            )

            menu_container = ft.Container(
                content=ft.Column([
                    ft.ElevatedButton(
                        "Abrir Mapa",
                        bgcolor="#1976d2",
                        color="white",
                        width=200,
                        on_click=lambda _: page.go("/mapa2")  # Navega a la página del mapa
                    ),
                    ft.ElevatedButton(
                        "Iniciar Sesion",
                        bgcolor="#c319d2",
                        color="white",
                        width=200,
                        on_click=lambda _: page.go("/login")
                    ),
                    ft.ElevatedButton(
                        "Salir",
                        bgcolor="#19d26c",
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=10,
                alignment=ft.alignment.center
            )

            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.Text("Bienvenido a Osiris Red Tracker", style="headlineMedium"),
                        notas_container,
                        menu_container
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30
                )
            )

        elif page.route == "/mapa2":
            page.views.append(view_map2(page))
        elif page.route == "/login":
            page.views.append(view_login(page))
        elif page.route == "/register":
            page.views.append(view_register(page))
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)