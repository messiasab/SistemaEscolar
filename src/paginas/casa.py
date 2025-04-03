import flet as ft



def Casa_v(page):
     # Função para criar os itens do Row
    def items():
        items_list = [ft.Card(
                            content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.ListTile(
                                        leading=ft.Icon(ft.Icons.ALBUM),
                                        title=ft.Text("Alunos"),
                                        subtitle=ft.Text(
                                            "Nesta pagina contem a relação de alunos da escola."
                                        ),
                                    ),
                                    ft.Row(
                                        [  ft.ElevatedButton("Entrar", on_click=lambda _: page.go("/alunos")),],
                                        alignment=ft.MainAxisAlignment.END,
                                    ),
                                ]
                            ),
                            width=400,
                            padding=10,
                        )

                    ),
                    ft.Card(
                            content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.ListTile(
                                        leading=ft.Icon(ft.Icons.ALBUM),
                                        title=ft.Text("Contatos"),
                                        subtitle=ft.Text(
                                            "Nesta pagina pode ser registrado os contatos realizados com os responsavei."
                                        ),
                                    ),
                                    ft.Row(
                                        [  ft.ElevatedButton("Entrar", on_click=lambda _: page.go("/contatos")),],
                                        alignment=ft.MainAxisAlignment.END,
                                    ),
                                ]
                            ),
                            width=400,
                            padding=10,
                        )

                    ),
                    ft.Card(
                            content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.ListTile(
                                        leading=ft.Icon(ft.Icons.ALBUM),
                                        title=ft.Text("Atestados"),
                                        subtitle=ft.Text(
                                            "Nesta pagina podem ser emitidos os documentos escolares."
                                        ),
                                    ),
                                    ft.Row(
                                        [  ft.ElevatedButton("Entrar", on_click=lambda _: page.go("/atestadot")),],
                                        alignment=ft.MainAxisAlignment.END,
                                    ),
                                ]
                            ),
                            width=400,
                            padding=10,
                        )

                    ),
                    ft.Card(
                            content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.ListTile(
                                        leading=ft.Icon(ft.Icons.ALBUM),
                                        title=ft.Text("Ocorrência"),
                                        subtitle=ft.Text(
                                            "Nesta pagina são registradas as ocorrência."
                                        ),
                                    ),
                                    ft.Row(
                                        [  ft.ElevatedButton("Entrar", on_click=lambda _: page.go("/ocorenciast")),],
                                        alignment=ft.MainAxisAlignment.END,
                                    ),
                                ]
                            ),
                            width=400,
                            padding=10,
                        )

                    ),
                    ft.Card(
                            content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.ListTile(
                                        leading=ft.Icon(ft.Icons.ALBUM),
                                        title=ft.Text("Importações"),
                                        subtitle=ft.Text(
                                            "Nesta pagina pode ser feita importação de banco de dados da escola."
                                        ),
                                    ),
                                    ft.Row(
                                        [  ft.ElevatedButton("Entrar", on_click=lambda _: page.go("/import")),],
                                        alignment=ft.MainAxisAlignment.END,
                                    ),
                                ]
                            ),
                            width=400,
                            padding=10,
                        )

                    ),
                     ft.Card(
                            content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.ListTile(
                                        leading=ft.Icon(ft.Icons.ALBUM),
                                        title=ft.Text("histórico"),
                                        subtitle=ft.Text(
                                            "Nesta pagina são emitidos os hitóricos escolates."
                                        ),
                                    ),
                                    ft.Row(
                                        [  ft.ElevatedButton("Entrar", on_click=lambda _: page.go("/histo")),],
                                        alignment=ft.MainAxisAlignment.END,
                                    ),
                                ]
                            ),
                            width=400,
                            padding=10,
                        )

                    ),

                    ft.Card(
                            content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.ListTile(
                                        leading=ft.Icon(ft.Icons.ALBUM),
                                        title=ft.Text("usuarios"),
                                        subtitle=ft.Text(
                                            "Nesta pagina são emitidos os hitóricos escolates."
                                        ),
                                    ),
                                    ft.Row(
                                        [  ft.ElevatedButton("Entrar", on_click=lambda _: page.go("/usuarios")),],
                                        alignment=ft.MainAxisAlignment.END,
                                    ),
                                ]
                            ),
                            width=400,
                            padding=10,
                        )

                    ),
                    
                    
                    ]
        
        return items_list

    # Variável para armazenar o contêiner que encapsula o Row
    container = ft.Container()

    # Função para ajustar o layout com base no tamanho da tela
    def adjust_layout(e=None):
        # Calcula a largura disponível para o Row (80% da largura da tela)
        available_width = page.width * 0.8

        # Atualiza o contêiner com o novo Row ajustado
        container.content = ft.Row(
            wrap=True,  # Permite que os itens sejam distribuídos em várias linhas
            spacing=10,  # Espaçamento horizontal entre os itens
            run_spacing=10,  # Espaçamento vertical entre as linhas
            controls=items(),  # Adiciona 30 itens ao Row
            width=available_width,  # Largura do Row ajustada ao tamanho da tela
        )

        # Atualiza o contêiner apenas se ele já estiver na página
        if container.page:
            container.update()

    # Configura o evento de redimensionamento da página
    page.on_resize = adjust_layout

    # Chama a função inicialmente para configurar o layout
    adjust_layout()

    # Cria um ListView para adicionar um scroll quando o conteúdo ultrapassa a altura da página
    scrollable_content = ft.ListView(
        expand=True,  # Expande para preencher o espaço disponível
        spacing=10,  # Espaçamento entre os elementos
    )

    # Adiciona o texto explicativo e o contêiner ao ListView
    
    scrollable_content.controls.append(container)

    return scrollable_content