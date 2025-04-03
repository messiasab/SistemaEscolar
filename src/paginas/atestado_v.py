import flet as ft
from model import AtestadosM

class AtestadosView():
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.atestados_db = AtestadosM()

        # Recupera o ID do aluno da sessão
        self.aluno_id = self.page.session.get("aluno_id")
        if not self.aluno_id:
            self.page.snack_bar.open = ft.SnackBar(ft.Text("Nenhum aluno selecionado."), bgcolor=ft.colors.RED)
            self.page.update()
            return

        # Controles da interface
        self.tipo_dropdown = ft.Dropdown(
            label="Tipo",
            options=[
                ft.dropdown.Option("Afastamento da Educação Física"),
                ft.dropdown.Option("Saúde"),
                ft.dropdown.Option("Restrição Alimentar"),
            ],
        )
        self.data_input = ft.TextField(label="Data", hint_text="DD/MM/AAAA")
        self.numero_dias = ft.TextField(label="Número de Dias", keyboard_type=ft.KeyboardType.NUMBER)
        self.conteudo = ft.TextField(label="Conteúdo", multiline=True)
        self.cid = ft.TextField(label="CID")
        self.observacao = ft.TextField(label="Observação", multiline=True)

        # Variável para armazenar o ID do atestado sendo editado
        self.editando_id = None

        # Referência para o botão "Cancelar Edição"
        self.cancelar_edicao_button = ft.ElevatedButton(
            "Cancelar Edição",
            on_click=self.cancelar_edicao,
            visible=False,
        )

        # Lista de atestados
        self.atestados_list = ft.ListView(spacing=10, height=300, auto_scroll=True)

        # Carrega os atestados existentes
        self.carregar_atestados()

    def build(self):
        return ft.Column([
            ft.Text("Formulário de Atestado", size=24, weight=ft.FontWeight.BOLD),
            self.tipo_dropdown,
            self.data_input,
            self.numero_dias,
            self.conteudo,
            self.cid,
            self.observacao,
            ft.Row([
                ft.ElevatedButton("Salvar Atestado", on_click=self.salvar_atestado),
                self.cancelar_edicao_button,  # Botão Cancelar Edição
            ]),
            ft.Divider(height=20, color=ft.colors.GREY_300),
            ft.Text("Atestados Cadastrados", size=20, weight=ft.FontWeight.BOLD),
            self.atestados_list,
        ])

    def salvar_atestado(self, e):
        """
        Salva ou atualiza um atestado no banco de dados.
        """
        if not self.tipo_dropdown.value or not self.data_input.value or not self.numero_dias.value:
            self.page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos obrigatórios."), bgcolor=ft.colors.RED)
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Monta os dados do atestado
        atestado_data = {
            "tipo": self.tipo_dropdown.value,
            "data": self.data_input.value,
            "numero_dias": int(self.numero_dias.value),
            "conteudo": self.conteudo.value,
            "cid": self.cid.value,
            "observacao": self.observacao.value,
        }

        if self.editando_id:  # Se estiver editando um atestado existente
            query = {"_id": self.editando_id}
            modificados = self.atestados_db.atualiza(query=query, update_data=atestado_data)
            if modificados > 0:
                self.page.snack_bar = ft.SnackBar(ft.Text("Atestado atualizado com sucesso!"), bgcolor=ft.colors.GREEN)
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text("Erro ao atualizar o atestado."), bgcolor=ft.colors.RED)
        else:  # Se estiver criando um novo atestado
            resultado = self.atestados_db.create_with_aluno_id(self.aluno_id, atestado_data)
            if resultado:
                self.page.snack_bar = ft.SnackBar(ft.Text("Atestado salvo com sucesso!"), bgcolor=ft.colors.GREEN)
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text("Erro ao salvar o atestado."), bgcolor=ft.colors.RED)

        self.limpar_formulario()
        self.carregar_atestados()  # Atualiza a lista de atestados
        self.page.snack_bar.open = True
        self.page.update()

    def carregar_atestados(self):
        """
        Carrega e exibe os atestados associados ao aluno.
        """
        atestados = self.atestados_db.ler_por_aluno(self.aluno_id)
        self.atestados_list.controls.clear()
        if atestados:
            for atestado in atestados:
                self.atestados_list.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text(f"Tipo: {atestado['tipo']}", weight=ft.FontWeight.BOLD),
                                ft.Text(f"Data: {atestado['data']}"),
                                ft.Text(f"Número de Dias: {atestado['numero_dias']}"),
                                ft.Text(f"Conteúdo: {atestado['conteudo']}"),
                                ft.Text(f"CID: {atestado['cid']}"),
                                ft.Text(f"Observação: {atestado['observacao']}"),
                                ft.Row([
                                    ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar", on_click=lambda e, at=atestado: self.editar_atestado(at)),
                                    ft.IconButton(icon=ft.icons.DELETE, tooltip="Excluir", on_click=lambda e, at=atestado: self.apagar_atestado(at["_id"])),
                                ], alignment=ft.MainAxisAlignment.END),
                            ], spacing=5),
                            padding=10,
                        ),
                        elevation=3,
                    )
                )
        else:
            self.atestados_list.controls.append(
                ft.Text("Nenhum atestado cadastrado para este aluno.", italic=True, color=ft.colors.GREY_500)
            )
        self.page.update()

    def editar_atestado(self, atestado):
        """
        Carrega os dados de um atestado no formulário para edição.
        """
        self.tipo_dropdown.value = atestado["tipo"]
        self.data_input.value = atestado["data"]
        self.numero_dias.value = str(atestado["numero_dias"])
        self.conteudo.value = atestado["conteudo"]
        self.cid.value = atestado["cid"]
        self.observacao.value = atestado["observacao"]

        # Define o ID do atestado sendo editado
        self.editando_id = atestado["_id"]

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

    def apagar_atestado(self, atestado_id):
        """
        Remove um atestado do banco de dados.
        """
        apagados = self.atestados_db.apaga_por_aluno(self.aluno_id, {"_id": atestado_id})
        if apagados > 0:
            self.page.snack_bar = ft.SnackBar(ft.Text("Atestado removido com sucesso!"), bgcolor=ft.colors.GREEN)
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Erro ao remover o atestado."), bgcolor=ft.colors.RED)
        self.page.snack_bar.open = True
        self.carregar_atestados()
        self.page.update()

    def limpar_formulario(self):
        """
        Limpa os campos do formulário.
        """
        self.tipo_dropdown.value = None
        self.data_input.value = ""
        self.numero_dias.value = ""
        self.conteudo.value = ""
        self.cid.value = ""
        self.observacao.value = ""
        self.page.update()