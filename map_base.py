import flet as ft

def view_mapa(page):
    # Barra lateral
    sidebar = ft.Container(
        width=320,
        bgcolor="#e3e7ea",
        border_radius=ft.border_radius.only(top_left=20, bottom_left=20),
        padding=20,
        content=ft.Column([
            # Botón para regresar a la página principal
            ft.ElevatedButton(
                "Regresar",
                icon="arrow_back",
                on_click=lambda _: page.go("/"),
                style=ft.ButtonStyle(bgcolor="#f5f7fa", color="#2d3a4a")
            ),
            # Barra superior con botón cerrar
            ft.Row([
                ft.Text("", expand=True),
                ft.IconButton("close", icon_color="#b0b8be", tooltip="Cerrar")
            ]),
            ft.TextField(
                hint_text="Search for places",
                prefix_icon="search",
                filled=True,
                bgcolor="#f5f7fa",
                border_radius=10,
                height=40,
                content_padding=ft.padding.only(left=10)
            ),
            ft.Divider(height=20, color="transparent"),
            ft.ElevatedButton("Home", icon="explore", style=ft.ButtonStyle(bgcolor="#f5f7fa", color="#2d3a4a")),
            ft.ElevatedButton("Directions", icon="directions", style=ft.ButtonStyle(bgcolor="#f5f7fa", color="#2d3a4a")),
            ft.Text("Saved", weight="bold", size=14, color="#7a8a99"),
            # Usuarios guardados (simulados)
            ft.ListTile(
                leading=ft.CircleAvatar(bgcolor="#b0b8be", content=ft.Text("A")),
                title=ft.Text("Usuario 1", size=12)
            ),
            ft.ListTile(
                leading=ft.CircleAvatar(bgcolor="#b0b8be", content=ft.Text("B")),
                title=ft.Text("Usuario 2", size=12)
            ),
            ft.Text("Nearby", weight="bold", size=14, color="#7a8a99"),
            ft.ListTile(
                leading=ft.CircleAvatar(bgcolor="#b0b8be", content=ft.Text("C")),
                title=ft.Text("Usuario 3", size=12)
            ),
            ft.Divider(height=20, color="transparent"),
            ft.Row([
                ft.Text("Layers", expand=True, color="#7a8a99"),
                ft.Text("Satellite", color="#7a8a99")
            ])
        ],
        scroll="auto",
        expand=True,
        spacing=10
        )
    )

    # Panel principal con imagen de fondo (puedes usar un Canvas para hacerlo interactivo)
    mapa_container = ft.Container(
        expand=True,
        bgcolor="#6587a5",
        border_radius=20,
        alignment=ft.alignment.center,
        content=ft.Image(
            src="templates/Chunchi01.jpg",  # Usa aquí tu imagen del grid si la tienes
            fit=ft.ImageFit.CONTAIN,
        ),
        padding=20
    )

    return ft.View(
        "/mapa",
        [
            ft.Row([
                sidebar,
                mapa_container
            ], expand=True)
        ]
    )