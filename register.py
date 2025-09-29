import flet as ft

def view_register(page):
    return ft.View(
        "/register",
        [
            ft.Text("Registrar Usuario", style="headlineMedium"),
            ft.ElevatedButton("Volver", on_click=lambda _: page.go("/")),

            login_form := ft.Column([
                ft.Text("Registrate", style="headlineSmall"),
                ft.TextField(label="Usuario", width=300),
                ft.textField(label="Correo Electrónico", width=300),
                ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300),
                ft.TextField(label="Comprobar Contraseña", password=True, can_reveal_password=True, width=300),
                ft.ElevatedButton("Ingresar", bgcolor="#1976d2", color="white", width=200),
            ]),
            
        ]
    )