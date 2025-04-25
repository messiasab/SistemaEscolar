import flet as ft
from bson import ObjectId
from model import OcorrenciasM, AlunosM

def OcorrenciasTotaisView(page):
    # Instâncias do banco de dados
    ocorrencias_db = OcorrenciasM()
    alunos_db = AlunosM()

    # Variável global para armazenar o dicionário de pesquisa
    turma_pesquisa = {}

    # Declaração dos controles da interface ANTES das funções
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

    # Lista de ocorrências filtradas
    ocorrencias_list = ft.ListView(spacing=10, height=300, auto_scroll=True)

    # Funções que utilizam os controles

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
            nonlocal turma_pesquisa
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
        Limpa os filtros selecionados nos dropdowns e exibe todas as ocorrências.
        """
        turma_dropdown.value = "Todos"
        periodo_dropdown.value = "Todos"
        pesquisar_ocorrencias()  # Chama a função de pesquisa sem filtros
        page.update()

    
    def pesquisar_ocorrencias(e):
        """
        Pesquisa ocorrências com base nos filtros de turma e período.
        Se nenhum filtro for selecionado, retorna todas as ocorrências.
        """
        turma_selecionada = turma_dropdown.value
        periodo = periodo_dropdown.value

        # Obtém os filtros de Série, Turma e Ensino a partir do dicionário
        filtros_turma = turma_pesquisa.get(turma_selecionada, {}) if turma_selecionada != "Todos" else {}

        # Busca todas as ocorrências
        ocorrencias = ocorrencias_db.ler()
        ocorrencias_filtradas = []

        print(f"Ocorrências encontradas no banco: {len(ocorrencias)}")  # Debug

        for ocorrencia in ocorrencias:
            aluno_id = ocorrencia.get("aluno_id")  # Obtém o ID ou os dados do aluno associado à ocorrência
            aluno = None

            # Verifica se aluno_id é um ObjectId ou um dicionário
            if isinstance(aluno_id, ObjectId):
                # Busca os dados do aluno no banco de dados
                aluno_result = alunos_db.ler({"_id": aluno_id})
                if aluno_result:
                    aluno = aluno_result[0]  # Assume que a busca retorna uma lista com um único aluno
            elif isinstance(aluno_id, dict):
                # Usa os dados do aluno diretamente
                aluno = aluno_id

            # Verifica se os dados do aluno estão disponíveis
            if aluno is None:
                print(f"Erro: Aluno não encontrado para a ocorrência {ocorrencia.get('data', 'desconhecida')}")  # Debug
                continue  # Pula para a próxima ocorrência

            print(f"Processando ocorrência para aluno: {aluno.get('Nome', 'Desconhecido')}")  # Debug

            # Normaliza os valores para comparação
            serie = aluno.get("Série", "Não informado").strip().lower()
            turma = aluno.get("Turma", "Não informado").strip().lower()
            ensino = aluno.get("Ensino", "Não informado").strip().lower()
            periodo_aluno = aluno.get("Período", "Não informado").strip().lower()

            filtro_serie = filtros_turma.get("Série", "Não informado").strip().lower()
            filtro_turma = filtros_turma.get("Turma", "Não informado").strip().lower()
            filtro_ensino = filtros_turma.get("Ensino", "Não informado").strip().lower()

            # Verifica se a ocorrência corresponde aos filtros ou se nenhum filtro foi selecionado
            if (
                (not filtros_turma or (
                    serie == filtro_serie and
                    turma == filtro_turma and
                    ensino == filtro_ensino
                )) and
                (not periodo or periodo == "Todos" or periodo_aluno == periodo.strip().lower())
            ):
                ocorrencias_filtradas.append({
                    "aluno": aluno.get("Nome", "Desconhecido"),
                    "turma": aluno.get("Turma", "Não informada"),
                    "periodo": aluno.get("Período", "Não informado"),
                    "data": ocorrencia.get("data", "Não informada"),
                    "relatorio": ocorrencia.get("relatorio", "Não informado"),
                    "estrategia": ocorrencia.get("estrategia", "Não informado"),
                    "encaminhamento": ocorrencia.get("encaminhamento", "Não informado"),
                })

        print(f"Ocorrências filtradas: {len(ocorrencias_filtradas)}")  # Debug

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

    # Botões
    pesquisar_button = ft.ElevatedButton("Pesquisar", on_click=pesquisar_ocorrencias)
    limpar_filtros_button = ft.ElevatedButton("Limpar Filtros", on_click=limpar_filtros)

    # Carrega as turmas ao inicializar
    carregar_turmas()

    return ft.Column([
        ft.Text("Pesquisa de Ocorrências Totais", size=24, weight=ft.FontWeight.BOLD),
        turma_dropdown,
        periodo_dropdown,
        ft.Row([pesquisar_button, limpar_filtros_button], spacing=10),
        ft.Divider(height=20, color=ft.colors.GREY_300),
        ft.Text("Resultados da Pesquisa", size=20, weight=ft.FontWeight.BOLD),
        ocorrencias_list,
    ])