import flet as ft
from datetime import datetime
import math
from model.colecao import AlunosM  # Importa a classe AlunosM

def main(page: ft.Page):
    # Instância da classe AlunosM
    alunos_db = AlunosM()

    # Variáveis globais para armazenar os controles do formulário
    form_fields = {}

    def handle_change(e):
        valor = e.control.value
        if len(valor) > 3:
            # Busca sugestões no MongoDB usando o método ler com uma query de regex
            query = {"Nome": {"$regex": valor, "$options": "i"}}
            sugestoes = alunos_db.ler(query=query)
            nomes = [sugestao['Nome'] for sugestao in sugestoes]
            print(f"Sugestões retornadas: {nomes}")

            # Atualiza os controles da lista de sugestões
            suggestions_column.controls.clear()
            for nome in nomes:
                suggestions_column.controls.append(
                    ft.ListTile(
                        title=ft.Text(nome),
                        on_click=lambda e, nome=nome: select_suggestion(nome),
                    )
                )
            page.update()

    def select_suggestion(nome):
        # Preenche o campo de pesquisa com o valor selecionado
        search_field.value = nome

        # Recupera todos os dados do aluno selecionado usando o método ler
        aluno_selecionado = alunos_db.ler(query={"Nome": nome})
        if aluno_selecionado:
            aluno_selecionado = aluno_selecionado[0]  # Assume que só há um aluno com esse nome
            print(f"Dados do aluno selecionado: {aluno_selecionado}")
            
            # Exibe os dados do aluno no formulário
            display_aluno_form(aluno_selecionado)
        
        # Limpa as sugestões
        suggestions_column.controls.clear()
        page.update()

    def format_value(value):
        """
        Formata valores especiais para exibição no formulário.
        - Converte NaN para string vazia.
        - Formata datas como 'DD/MM/YYYY'.
        - Converte números para string.
        """
        if isinstance(value, float) and math.isnan(value):  # Verifica se é NaN
            return ""
        elif isinstance(value, datetime):  # Formata datas
            return value.strftime("%d/%m/%Y")
        else:
            return str(value)

    def display_aluno_form(aluno):
        # Limpa o formulário anterior, se existir
        form_scroll_view.controls.clear()

        # Cria os campos do formulário com base nos dados do aluno
        for key, value in aluno.items():
            formatted_value = format_value(value)  # Formata o valor para exibição
            form_fields[key] = ft.TextField(
                label=key,
                value=formatted_value,
                multiline=(key == "Endereço" or key == "Observações"),  # Permite múltiplas linhas para campos longos
            )
            form_scroll_view.controls.append(form_fields[key])

        # Adiciona um botão para salvar as alterações
        form_scroll_view.controls.append(
            ft.ElevatedButton("Salvar Alterações", on_click=lambda e: save_changes(aluno))
        )

        # Torna o formulário visível
        form_container.visible = True
        page.update()

    def save_changes(aluno):
        # Recupera os valores atualizados dos campos do formulário
        updated_data = {key: field.value for key, field in form_fields.items()}
        print(f"Dados atualizados: {updated_data}")

        # Atualiza os dados no MongoDB usando o método atualiza
        query = {"Nome": aluno["Nome"]}
        modificados = alunos_db.atualiza(query=query, update_data=updated_data)

        # Feedback ao usuário
        if modificados > 0:
            page.snack_bar = ft.SnackBar(ft.Text("Alterações salvas com sucesso!"))
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Erro ao salvar alterações."))
        page.snack_bar.open = True
        page.update()

    # Cria o TextField para pesquisa
    search_field = ft.TextField(
        hint_text="Pesquise por nome...",
        on_change=handle_change,
        expand=True,
    )

    # Cria a coluna para exibir as sugestões
    suggestions_column = ft.Column(
        controls=[],
        spacing=2,
    )

    # Cria o ListView para o formulário (com barra de rolagem)
    form_scroll_view = ft.ListView(
        controls=[],  # Inicialmente vazio
        spacing=10,   # Espaçamento entre os controles
        height=400,   # Altura máxima do formulário (ajustável)
        auto_scroll=True,  # Rola automaticamente ao adicionar novos controles
    )

    # Cria o container para o formulário
    form_container = ft.Container(
        content=form_scroll_view,  # O conteúdo é o ListView com barra de rolagem
        padding=20,
        border=ft.border.all(1, ft.colors.BLUE),
        border_radius=10,
        visible=False,  # Inicialmente invisível
    )

    # Adiciona os controles à página
    page.add(
        ft.Column(
            expand=True,
            controls=[
                search_field,
                suggestions_column,
                form_container,
            ],
        )
    )

# Executa o aplicativo
ft.app(target=main)