import flet as ft
from paginas import *  # Importa todas as páginas

def main(page: ft.Page):
    # Configurações iniciais da página
    page.title = "Sistema Escolar"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Verifica se o usuário está logado
    if not page.session.get('usuario'):
        page.go("/login")  # Redireciona para a página de login

    # Configuração do AppBar
    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.HOME,
            on_click=lambda _: page.go("/home"),  # Navega para a rota "/"
        ),
        leading_width=40,
        title=ft.Text("Sistema Escolar"),
        center_title=False,
        bgcolor='#4250afff',
        actions=[
            ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED),
            ft.IconButton(ft.Icons.FILTER_3),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Aluno", on_click=lambda _: page.go("/alunos")),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(text="Documentos"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(text="Ocorrência", on_click=lambda _: page.go("/ocorenciast")),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(text="Contatos"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(text="Históricos"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(text="Importações", on_click=lambda _: page.go("/import")),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(text="Usuários", on_click=lambda _: page.go("/usuarios")),
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
        """Atualiza o conteúdo principal com base na rota."""
        if route == "/login":
            main_content.content = LoginView(page)
        elif route == "/":
            main_content.content = Casa_v(page)  # Página inicial após login
        elif route == "/sobre":
            main_content.content = Sobre_v(page)
        elif route == "/import":
            main_content.content = Importes_v(page)
        elif route == "/home":
            main_content.content = Casa_v(page)
        elif route == "/alunos":
            meualuno = AlunosView(page)
            main_content.content = meualuno.create_view()
        elif route == "/usuarios":
            main_content.content = UsuariosView(page)
        elif route == "/atestadot":
            main_content.content = AtestadoViewT(page)
        elif route == "/ocorenciast":
            main_content.content = OcorrenciasTotaisView(page)
        else:
            main_content.content = ft.Text("Página não encontrada.", size=20, color=ft.colors.RED)

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
        """Função chamada quando a rota muda."""
        print(f"Rota atual: {route.route}")  # Debugging
        update_main_content(route.route)

    # Configurar eventos de navegação
    page.on_route_change = route_change

    # Definir a rota inicial
    page.go(page.route)


# Executar o aplicativo
ft.app(target=main)