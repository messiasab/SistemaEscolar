import flet as ft
from model.colecao import RegistrosM

class RegistroTelefonicoView():
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.registros_db = RegistrosM()

        # Recupera o ID do aluno da sessão
        self.aluno_id = self.page.session.get("aluno_id")
        if not self.aluno_id:
            self.page.snack_bar = ft.SnackBar(ft.Text("Nenhum aluno selecionado."), bgcolor=ft.colors.RED)
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Controles da interface
        self.tipo_dropdown = ft.Dropdown(
            label="Tipo",
            options=[
                ft.dropdown.Option("Busca Ativa"),
                ft.dropdown.Option("Acidentes"),
                ft.dropdown.Option("Saúde"),
                ft.dropdown.Option("Indisciplina"),
                ft.dropdown.Option("Outros"),
            ],
        )
        self.nome_responsavel = ft.TextField(label="Nome do Responsável")
        self.data_input = ft.TextField(label="Data", hint_text="DD/MM/AAAA")
        self.acao_realizada = ft.TextField(label="Ação Realizada", multiline=True)
        self.observacao = ft.TextField(label="Observação", multiline=True)

        # Variável para armazenar o ID do registro sendo editado
        self.editando_id = None

        # Referência para o botão "Cancelar Edição"
        self.cancelar_edicao_button = ft.ElevatedButton(
            "Cancelar Edição",
            on_click=self.cancelar_edicao,
            visible=False,
        )

        # Lista de registros
        self.registros_list = ft.ListView(spacing=10, height=300, auto_scroll=True)

        # Carrega os registros existentes
        self.carregar_registros()

    def build(self):
        return ft.Column([
            ft.Text("Formulário de Registro Telefônico", size=24, weight=ft.FontWeight.BOLD),
            self.tipo_dropdown,
            self.nome_responsavel,
            self.data_input,
            self.acao_realizada,
            self.observacao,
            ft.Row([
                ft.ElevatedButton("Salvar Registro", on_click=self.salvar_registro),
                self.cancelar_edicao_button,  # Botão Cancelar Edição
            ]),
            ft.Divider(height=20, color=ft.colors.GREY_300),
            ft.Text("Registros Cadastrados", size=20, weight=ft.FontWeight.BOLD),
            self.registros_list,
        ])

    def salvar_registro(self, e):
        """
        Salva ou atualiza um registro telefônico no banco de dados.
        """
        if not self.tipo_dropdown.value or not self.nome_responsavel.value or not self.data_input.value:
            self.page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos obrigatórios."), bgcolor=ft.colors.RED)
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Monta os dados do registro
        registro_data = {
            "tipo": self.tipo_dropdown.value,
            "nome_responsavel": self.nome_responsavel.value,
            "data": self.data_input.value,
            "acao_realizada": self.acao_realizada.value,
            "observacao": self.observacao.value,
        }

        if self.editando_id:  # Se estiver editando um registro existente
            query = {"_id": self.editando_id}
            modificados = self.registros_db.atualiza(query=query, update_data=registro_data)
            if modificados > 0:
                self.page.snack_bar = ft.SnackBar(ft.Text("Registro atualizado com sucesso!"), bgcolor=ft.colors.GREEN)
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text("Erro ao atualizar o registro."), bgcolor=ft.colors.RED)
        else:  # Se estiver criando um novo registro
            resultado = self.registros_db.create_with_aluno_id(self.aluno_id, registro_data)
            if resultado:
                self.page.snack_bar = ft.SnackBar(ft.Text("Registro salvo com sucesso!"), bgcolor=ft.colors.GREEN)
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text("Erro ao salvar o registro."), bgcolor=ft.colors.RED)

        self.limpar_formulario()
        self.carregar_registros()  # Atualiza a lista de registros
        self.page.snack_bar.open = True
        self.page.update()

    def carregar_registros(self):
        """
        Carrega e exibe os registros associados ao aluno.
        """
        registros = self.registros_db.ler_por_aluno(self.aluno_id)
        self.registros_list.controls.clear()
        if registros:
            for registro in registros:
                self.registros_list.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text(f"Tipo: {registro['tipo']}", weight=ft.FontWeight.BOLD),
                                ft.Text(f"Responsável: {registro['nome_responsavel']}"),
                                ft.Text(f"Data: {registro['data']}"),
                                ft.Text(f"Ação Realizada: {registro['acao_realizada']}"),
                                ft.Text(f"Observação: {registro['observacao']}"),
                                ft.Row([
                                    ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar", on_click=lambda e, reg=registro: self.editar_registro(reg)),
                                    ft.IconButton(icon=ft.icons.DELETE, tooltip="Excluir", on_click=lambda e, reg_id=registro["_id"]: self.apagar_registro(reg_id)),
                                ], alignment=ft.MainAxisAlignment.END),
                            ], spacing=5),
                            padding=10,
                        ),
                        elevation=3,
                    )
                )
        else:
            self.registros_list.controls.append(
                ft.Text("Nenhum registro cadastrado para este aluno.", italic=True, color=ft.colors.GREY_500)
            )
        self.page.update()

    def editar_registro(self, registro):
        """
        Carrega os dados de um registro no formulário para edição.
        """
        self.tipo_dropdown.value = registro["tipo"]
        self.nome_responsavel.value = registro["nome_responsavel"]
        self.data_input.value = registro["data"]
        self.acao_realizada.value = registro["acao_realizada"]
        self.observacao.value = registro["observacao"]

        # Define o ID do registro sendo editado
        self.editando_id = registro["_id"]

        # Ativa o botão "Cancelar Edição"
        self.cancelar_edicao_button.visible = True

        self.page.update()

    def cancelar_edicao(self, e):
        """
        Cancela a edição e limpa o formulário.
        """
        self.editando_id = None
        self.limpar_formulario()

        # Desativa o botão "Cancelar Edição"
        self.cancelar_edicao_button.visible = False

        self.page.update()

    def apagar_registro(self, registro_id):
        """
        Remove um registro do banco de dados.
        """
        apagados = self.registros_db.apaga_por_aluno(self.aluno_id, {"_id": registro_id})
        if apagados > 0:
            self.page.snack_bar = ft.SnackBar(ft.Text("Registro removido com sucesso!"), bgcolor=ft.colors.GREEN)
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Erro ao remover o registro."), bgcolor=ft.colors.RED)
        self.page.snack_bar.open = True
        self.carregar_registros()
        self.page.update()

    def limpar_formulario(self):
        """
        Limpa os campos do formulário.
        """
        self.tipo_dropdown.value = None
        self.nome_responsavel.value = ""
        self.data_input.value = ""
        self.acao_realizada.value = ""
        self.observacao.value = ""
        self.page.update()