import flet as ft
from bson import ObjectId  # Importe ObjectId para trabalhar com IDs do MongoDB
from model.colecao import AtestadosM, AlunosM  # Importa as classes de acesso ao MongoDB

def AtestadoViewT(page):
    # Instâncias do banco de dados
    atestados_db = AtestadosM()
    alunos_db = AlunosM()
    def carregar_turmas():
        """
        Carrega as turmas únicas da coleção Alunos e preenche o Dropdown de turmas.
        """
        try:
            # Busca todas as turmas na coleção Alunos
            alunos = alunos_db.ler()
            turmas = set(aluno.get("Turma") for aluno in alunos if aluno.get("Turma"))  # Remove duplicatas
            print(f"Essas são as turmas obtidas: {turmas}")
            # Limpa as opções existentes e adiciona as novas turmas
            turma_dropdown.options.clear()
            for turma in sorted(turmas):  # Ordena as turmas alfabeticamente
                turma_dropdown.options.append(ft.dropdown.Option(turma))

            page.update()  # Atualiza a interface para refletir as mudanças
        except Exception as e:
            print(f"Erro ao carregar turmas: {e}")

    # Controles da interface
    turma_dropdown = ft.Dropdown(
        label="Turma",
        options=[   ],
    )

    periodo_dropdown = ft.Dropdown(
        label="Período",
        options=[
            ft.dropdown.Option("Manhã"),
            ft.dropdown.Option("Tarde"),
            ft.dropdown.Option("Noite"),
        ],
    )

    # Lista de atestados filtrados
    atestados_list = ft.ListView(spacing=10, height=300, auto_scroll=True)

    def obter_dados_aluno(aluno_id):
        """
        Busca os dados do aluno (nome, turma e período) no banco de dados.
        Retorna um dicionário com os dados ou valores padrão se o aluno não for encontrado.
        """
        try:
            # Converte o ID para ObjectId e busca o aluno
            aluno = alunos_db.ler(query={"_id": ObjectId(aluno_id)})
            if aluno:
                aluno = aluno[0]  # Pega o primeiro resultado
                print(f"o aluno relacionado ao atestado é: {aluno}")
                return aluno
        except Exception as e:
            print(f"Erro ao buscar aluno com ID {aluno_id}: {e}")

        # Retorna valores padrão se o aluno não for encontrado
        return {
            "nome": "Desconhecido",
            "turma": "Não informada",
            "periodo": "Não informado",
        }

    def pesquisar_atestados(e):
        """
        Pesquisa atestados com base nos filtros de turma e período.
        Se nenhum filtro for selecionado, retorna todos os atestados.
        """
        turma = turma_dropdown.value
        periodo = periodo_dropdown.value

        # Busca todos os atestados
        atestados = atestados_db.ler()
        atestados_filtrados = []

        for atestado in atestados:
            aluno_id = atestado.get("aluno_id")  # Obtém o ID do aluno associado ao atestado
            if aluno_id:
                aluno = obter_dados_aluno(aluno_id)

                # Verifica se o atestado corresponde aos filtros ou se nenhum filtro foi selecionado
                if (not turma or aluno["turma"] == turma) and (not periodo or aluno["periodo"] == periodo):
                    atestados_filtrados.append({
                        "aluno": aluno["Nome"],
                        "turma": aluno["Turma"],
                        "periodo": aluno.get("Periodo","Não informada"),
                        "data": atestado.get("data", "Não informada"),
                        "motivo": atestado.get("motivo", "Não informado"),
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
                                ft.Text(f"Período: {atestado['periodo']}"),
                                ft.Text(f"Data: {atestado['data']}"),
                                ft.Text(f"Motivo: {atestado['motivo']}"),
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

    # Botão "Pesquisar"
    pesquisar_button = ft.ElevatedButton("Pesquisar", on_click=pesquisar_atestados)
    carregar_turmas()
    return ft.Column([
        ft.Text("Pesquisa de Atestados", size=24, weight=ft.FontWeight.BOLD),
        turma_dropdown,
        periodo_dropdown,
        pesquisar_button,
        ft.Divider(height=20, color=ft.colors.GREY_300),
        ft.Text("Resultados da Pesquisa", size=20, weight=ft.FontWeight.BOLD),
        atestados_list,
    ])