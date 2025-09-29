import flet as ft
from register import view_register

def view_login(page):
    return ft.View(
        "/login",
        [
            ft.Text("Página de Perfil", style="headlineMedium"),
            ft.ElevatedButton("Volver", on_click=lambda _: page.go("/")),

            login_form := ft.Column([
                ft.Text("Iniciar Sesión", style="headlineSmall"),
                ft.TextField(label="Usuario", width=300),
                ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300),
                ft.ElevatedButton("Ingresar", bgcolor="#1976d2", color="white", width=200),
                ft.TextButton("¿Olvidaste tu contraseña?", on_click=lambda _: print("Recuperar contraseña")),
                ft.TextButton("¿No tienes una cuenta? Regístrate", on_click=lambda _:   page.go("/register"))
            ]),
            
        ]
    )