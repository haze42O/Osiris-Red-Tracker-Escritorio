import flet as ft
import sys
import os
import subprocess
import shutil

def quit_app(e):
    # keep for compatibility if some code calls with event
    try:
        p = e.page
        try:
            p.window_destroy()
        except Exception:
            pass
    except Exception:
        pass
    # force-exit as fallback
    try:
        os._exit(0)
    except Exception:
        try:
            sys.exit(0)
        except Exception:
            pass

def quit_app_page(page: ft.Page):
    try:
        page.window_destroy()
    except Exception:
        pass
    # Try to kill any flet-desktop / flet helper processes (Linux)
    try:
        if shutil.which("pkill"):
            # best-effort: kill processes that include 'flet' or 'flet-desktop'
            for pattern in ("flet-desktop", "flet", "\.flet"):
                try:
                    subprocess.Popen(["pkill", "-f", pattern], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except Exception:
                    pass
    except Exception:
        pass

    # force-exit as fallback
    try:
        os._exit(0)
    except Exception:
        try:
            sys.exit(0)
        except Exception:
            pass
from map_base import view_mapa
from mapv2 import view_map2
from map_canvas import view_map_canvas
from login import view_login
from register import view_register

def main(page: ft.Page):
    def route_change(e):
        print('route_change called, page.route=', page.route)
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
                        on_click=lambda _: page.go("/mapa2")
                    ),
                    ft.ElevatedButton(
                        "Canvas",
                        bgcolor="#1976d2",
                        color="white",
                        width=200,
                        on_click=lambda _: page.go("/map_canvas")
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
                        on_click=lambda e: quit_app_page(page)
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

        elif page.route == "/map_canvas":
            page.views.append(view_map_canvas(page))

        elif page.route == "/login":
            page.views.append(view_login(page))

        elif page.route == "/register":
            page.views.append(view_register(page))

        # ensure the current view is shown
        if page.views:
            print('page.views appended, updating page')
            page.update()

    page.on_route_change = route_change
    # start at current route (this will call route_change)
    page.go(page.route or "/")

ft.app(target=main)