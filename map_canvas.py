import flet as ft
import flet.canvas as cv
import json
import os


class State:
    x: float
    y: float


state = State()


def view_map_canvas(page: ft.Page):
    page.title = "Flet Brush - Image Background"

    # Background image path (exists in templates/)
    image_path = "templates/Chunchi01.jpg"

    # Try to read image size via Pillow; fallback to a large default
    try:
        from PIL import Image

        img = Image.open(image_path)
        IMAGE_W, IMAGE_H = img.size
    except Exception:
        IMAGE_W, IMAGE_H = 2000, 2000

    scale = 1.0
    brush_width = 3

    # store lines in logical (image) coordinates: list of (x1,y1,x2,y2,width)
    logical_lines: list[tuple] = []

    def rebuild_shapes():
        # update canvas shapes (only lines) and resize image and canvas
        shapes = []
        for (x1, y1, x2, y2, w) in logical_lines:
            shapes.append(
                cv.Line(x1 * scale, y1 * scale, x2 * scale, y2 * scale, paint=ft.Paint(stroke_width=w * scale))
            )
        cp.shapes = shapes
        # resize controls
        cp.width = IMAGE_W * scale
        cp.height = IMAGE_H * scale
        bg_image.width = IMAGE_W * scale
        bg_image.height = IMAGE_H * scale
        # container that holds the stack will also reflect sizes
        outer.width = IMAGE_W * scale
        outer.height = IMAGE_H * scale
        cp.update()

    def pan_start(e: ft.DragStartEvent):
        # map screen local coords to logical coords
        state.x = e.local_x / scale
        state.y = e.local_y / scale

    def pan_update(e: ft.DragUpdateEvent):
        x2 = e.local_x / scale
        y2 = e.local_y / scale
        logical_lines.append((state.x, state.y, x2, y2, brush_width))
        state.x = x2
        state.y = y2
        rebuild_shapes()

    def clear_canvas(e):
        logical_lines.clear()
        rebuild_shapes()

    def zoom_in(e):
        nonlocal scale
        scale *= 1.25
        rebuild_shapes()

    def zoom_out(e):
        nonlocal scale
        scale /= 1.25
        rebuild_shapes()

    def set_brush(e):
        nonlocal brush_width
        brush_width = int(e.control.value)

    def on_file_picked(e: ft.FilePickerResultEvent):
        # file picker returns list of files; take first
        nonlocal IMAGE_W, IMAGE_H, image_path
        if not e.files:
            return
        p = e.files[0].path
        image_path = p
        # try to get real size
        try:
            from PIL import Image

            img = Image.open(image_path)
            IMAGE_W, IMAGE_H = img.size
        except Exception:
            IMAGE_W, IMAGE_H = 2000, 2000

        # clear previous lines when loading new image
        logical_lines.clear()
        bg_image.src = image_path
        rebuild_shapes()

    def save_drawing(e):
        # save logical_lines to drawing.json in project root
        try:
            with open("drawing.json", "w", encoding="utf-8") as f:
                json.dump(logical_lines, f)
            page.snack_bar = ft.SnackBar(ft.Text("Dibujo guardado en drawing.json"))
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error guardando: {ex}"))
            page.snack_bar.open = True
            page.update()

    def load_drawing(e):
        # load logical_lines from drawing.json if exists
        if not os.path.exists("drawing.json"):
            page.snack_bar = ft.SnackBar(ft.Text("No existe drawing.json"))
            page.snack_bar.open = True
            page.update()
            return
        try:
            with open("drawing.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            # validate and load
            logical_lines.clear()
            for item in data:
                if isinstance(item, list) or isinstance(item, tuple):
                    logical_lines.append(tuple(item))
            rebuild_shapes()
            page.snack_bar = ft.SnackBar(ft.Text("Dibujo cargado desde drawing.json"))
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error cargando: {ex}"))
            page.snack_bar.open = True
            page.update()

    # initial canvas (no image in canvas shapes)
    cp = cv.Canvas(
        [],
        content=ft.GestureDetector(
            on_pan_start=pan_start,
            on_pan_update=pan_update,
            drag_interval=4,
        ),
        expand=False,
        width=IMAGE_W * scale,
        height=IMAGE_H * scale,
    )

    # background image control (flet Image, not canvas Image)
    bg_image = ft.Image(src=image_path, width=IMAGE_W * scale, height=IMAGE_H * scale)

    # outer container to give the scroll area fixed size
    outer = ft.Container(width=IMAGE_W * scale, height=IMAGE_H * scale)

    # Controls
    # file picker (overlay) and controls
    fp = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(fp)

    controls = ft.Row([
        ft.ElevatedButton("Volver", on_click=lambda e: page.go("/")),
        ft.ElevatedButton("Open image", on_click=lambda e: fp.pick_files()),
        ft.ElevatedButton("Zoom +", on_click=zoom_in),
        ft.ElevatedButton("Zoom -", on_click=zoom_out),
        ft.ElevatedButton("Clear", on_click=clear_canvas),
        ft.ElevatedButton("Guardar", on_click=save_drawing),
        ft.ElevatedButton("Cargar", on_click=load_drawing),
        ft.Text("Brush:"),
        ft.Slider(min=1, max=20, value=brush_width, divisions=19, width=120, on_change=set_brush),
    ])

    # Stack image (bottom) and canvas (top)
    # Stack children are rendered on top of each other; bg_image first, canvas on top
    stack = ft.Stack([bg_image, cp])
    outer.content = stack

    # Put stack inside a ListView to enable scrolling
    sc = ft.ListView([outer], spacing=0, padding=0)

    # return as a View so it can be embedded in the app navigation
    return ft.View(
        "/map_canvas",
        [
            controls,
            sc,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )