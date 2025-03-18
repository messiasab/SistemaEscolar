import flet as ft

from paginas.sobre import Sobre
from paginas.casa import Casa
from paginas.importes import Importes


def main(page: ft.Page):
    # Configurações iniciais da página
    page.title = "Sistema Escolar"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Configuração do AppBar
    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.icons.HOME,
            on_click=lambda _: page.go("/home"),  # Navega para a rota "/"
        ),
        leading_width=40,
        title=ft.Text("Sistema Escolar"),
        center_title=False,
        bgcolor=ft.colors.INDIGO_500,
        actions=[
            ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED),
            ft.IconButton(ft.Icons.FILTER_3),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Aluno", on_click=lambda _: page.go("/home")),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(text="Documentos"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(text="Ocorrência"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(text="Contatos"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(text="Históricos"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(text="Importações" ,on_click=lambda _: page.go("/import")),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Sobre",
                        on_click=lambda _: page.go("/sobre"),
                    ),
                ]
            ),
        ],
    )

    # Variável para armazenar o conteúdo principal
    main_content = ft.Container(expand=True)

    # Função para atualizar o conteúdo principal
    def update_main_content(route):
        if route == "/":
            main_content.content = Casa(page)
        elif route == "/sobre":
            main_content.content = Sobre(page)
        elif route == "/import":
            main_content.content = Importes(page)  
        elif route == "/home":
            main_content.content = Casa(page)       

        page.update()

    # Rodapé fixo
    footer = ft.Container(
        content=ft.Text("Todos os direitos reservados.", size=16),
        padding=10,
    )

    # Layout principal com cabeçalho, conteúdo e rodapé
    layout = ft.Column(
        [
            ft.Container(
                content=ft.Column([main_content], scroll=ft.ScrollMode.AUTO),
                expand=True,
            ),
            footer,
        ],
        expand=True,
    )

    # Definir o layout na página
    page.add(layout)

    # Função para lidar com mudanças de rota
    def route_change(route):
        update_main_content(route.route)

    # Configurar eventos de navegação
    page.on_route_change = route_change

    # Definir a rota inicial
    page.go(page.route)


# Executar o aplicativo
ft.app(target=main)