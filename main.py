import flet as ft
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

def main(page: ft.Page):
    page.title = "OCR con Doctr y Flet"
    page.scroll = "adaptive"

    result_text = ft.Text("El texto extraído aparecerá aquí.", size=16)

    def process_image(e: ft.FilePickerResultEvent):
        if not e.files:
            return

        doc = DocumentFile.from_images(e.files[0].path)
        result = ocr_predictor(pretrained=True)(doc)

        extracted_text = "\n".join(
            " ".join(word.value for word in line.words)
            for page in result.pages
            for block in page.blocks
            for line in block.lines
        )
        result_text.value = extracted_text or "No se detectó texto."
        page.update()

    file_picker = ft.FilePicker(on_result=process_image)
    page.overlay.append(file_picker)

    page.add(
        ft.Column(
            [
                ft.Text("OCR con Doctr y Flet", size=20, weight="bold"),
                ft.ElevatedButton(
                    "Seleccionar Imagen",
                    on_click=lambda _: file_picker.pick_files(allow_multiple=False),
                ),
                result_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(target=main)


