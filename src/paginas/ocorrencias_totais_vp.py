import flet as ft
from bson import ObjectId  # Importe ObjectId para trabalhar com IDs do MongoDB
from model import OcorrenciasM, AlunosM  # Importa as classes de acesso ao MongoDB
import math  # Para verificar valores NaN

def OcorrenciasTotaisView(page):
    # Instâncias do banco de dados
    ocorrencias_db = OcorrenciasM()
    alunos_db = AlunosM()

    # Controles da interface
    turma_dropdown = ft.Dropdown(
        label="Turma",
        options=[],  # Inicialmente vazio, será preenchido dinamicamente
    )

    periodo_dropdown = ft.Dropdown(
        label="Período",
        options=[
            ft.dropdown.Option("Manhã"),
            ft.dropdown.Option("Tarde"),
            ft.dropdown.Option("Noite"),
        ],
    )

    # Lista de ocorrências filtradas
    ocorrencias_list = ft.ListView(spacing=10, height=300, auto_scroll=True)

    def carregar_turmas():
        """
        Carrega as turmas únicas da coleção Alunos e preenche o Dropdown de turmas.
        """
        try:
            # Busca todos os alunos na coleção Alunos
            alunos = alunos_db.ler()
            print(f"Documentos encontrados na coleção Alunos: {alunos}")  # Log de debugging

            # Extrai as turmas (remove duplicatas e filtra valores inválidos)
            turmas = set()
            for aluno in alunos:
                turma = aluno.get("Turma")
                if turma and not (isinstance(turma, float) and math.isnan(turma)):  # Ignora valores NaN
                    turmas.add(turma)

            print(f"Turmas extraídas: {turmas}")  # Log de debugging

            # Limpa as opções existentes e adiciona as novas turmas
            turma_dropdown.options.clear()
            if turmas:
                for turma in sorted(turmas):  # Ordena as turmas alfabeticamente
                    turma_dropdown.options.append(ft.dropdown.Option(turma))
            else:
                # Adiciona uma opção padrão se nenhuma turma for encontrada
                turma_dropdown.options.append(ft.dropdown.Option("Nenhuma turma disponível"))

            page.update()  # Atualiza a interface para refletir as mudanças
        except Exception as e:
            print(f"Erro ao carregar turmas: {e}")

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
                turma = aluno.get("Turma", "Não informada")
                periodo = aluno.get("Periodo", "Não informado")

                # Trata valores NaN
                if isinstance(turma, float) and math.isnan(turma):
                    turma = "Não informada"
                if isinstance(periodo, float) and math.isnan(periodo):
                    periodo = "Não informado"

                return {
                    "nome": aluno.get("Nome", "Desconhecido"),
                    "turma": turma,
                    "periodo": periodo,
                }
        except Exception as e:
            print(f"Erro ao buscar aluno com ID {aluno_id}: {e}")

        # Retorna valores padrão se o aluno não for encontrado
        return {
            "nome": "Desconhecido",
            "turma": "Não informada",
            "periodo": "Não informado",
        }

    def pesquisar_ocorrencias(e):
        """
        Pesquisa ocorrências com base nos filtros de turma e período.
        Se nenhum filtro for selecionado, retorna todas as ocorrências.
        """
        turma = turma_dropdown.value
        periodo = periodo_dropdown.value

        # Busca todas as ocorrências
        ocorrencias = ocorrencias_db.ler()
        ocorrencias_filtradas = []

        for ocorrencia in ocorrencias:
            aluno_id = ocorrencia.get("aluno_id")  # Obtém o ID do aluno associado à ocorrência
            if aluno_id:
                aluno = obter_dados_aluno(aluno_id)

                # Verifica se a ocorrência corresponde aos filtros ou se nenhum filtro foi selecionado
                if (not turma or aluno["turma"] == turma) and (not periodo or aluno["periodo"] == periodo):
                    ocorrencias_filtradas.append({
                        "aluno": aluno["nome"],
                        "turma": aluno["turma"],
                        "periodo": aluno["periodo"],
                        "data": ocorrencia.get("data", "Não informada"),
                        "relatorio": ocorrencia.get("relatorio", "Não informado"),
                        "estrategia": ocorrencia.get("estrategia", "Não informado"),
                        "encaminhamento": ocorrencia.get("encaminhamento", "Não informado"),
                    })

        # Exibe os resultados na lista
        ocorrencias_list.controls.clear()
        if ocorrencias_filtradas:
            for ocorrencia in ocorrencias_filtradas:
                ocorrencias_list.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text(f"Aluno: {ocorrencia['aluno']}", weight=ft.FontWeight.BOLD),
                                ft.Text(f"Turma: {ocorrencia['turma']}"),
                                ft.Text(f"Período: {ocorrencia['periodo']}"),
                                ft.Text(f"Data: {ocorrencia['data']}"),
                                ft.Text(f"Relatório: {ocorrencia['relatorio']}"),
                                ft.Text(f"Estratégia Pedagógica: {ocorrencia['estrategia']}"),
                                ft.Text(f"Encaminhamentos: {ocorrencia['encaminhamento']}"),
                            ], spacing=5),
                            padding=10,
                        ),
                        elevation=3,
                    )
                )
        else:
            ocorrencias_list.controls.append(
                ft.Text("Nenhuma ocorrência encontrada.", italic=True, color=ft.colors.GREY_500)
            )

        page.update()

    # Botão "Pesquisar"
    pesquisar_button = ft.ElevatedButton("Pesquisar", on_click=pesquisar_ocorrencias)

    # Carrega as turmas ao iniciar a tela
    carregar_turmas()

    return ft.Column([
        ft.Text("Pesquisa de Ocorrências Totais", size=24, weight=ft.FontWeight.BOLD),
        turma_dropdown,
        periodo_dropdown,
        pesquisar_button,
        ft.Divider(height=20, color=ft.colors.GREY_300),
        ft.Text("Resultados da Pesquisa", size=20, weight=ft.FontWeight.BOLD),
        ocorrencias_list,
    ])