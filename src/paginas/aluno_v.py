import flet as ft
from datetime import datetime
import math
from model.colecao import AlunosM

class AlunosView:
    def __init__(self, page):
        self.page = page
        self.alunos_db = AlunosM()
        self.form_fields = {}
        self.suggestions_column = ft.Column(controls=[], spacing=2)
        self.suggestions_column_eol = ft.Column(controls=[], spacing=2)
        self.form_scroll_view = ft.ListView(
            controls=[], spacing=10, height=400, auto_scroll=True
        )
        self.form_container = ft.Container(
            content=self.form_scroll_view,
            padding=20,
            border=ft.border.all(1, ft.colors.BLUE),
            border_radius=10,
            visible=False,
        )
        self.bnome = ft.TextField(
            hint_text="Pesquise por nome...",
            on_change=self.handle_name_change,
            expand=True,
        )
        self.beol = ft.TextField(
            hint_text="Pesquise por EOL...",
            on_submit=self.handle_eol_submit,
            expand=True,
        )

    def handle_name_change(self, e):
        """Manipula a busca por nome."""
        valor = e.control.value
        if len(valor) > 3:
            query = {'Nome': {"$regex": valor, "$options": "i"}}
            sugestoes = self.alunos_db.ler(query)
            nomes = [sugestao['Nome'] for sugestao in sugestoes]
            self.suggestions_column.controls.clear()
            for nome in nomes:
                self.suggestions_column.controls.append(
                    ft.ListTile(
                        title=ft.Text(nome),
                        on_click=lambda e, nome=nome: self.select_suggestion(nome),
                    )
                )
            self.page.update()

    def handle_eol_submit(self, e):
        """Manipula a busca por EOL."""
        valor = e.control.value
        if len(valor) > 6:
            query = {"EOL": int(valor)}
            resultados = self.alunos_db.ler(query)
            if resultados:
                aluno = resultados[0]
                self.bnome.value = aluno['Nome']
                self.page.session.set("aluno_selecionado", aluno)
                self.display_aluno_form(aluno)
                self.page.update()

    def select_suggestion(self, nome):
        """Seleciona um aluno da lista de sugestões."""
        self.bnome.value = nome
        aluno_selecionado = self.alunos_db.ler(query={"Nome": nome})
        if aluno_selecionado:
            aluno_selecionado = aluno_selecionado[0]
            self.page.session.set("aluno_selecionado", aluno_selecionado)
            self.display_aluno_form(aluno_selecionado)
        self.suggestions_column.controls.clear()
        self.page.update()

    def display_aluno_form(self, aluno):
        """Exibe o formulário com os dados do aluno selecionado."""
        self.page.session.set("aluno_id", aluno['_id'])
        self.form_scroll_view.controls.clear()
        self.beol.visible = False
        for key, value in aluno.items():
            formatted_value = self.format_value(value)
            self.form_fields[key] = ft.TextField(
                label=key,
                value=formatted_value,
                multiline=(key == "Endereço" or key == "Observações"),
            )
            self.form_scroll_view.controls.append(self.form_fields[key])
        self.form_scroll_view.controls.append(
            ft.ElevatedButton("Salvar Alterações", on_click=lambda e: self.save_changes(aluno))
        )
        self.form_container.visible = True
        self.page.update()

    def save_changes(self, aluno):
        """Salva as alterações feitas no formulário."""
        updated_data = {key: field.value for key, field in self.form_fields.items()}
        updated_data.pop("_id", None)
        query = {"_id": aluno["_id"]}
        modificados = self.alunos_db.atualiza(query=query, update_data=updated_data)
        if modificados > 0:
            self.page.snack_bar = ft.SnackBar(ft.Text("Alterações salvas com sucesso!"))
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Erro ao salvar alterações."))
        self.page.snack_bar.open = True
        self.page.update()

    def format_value(self, value):
        """Formata valores para exibição no formulário."""
        if isinstance(value, float) and math.isnan(value):
            return ""
        elif isinstance(value, datetime):
            return value.strftime("%d/%m/%Y")
        else:
            return str(value)

    def build(self):
        """Constrói a interface da página."""
        box_nome = ft.Column(
            expand=True,
            controls=[
                self.bnome,
                self.suggestions_column,
            ],
        )
        box_eol = ft.Column(
            expand=True,
            controls=[
                self.beol,
                self.suggestions_column_eol,
            ],
        )
        return ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    expand=True,
                    controls=[
                        ft.Container(expand=5, content=box_nome),
                        ft.Container(expand=3, content=box_eol),
                    ],
                ),
                ft.Row(
                    expand=True,
                    controls=[
                        ft.Container(expand=5, content=self.form_container),
                    ],
                ),
            ],
        )

    def build_new_aluno_form(self):
        """Constrói e retorna o formulário para inserção de um novo aluno."""
        # Limpa os controles existentes no formulário
        self.form_scroll_view.controls.clear()
        self.form_fields = {}

        # Obtém as chaves do modelo AlunosM
        aluno_campos = self.alunos_db.get_campos()  # Certifique-se de que o método get_campos() retorna as chaves do modelo
        print(f"Campos do aluno: {aluno_campos}")  # Debugging
        # Adiciona os campos ao formulário
        for campo in aluno_campos:
            self.form_fields[campo] = ft.TextField(label=campo)
            self.form_scroll_view.controls.append(self.form_fields[campo])

        # Adiciona o botão de salvar ao formulário
        self.form_scroll_view.controls.append(
            ft.ElevatedButton("Salvar Novo Aluno", on_click=self.save_new_aluno)
        )

        # Torna o container visível
        self.form_container.visible = True

        # Retorna o layout do formulário
        return ft.Column(
            [
                ft.Text("Novo Aluno", size=24, weight=ft.FontWeight.BOLD),
                self.form_container,  # Inclui o container com o formulário
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

    def save_new_aluno(self, e):
        """Salva um novo aluno no banco de dados."""
        new_aluno = {key: field.value for key, field in self.form_fields.items()}
        self.alunos_db.cria(new_aluno)
        self.page.snack_bar = ft.SnackBar(ft.Text("Novo aluno salvo com sucesso!"))
        self.page.snack_bar.open = True
        self.page.update()
    def mostra(self):    
        print