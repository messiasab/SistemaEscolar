import flet as ft
from model.colecao import OcorrenciasM, ContatosM, UsuariosM

class OcorrenciasView():
    def __init__(self, page):
        super().__init__()
        self.page = page

        # Recupera o ID do aluno da sessão
        self.aluno_id = self.page.session.get("aluno_id")
        if not self.aluno_id:
            
            self.page.open (ft.SnackBar(ft.Text("Nenhum aluno selecionado."), bgcolor=ft.colors.RED))
            self.page.update()
            return

        self.ocorrencias_db = OcorrenciasM()
        self.contatos_db = ContatosM()
        self.usuarios_db = UsuariosM()

        # Recupera os contatos do aluno
        contatos = self.contatos_db.ler_por_aluno(self.aluno_id)
        self.telefones_disponiveis = [contato["telefone"] for contato in contatos]

        # Recupera o usuário logado (simulado ou real)
        self.usuario_logado = self.page.session.get("usuario_logado")  # Supondo que o usuário foi armazenado na sessão
        if not self.usuario_logado:
            self.page.open(ft.SnackBar(ft.Text("Nenhum usuário logado."), bgcolor=ft.colors.RED))  
            
            self.page.update()
            return

        # Controles da interface
        self.nome_responsavel = ft.TextField(label="Nome do Responsável")
        self.telefone_dropdown = ft.Dropdown(
            label="Telefone",
            options=[ft.dropdown.Option(tel) for tel in self.telefones_disponiveis],
        )
        self.responsavel_registro = ft.TextField(
            label="Responsável pelo Registro",
            value=self.usuario_logado["nome"],
            read_only=True,
        )
        self.rf_registro = ft.TextField(
            label="RF",
            value=self.usuario_logado["rf"],
            read_only=True,
        )
        self.data_input = ft.TextField(label="Data", hint_text="DD/MM/AAAA")
        self.relato = ft.TextField(label="Relatório da Ocorrência", multiline=True)
        self.estrategia = ft.TextField(label="Estratégia Pedagógica Utilizada", multiline=True)
        self.encaminhamento = ft.TextField(label="Encaminhamentos Realizados", multiline=True)

        # Variável para armazenar o ID da ocorrência sendo editada
        self.editando_id = None

        # Botão "Cancelar Edição"
        self.cancelar_edicao_button = ft.ElevatedButton(
            "Cancelar Edição",
            on_click=self.cancelar_edicao,
            visible=False,
        )

        # Lista de ocorrências
        self.ocorrencias_list = ft.ListView(spacing=10, height=300, auto_scroll=True)

        # Carrega as ocorrências existentes
        self.carregar_ocorrencias()

    def build(self):
        return ft.Column([
            ft.Text("Formulário de Ocorrência", size=24, weight=ft.FontWeight.BOLD),
            self.nome_responsavel,
            self.telefone_dropdown,
            self.responsavel_registro,
            self.rf_registro,
            self.data_input,
            self.relato,
            self.estrategia,
            self.encaminhamento,
            ft.Row([
                ft.ElevatedButton("Salvar Ocorrência", on_click=self.salvar_ocorrencia),
                self.cancelar_edicao_button,  # Botão Cancelar Edição
            ]),
            ft.Divider(height=20, color=ft.colors.GREY_300),
            ft.Text("Ocorrências Cadastradas", size=20, weight=ft.FontWeight.BOLD),
            self.ocorrencias_list,
        ])

    def salvar_ocorrencia(self, e):
        """
        Salva ou atualiza uma ocorrência no banco de dados.
        """
        if not self.nome_responsavel.value or not self.telefone_dropdown.value or not self.data_input.value or not self.relato.value:
            self.page.opem(ft.SnackBar(ft.Text("Preencha todos os campos obrigatórios."), bgcolor=ft.colors.RED)) 
            self.page.update()
            return

        # Monta os dados da ocorrência
        ocorrencia_data = {
            "nome_responsavel": self.nome_responsavel.value,
            "telefone": self.telefone_dropdown.value,
            "responsavel_registro": self.responsavel_registro.value,
            "rf_registro": self.rf_registro.value,
            "data": self.data_input.value,
            "relato": self.relato.value,
            "estrategia": self.estrategia.value,
            "encaminhamento": self.encaminhamento.value,
        }

        if self.editando_id:  # Se estiver editando uma ocorrência existente
            query = {"_id": self.editando_id}
            modificados = self.ocorrencias_db.atualiza(query=query, update_data=ocorrencia_data)
            if modificados > 0:
                self.page.open(ft.SnackBar(ft.Text("Ocorrência atualizada com sucesso!"), bgcolor=ft.colors.GREEN))
            else:
                self.page.open(ft.SnackBar(ft.Text("Erro ao atualizar a ocorrência."), bgcolor=ft.colors.RED))
        else:  # Se estiver criando uma nova ocorrência
            resultado = self.ocorrencias_db.create_with_aluno_id(self.aluno_id, ocorrencia_data)
            if resultado:
                self.page.open(ft.SnackBar(ft.Text("Ocorrência salva com sucesso!"), bgcolor=ft.colors.GREEN))
            else:
                self.page.open(ft.SnackBar(ft.Text("Erro ao salvar a ocorrência."), bgcolor=ft.colors.RED))

        self.limpar_formulario()
        self.carregar_ocorrencias()  # Atualiza a lista de ocorrências
        
        self.page.update()

    def carregar_ocorrencias(self):
        """
        Carrega e exibe as ocorrências associadas ao aluno.
        """
        ocorrencias = self.ocorrencias_db.ler_por_aluno(self.aluno_id)
        self.ocorrencias_list.controls.clear()
        if ocorrencias:
            for ocorrencia in ocorrencias:
                self.ocorrencias_list.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text(f"Responsável: {ocorrencia['nome_responsavel']}", weight=ft.FontWeight.BOLD),
                                ft.Text(f"Telefone: {ocorrencia['telefone']}"),
                                ft.Text(f"Data: {ocorrencia['data']}"),
                                ft.Text(f"Relatório: {ocorrencia['relato']}"),
                                ft.Text(f"Estratégia: {ocorrencia['estrategia']}"),
                                ft.Text(f"Encaminhamentos: {ocorrencia['encaminhamento']}"),
                                ft.Row([
                                    ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar", on_click=lambda e, oc=ocorrencia: self.editar_ocorrencia(oc)),
                                    ft.IconButton(icon=ft.icons.DELETE, tooltip="Excluir", on_click=lambda e, oc_id=ocorrencia["_id"]: self.apagar_ocorrencia(oc_id)),
                                    ft.IconButton(icon=ft.icons.PRINT, tooltip="Imprimir", on_click=lambda e, oc=ocorrencia: self.imprimir_ocorrencia(oc)),
                                ], alignment=ft.MainAxisAlignment.END),
                            ], spacing=5),
                            padding=10,
                        ),
                        elevation=3,
                    )
                )
        else:
            self.ocorrencias_list.controls.append(
                ft.Text("Nenhuma ocorrência cadastrada para este aluno.", italic=True, color=ft.colors.GREY_500)
            )
        self.page.update()

    def editar_ocorrencia(self, ocorrencia):
        """
        Carrega os dados de uma ocorrência no formulário para edição.
        """
        self.nome_responsavel.value = ocorrencia["nome_responsavel"]
        self.telefone_dropdown.value = ocorrencia["telefone"]
        self.data_input.value = ocorrencia["data"]
        self.relato.value = ocorrencia["relato"]
        self.estrategia.value = ocorrencia["estrategia"]
        self.encaminhamento.value = ocorrencia["encaminhamento"]

        # Define o ID da ocorrência sendo editada
        self.editando_id = ocorrencia["_id"]

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

    def apagar_ocorrencia(self, ocorrencia_id):
        """
        Remove uma ocorrência do banco de dados.
        """
        apagados = self.ocorrencias_db.apaga_por_aluno(self.aluno_id, {"_id": ocorrencia_id})
        if apagados > 0:
            self.page.snack_bar = ft.SnackBar(ft.Text("Ocorrência removida com sucesso!"), bgcolor=ft.colors.GREEN)
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Erro ao remover a ocorrência."), bgcolor=ft.colors.RED)
        self.page.snack_bar.open = True
        self.carregar_ocorrencias()
        self.page.update()

    def imprimir_ocorrencia(self, ocorrencia):
        """
        Abre uma nova janela com os detalhes da ocorrência para impressão.
        """
        dialog = ft.AlertDialog(
            title=ft.Text("Detalhes da Ocorrência"),
            content=ft.Column([
                ft.Text(f"Responsável: {ocorrencia['nome_responsavel']}", weight=ft.FontWeight.BOLD),
                ft.Text(f"Telefone: {ocorrencia['telefone']}"),
                ft.Text(f"Data: {ocorrencia['data']}"),
                ft.Text(f"Relatório: {ocorrencia['relato']}"),
                ft.Text(f"Estratégia: {ocorrencia['estrategia']}"),
                ft.Text(f"Encaminhamentos: {ocorrencia['encaminhamento']}"),
            ], spacing=5),
            actions=[
                ft.ElevatedButton("Fechar", on_click=lambda e: self.page.dialog.close()),
                ft.ElevatedButton("Imprimir", on_click=lambda e: self.abrir_impressao(ocorrencia)),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def abrir_impressao(self, ocorrencia):
        """
        Simula a abertura de uma janela de impressão.
        """
        print(f"Dados da ocorrência para impressão: {ocorrencia}")
        self.page.snack_bar = ft.SnackBar(ft.Text("Impressão realizada com sucesso!"), bgcolor=ft.colors.GREEN)
        self.page.snack_bar.open = True
        self.page.update()

    def limpar_formulario(self):
        """
        Limpa os campos do formulário.
        """
        self.nome_responsavel.value = ""
        self.telefone_dropdown.value = None
        self.data_input.value = ""
        self.relato.value = ""
        self.estrategia.value = ""
        self.encaminhamento.value = ""
        self.page.update()