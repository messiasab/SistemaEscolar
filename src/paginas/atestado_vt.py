import flet as ft
from bson import ObjectId  # Importe ObjectId para trabalhar com IDs do MongoDB
from model.colecao import AtestadosM, AlunosM  # Importa as classes de acesso ao MongoDB

def AtestadoViewT(page):
    # Instâncias do banco de dados
    atestados_db = AtestadosM()
    alunos_db = AlunosM()

    # Variável global para armazenar o dicionário de pesquisa
    global turma_pesquisa
    turma_pesquisa = {}

    def carregar_turmas():
        """
        Carrega combinações únicas de Série, Turma e Ensino da coleção Alunos
        e preenche o Dropdown de turmas.
        """
        try:
            # Busca todos os alunos na coleção
            alunos = alunos_db.ler()

            # Cria um conjunto de combinações únicas de Série, Turma e Ensino
            combinacoes_unicas = set(
                (aluno.get("Série"), aluno.get("Turma"), aluno.get("Ensino"))
                for aluno in alunos
                if aluno.get("Série") and aluno.get("Turma") and aluno.get("Ensino")
            )

            # Cria um dicionário para pesquisa
            global turma_pesquisa
            turma_pesquisa = {
                f"{serie} - {turma} - {ensino}": {"Série": serie, "Turma": turma, "Ensino": ensino}
                for serie, turma, ensino in combinacoes_unicas
            }

            # Limpa as opções existentes e adiciona as novas combinações
            turma_dropdown.options.clear()
            turma_dropdown.options.append(ft.dropdown.Option("Todos"))  # Adiciona a opção "Todos"
            for chave in sorted(turma_pesquisa.keys()):  # Ordena alfabeticamente
                turma_dropdown.options.append(ft.dropdown.Option(chave))

            print(f"Opções de turma geradas: OK")  # Debug
            page.update()  # Atualiza a interface para refletir as mudanças
        except Exception as e:
            print(f"Erro ao carregar turmas: {e}")

    def limpar_filtros(e):
        """
        Limpa os filtros selecionados nos dropdowns e exibe todos os atestados.
        """
        turma_dropdown.value = "Todos"
        periodo_dropdown.value = "Todos"
        pesquisar_atestados(None)  # Chama a função de pesquisa sem filtros
        page.update()

    def pesquisar_atestados(e):
        """
        Pesquisa atestados com base nos filtros de turma e período.
        Se nenhum filtro for selecionado, retorna todos os atestados.
        """
        turma_selecionada = turma_dropdown.value
        periodo = periodo_dropdown.value

        # Obtém os filtros de Série, Turma e Ensino a partir do dicionário
        filtros_turma = turma_pesquisa.get(turma_selecionada, {}) if turma_selecionada != "Todos" else {}

        # Busca todos os atestados
        atestados = atestados_db.ler()
        atestados_filtrados = []

        for atestado in atestados:
            aluno = atestado.get("aluno_id")  # Obtém os dados do aluno diretamente

            # Verifica se os dados do aluno estão disponíveis
            if isinstance(aluno, dict):
                # Verifica se o atestado corresponde aos filtros ou se nenhum filtro foi selecionado
                if (
                    (not filtros_turma or (
                        aluno.get("Série") == filtros_turma.get("Série") and
                        aluno.get("Turma") == filtros_turma.get("Turma") and
                        aluno.get("Ensino") == filtros_turma.get("Ensino")
                    )) and
                    (not periodo or periodo == "Todos" or aluno.get("Período") == periodo)
                ):
                    atestados_filtrados.append({
                        "aluno": aluno.get("Nome", "Desconhecido"),
                        "serie": aluno.get("Série", "Não informada"),
                        "turma": aluno.get("Turma", "Não informada"),
                        "periodo": aluno.get("Período", "Não informado"),
                        "data": atestado.get("data", "Não informada"),
                        "motivo": atestado.get("conteudo", "Não informado"),
                        "numero_dias": atestado.get("numero_dias", "Não informado"),
                    })

        # Exibe os resultados na lista
        atestados_list.controls.clear()
        if atestados_filtrados:
            for atestado in atestados_filtrados:
                atestados_list.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text(f"Aluno: {atestado['aluno']}", weight=ft.FontWeight.BOLD),
                                ft.Text(f"Turma: {atestado['turma']}"),
                                ft.Text(f"Série: {atestado['serie']}"),
                                ft.Text(f"Período: {atestado['periodo']}"),
                                ft.Text(f"Data: {atestado['data']}"),
                                ft.Text(f"Motivo: {atestado['motivo']}"),
                                ft.Text(f"Número de dias: {atestado.get('numero_dias', 'Não informado')}"),
                            ], spacing=5),
                            padding=10,
                        ),
                        elevation=3,
                    )
                )
        else:
            atestados_list.controls.append(
                ft.Text("Nenhum atestado encontrado.", italic=True, color=ft.colors.GREY_500)
            )

        page.update()

    # Controles da interface
    turma_dropdown = ft.Dropdown(
        label="Turma",
        options=[ft.dropdown.Option("Todos")],  # Adiciona a opção "Todos" inicialmente
    )

    periodo_dropdown = ft.Dropdown(
        label="Período",
        options=[
            ft.dropdown.Option("Todos"),  # Adiciona a opção "Todos"
            ft.dropdown.Option("Manhã"),
            ft.dropdown.Option("Tarde"),
            ft.dropdown.Option("Noite"),
        ],
    )

    # Lista de atestados filtrados
    atestados_list = ft.ListView(spacing=10, height=300, auto_scroll=True)

    # Botões
    pesquisar_button = ft.ElevatedButton("Pesquisar", on_click=pesquisar_atestados)
    limpar_filtros_button = ft.ElevatedButton("Limpar Filtros", on_click=limpar_filtros)

    # Carrega as turmas ao inicializar
    carregar_turmas()

    return ft.Column([
        ft.Text("Pesquisa de Atestados", size=24, weight=ft.FontWeight.BOLD),
        turma_dropdown,
        periodo_dropdown,
        ft.Row([pesquisar_button, limpar_filtros_button], spacing=10),
        ft.Divider(height=20, color=ft.colors.GREY_300),
        ft.Text("Resultados da Pesquisa", size=20, weight=ft.FontWeight.BOLD),
        atestados_list,
    ])