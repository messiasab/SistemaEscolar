import flet as ft


# Função para criar o conteúdo da página "Sobre"
def Sobre(page):
    
    return ft.Column(
        [
            ft.Text("Esta é a Página Sobre", size=24),
            ft.ElevatedButton("Voltar para Home", on_click=lambda _: page.go("/")),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
