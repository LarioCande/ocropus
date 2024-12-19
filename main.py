import flet as ft
from doctr.models import ocr_predictor
from doctr.io import DocumentFile

# Carga el modelo OCR preentrenado
model = ocr_predictor(pretrained=True)

def main(page: ft.Page):
    # Configuración de la página
    page.title = "OCR con Doctr y Flet"
    page.scroll = "adaptive"

    # Contenedor para mostrar el texto extraído
    extracted_text = ft.Text(value="El texto extraído aparecerá aquí.", size=16)

    # Función para procesar la imagen seleccionada
    def process_image(e: ft.FilePickerResultEvent):
        if not e.files:
            return

        # Obtiene la ruta del archivo seleccionado
        file_path = e.files[0].path

        # Cargar la imagen con Doctr
        doc = DocumentFile.from_images(file_path)
        result = model(doc)

        # Extraer texto
        text = "\n".join(
            [
                " ".join(word.value for word in line.words)
                for page in result.pages
                for block in page.blocks
                for line in block.lines
            ]
        )

        # Mostrar el texto en pantalla
        extracted_text.value = text if text else "No se detectó texto en la imagen."
        page.update()

    # FilePicker para seleccionar la imagen
    file_picker = ft.FilePicker(on_result=process_image)
    page.overlay.append(file_picker)

    # Botón para abrir el FilePicker
    upload_button = ft.ElevatedButton(
        text="Seleccionar Imagen",
        on_click=lambda _: file_picker.pick_files(allow_multiple=False),
    )

    # Añadir elementos a la página
    page.add(
        ft.Column(
            [
                ft.Text(value="OCR con Doctr y Flet", size=20, weight="bold"),
                upload_button,
                extracted_text,
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

# Ejecutar la aplicación
if __name__ == "__main__":
    ft.app(target=main)

