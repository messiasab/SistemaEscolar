import flet as ft
from model.colecao import OcorrenciasM, ContatosM, UsuariosM, AlunosM
from model.relat import RelatOcorrencia

class OcorrenciasView:
    def __init__(self, page):
        self.page = page
        self.aluno_id = None  # Certifique-se de que o aluno_id seja definido
        self.ocorrencias_db = OcorrenciasM()  # Instância do banco de dados de ocorrências

        # Inicializa a lista de ocorrências como um controle vazio
        self.lista_ocorrencias = ft.Column()  # Use ft.Column para armazenar as ocorrências

        # Carrega as ocorrências
        self.carregar_ocorrencias()

        # Recupera o ID do aluno da sessão
        self.aluno = self.page.session.get("aluno_selecionado")
        if not self.aluno:
            self.page.open(ft.SnackBar(ft.Text("Nenhum aluno selecionado."), bgcolor=ft.colors.RED))
            self.page.update()
            return
        else:
            self.aluno_id = self.aluno["_id"]
            self.aluno_nome = self.aluno["Nome"]
            print(f"Aluno selecionado: {self.aluno_nome}")
            print(f"Aluno selecionado com o ID: {self.aluno_id}")

        # Inicializa os bancos de dados
        self.ocorrencias_db = OcorrenciasM()
        self.contatos_db = ContatosM()
        self.usuarios_db = UsuariosM()
        self.alunos_db = AlunosM()

        # Recupera os contatos do aluno
        contatos = self.contatos_db.ler({"aluno_id": self.aluno_id})
        if not contatos:
            self.page.open(ft.SnackBar(ft.Text("Nenhum Contato cadastrado para o aluno."), bgcolor=ft.colors.RED))
            self.page.update()
            return

        # Cria um dicionário de contatos com nome e telefone
        self.telefones_disponiveis = {contato["nome"]: contato["telefone"] for contato in contatos}

        # Recupera o usuário logado
        self.usuario_logado = self.page.session.get("usuario_logado")
        if not self.usuario_logado:
            self.page.open(ft.SnackBar(ft.Text("Nenhum usuário logado."), bgcolor=ft.colors.RED))
            self.page.update()
            return

        # Controles da interface
        self.nome_responsavel = ft.TextField(label="Nome do Responsável")
        self.telefone_dropdown = ft.Dropdown(
            label="Contato",
            options=[ft.dropdown.Option(nome) for nome in self.telefones_disponiveis.keys()],
            on_change=self.preencher_campos_responsavel,  # Evento para preencher os campos automaticamente
        )
        self.telefone_input = ft.TextField(label="Telefone (Editável)")
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
        self.data_input = ft.TextField(
            label="Data",
            hint_text="DD/MM/AAAA",
            on_change=self.formatar_data,  # Evento para formatar a data
        )
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
          # Instância da classe Relat
        #self.report_data
    # Botão para salvar o relatório
    
    def build(self):
        return ft.Column([
            ft.Text("Formulário de Ocorrência", size=24, weight=ft.FontWeight.BOLD),
            self.nome_responsavel,
            self.telefone_dropdown,
            self.telefone_input,  # Campo editável para o telefone
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
            self.lista_ocorrencias,
        ])

    def salvar_ocorrencia(self, e):
        """
        Salva ou atualiza uma ocorrência no banco de dados.
        """
        # Verifica se estamos no modo de edição
        if self.editando_id:
            # Busca a ocorrência original no banco de dados
            ocorrencia_original = self.ocorrencias_db.ler({"_id": self.editando_id})
            if not ocorrencia_original:
                self.page.open(ft.SnackBar(ft.Text("Erro: Ocorrência não encontrada."), bgcolor=ft.Colors.RED))
                self.page.update()
                return
            ocorrencia_original = ocorrencia_original[0]

            # Atualiza apenas os campos preenchidos
            ocorrencia_data = {
                "nome_responsavel": self.nome_responsavel.value or ocorrencia_original["nome_responsavel"],
                "telefone": self.telefone_input.value or ocorrencia_original["telefone"],
                "responsavel_registro": self.responsavel_registro.value or ocorrencia_original["responsavel_registro"],
                "rf_registro": self.rf_registro.value or ocorrencia_original["rf_registro"],
                "data": self.data_input.value or ocorrencia_original["data"],
                "relato": self.relato.value or ocorrencia_original["relato"],
                "estrategia": self.estrategia.value or ocorrencia_original["estrategia"],
                "encaminhamento": self.encaminhamento.value or ocorrencia_original["encaminhamento"],
            }

            # Atualiza a ocorrência no banco de dados
            query = {"_id": self.editando_id}
            modificados = self.ocorrencias_db.atualiza(query=query, update_data=ocorrencia_data)
            if modificados > 0:
                self.page.open(ft.SnackBar(ft.Text("Ocorrência atualizada com sucesso!"), bgcolor=ft.Colors.GREEN))
            else:
                self.page.open(ft.SnackBar(ft.Text("Erro ao atualizar a ocorrência."), bgcolor=ft.Colors.RED))
        else:
            # Valida os campos obrigatórios para uma nova ocorrência
            if not self.nome_responsavel.value or not self.telefone_input.value or not self.data_input.value or not self.relato.value:
                self.page.open(ft.SnackBar(ft.Text("Preencha todos os campos obrigatórios."), bgcolor=ft.Colors.RED))
                self.page.update()
                return

            # Monta os dados da nova ocorrência
            ocorrencia_data = {
                "nome_responsavel": self.nome_responsavel.value,
                "telefone": self.telefone_input.value,
                "responsavel_registro": self.responsavel_registro.value,
                "rf_registro": self.rf_registro.value,
                "data": self.data_input.value,
                "relato": self.relato.value,
                "estrategia": self.estrategia.value,
                "encaminhamento": self.encaminhamento.value,
            }

            # Salva a nova ocorrência no banco de dados
            resultado = self.ocorrencias_db.cria(self.aluno_id, ocorrencia_data)
            if resultado:
                self.page.open(ft.SnackBar(ft.Text("Ocorrência salva com sucesso!"), bgcolor=ft.Colors.GREEN))
            else:
                self.page.open(ft.SnackBar(ft.Text("Erro ao salvar a ocorrência."), bgcolor=ft.Colors.RED))

        # Limpa o formulário e recarrega as ocorrências
        self.limpar_formulario()
        self.carregar_ocorrencias()
        self.page.update()

    def carregar_ocorrencias(self):
        """Carrega as ocorrências do banco de dados e exibe usando ft.Card."""
        if not self.aluno_id:
            print("Nenhum aluno selecionado para carregar ocorrências.")
            return

        # Certifique-se de que o filtro seja um dicionário válido
        query = {"aluno_id": self.aluno_id}
        ocorrencias = self.ocorrencias_db.ler(query)  # Passa o filtro como um dicionário

        if not ocorrencias:
            print("Nenhuma ocorrência encontrada para o aluno.")
            return

        self.lista_ocorrencias.controls.clear()  # Limpa a lista antes de atualizar
        for ocorrencia in ocorrencias:
            self.lista_ocorrencias.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f"Responsável: {ocorrencia.get('nome_responsavel', 'N/A')}", weight=ft.FontWeight.BOLD),
                            ft.Text(f"Telefone: {ocorrencia.get('telefone', 'N/A')}"),
                            ft.Text(f"Data: {ocorrencia.get('data', 'N/A')}"),
                            ft.Text(f"Relatório: {ocorrencia.get('relato', 'N/A')}"),
                            ft.Text(f"Estratégia: {ocorrencia.get('estrategia', 'N/A')}"),
                            ft.Text(f"Encaminhamentos: {ocorrencia.get('encaminhamento', 'N/A')}"),
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
        self.page.update()  # Atualiza a página para refletir as mudanças

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
        apagados = self.ocorrencias_db.apaga({"_id": ocorrencia_id})
        if apagados > 0:
            self.page.open(ft.SnackBar(ft.Text("Ocorrência removida com sucesso!"), bgcolor=ft.colors.GREEN)) 
        else:
            self.page.open( ft.SnackBar(ft.Text("Erro ao remover a ocorrência."), bgcolor=ft.colors.RED))
       
        self.carregar_ocorrencias()
        self.page.update()

    def imprimir_ocorrencia(self, ocorrencia):
        """
        Gera um relatório da ocorrência e solicita o local para salvar.
        """
        prefixo = "D_"
        from datetime import datetime
        hoje = datetime.now()

        infor = {"D_hoje": str(hoje.strftime("%d/%m/%Y"))}
        D_ocorrencia = {f"{prefixo}{key}": value for key, value in ocorrencia.items()}
        D_ocorrencia1 = {f"{prefixo}{key}": value for key, value in self.aluno.items()}
        D_ocorrencia.update(infor)
        D_ocorrencia.update(D_ocorrencia1)

        print("Imprimindo ocorrência: ")

        # Instância da classe RelatOcorrencia
        self.relatorio = RelatOcorrencia(self.page)

        # Solicita o local para salvar o relatório
       
        self.relatorio.salvar_relatorio(D_ocorrencia)
        #self.page.update()

    

    def abrir_impressao(self, ocorrencia):
        """
        Simula a abertura de uma janela de impressão.
        """
        print(f"Dados da ocorrência para impressão: {ocorrencia}")
        self.page.open(ft.SnackBar(ft.Text("Impressão realizada com sucesso!"), bgcolor=ft.colors.GREEN))
        
        self.page.update()

    def limpar_formulario(self):
        """
        Limpa os campos do formulário.
        """
        self.nome_responsavel.value = ""
        self.telefone_dropdown.value = None
        self.telefone_input.value = ""
        self.data_input.value = ""
        self.relato.value = ""
        self.estrategia.value = ""
        self.encaminhamento.value = ""
        self.page.update()

    def preencher_campos_responsavel(self, e):
        """
        Preenche automaticamente os campos "Nome do Responsável" e "Telefone"
        com base no contato selecionado no Dropdown.
        """
        nome_selecionado = e.control.value
        if nome_selecionado in self.telefones_disponiveis:
            self.nome_responsavel.value = nome_selecionado
            self.telefone_input.value = self.telefones_disponiveis[nome_selecionado]
            self.page.update()

    def formatar_data(self, e):
        """
        Formata o valor do campo de data no formato DD/MM/AAAA enquanto o usuário digita.
        """
        valor = e.control.value
        valor = ''.join(filter(str.isdigit, valor))  # Remove caracteres não numéricos

        if len(valor) > 2:
            valor = f"{valor[:2]}/{valor[2:]}"
        if len(valor) > 5:
            valor = f"{valor[:5]}/{valor[5:]}"
        
        e.control.value = valor
        e.control.update()