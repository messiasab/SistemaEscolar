import flet as ft
from model.colecao import ContatosM  # Importa o modelo de contatos

class ContatosView:
    def __init__(self, page):
        self.page = page
        # Corrigir a obtenção do aluno selecionado
        aluno_selecionado = self.page.session.get("aluno_selecionado")
        if aluno_selecionado:
            self.meualuno = aluno_selecionado['Nome']
            self.aluno_id = aluno_selecionado['_id']
            print(f"Aluno selecionado: {self.meualuno}")
        else:
            self.meualuno = None
            self.aluno_id = None

        self.contatos = ContatosM()  # Instancia o modelo de contatos
        self._criar_campos()
        self._criar_lista_contatos()
        self._criar_botao_adicionar()

    def _criar_campos(self):
        """Cria os campos do formulário."""
        self.nome = ft.TextField(label="Nome", width=300)
        self.telefone = ft.TextField(
            label="Telefone",
            width=300,
            on_change=self._formatar_telefone  # Formata o telefone enquanto o usuário digita
        )
        self.telefone_whatsapp = ft.Checkbox(label="Telefone funciona como WhatsApp")
        self.mail = ft.TextField(label="E-mail", width=300)
        self.link_redes = ft.TextField(label="Link de Redes Sociais", width=300)

    def _formatar_telefone(self, e):
        """Formata o valor do telefone no formato (xx) 9999-9999."""
        valor = e.control.value
        valor = ''.join(filter(str.isdigit, valor))  # Remove caracteres não numéricos
        if len(valor) > 2:
            valor = f"({valor[:2]}) {valor[2:]}"
        if len(valor) > 9:
            valor = f"{valor[:9]}-{valor[9:]}"
        e.control.value = valor
        e.control.update()

    def _criar_lista_contatos(self):
        """Cria a lista de contatos."""
        self.lista_contatos = ft.ListView(expand=True, spacing=10, padding=10)

    def _criar_botao_adicionar(self):
        """Cria o botão de adicionar contato."""
        self.adicionar_button = ft.ElevatedButton("Adicionar", on_click=self.adicionar_contato)

    def carregar_contatos(self):
        """Carrega os contatos do banco de dados e atualiza a lista."""
        if not self.aluno_id:
            print("Nenhum aluno selecionado para carregar contatos.")
            return

        contatos = self.contatos.ler_por_aluno(self.aluno_id)
        self.lista_contatos.controls.clear()  # Limpa a lista antes de atualizar
        for contato in contatos:
            self.lista_contatos.controls.append(
                ft.Row(
                    [
                        ft.Text(f"Nome: {contato['nome']}"),
                        ft.Text(f"Telefone: {contato['telefone']}"),
                        ft.Text(f"WhatsApp: {'Sim' if contato.get('telefone_whatsapp') else 'Não'}"),
                        ft.Text(f"E-mail: {contato['mail']}"),
                        ft.Text(f"Redes Sociais: {contato['link_redes']}"),
                        ft.IconButton(
                            icon=ft.icons.EDIT,
                            tooltip="Editar",
                            on_click=lambda e, c=contato: self.editar_contato(c),
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            tooltip="Excluir",
                            on_click=lambda e, c=contato: self.excluir_contato(c),
                        ),
                    ],
                    spacing=10,
                )
            )
        self.page.update()  # Atualiza a página para refletir as mudanças

    def editar_contato(self, contato):
        """Preenche os campos com os dados do contato para edição."""
        self.nome.value = contato["nome"]
        self.telefone.value = contato["telefone"]
        self.telefone_whatsapp.value = contato.get("telefone_whatsapp", False)
        self.mail.value = contato["mail"]
        self.link_redes.value = contato["link_redes"]
        self.page.update()

        # Atualiza o botão para salvar as alterações
        self.adicionar_button.text = "Salvar Alterações"
        self.adicionar_button.on_click = lambda e: self.salvar_edicao_contato(contato["_id"])
        self.adicionar_button.update()

    def salvar_edicao_contato(self, contato_id):
        """Salva as alterações feitas no contato."""
        if not self.nome.value or not self.telefone.value:
            self.page.open(
                ft.SnackBar(
                    content=ft.Text("Por favor, preencha todos os campos obrigatórios."),
                )
            )
            return

        contato_data = {
            "nome": self.nome.value,
            "telefone": self.telefone.value,
            "telefone_whatsapp": self.telefone_whatsapp.value,
            "mail": self.mail.value,
            "link_redes": self.link_redes.value,
        }

        self.contatos.atualiza({"_id": contato_id}, contato_data)
        self.carregar_contatos()  # Atualiza a lista de contatos
        self._limpar_campos()

        # Restaura o botão para adicionar novos contatos
        self.adicionar_button.text = "Adicionar"
        self.adicionar_button.on_click = self.adicionar_contato
        self.adicionar_button.update()

    def excluir_contato(self, contato):
        """Exclui o contato selecionado."""
        self.contatos.apaga({"_id": contato["_id"]})
        self.carregar_contatos()  # Atualiza a lista de contatos

    def adicionar_contato(self, e):
        """Adiciona um contato à lista."""
        if not self.nome.value or not self.telefone.value:
            self.page.open(
                ft.SnackBar(
                    content=ft.Text("Por favor, preencha todos os campos obrigatórios."),
                )
            )
            return

        contato_data = {
            "nome": self.nome.value,
            "telefone": self.telefone.value,
            "telefone_whatsapp": self.telefone_whatsapp.value,
            "mail": self.mail.value,
            "link_redes": self.link_redes.value,
        }

        self.contatos.create_with_aluno_id(aluno_id=self.aluno_id, data=contato_data)
        self.carregar_contatos()  # Atualiza a lista de contatos
        self._limpar_campos()

    def _limpar_campos(self):
        """Limpa os campos do formulário após adicionar um contato."""
        self.nome.value = ""
        self.telefone.value = ""
        self.telefone_whatsapp.value = False
        self.mail.value = ""
        self.link_redes.value = ""
        self.page.update()

    def build(self):
        """Constrói a interface da página."""
        # Adiciona os controles à página
        layout = ft.Column(
            [
                ft.Text(
                    f"Cadastro de Contatos para o Aluno: {self.meualuno}",
                    style="headlineMedium",
                ),
                self.nome,
                self.telefone,
                self.telefone_whatsapp,
                self.mail,
                self.link_redes,
                self.adicionar_button,
                ft.Divider(),
                ft.Text("Lista de Contatos", style="headlineSmall"),
                self.lista_contatos,
            ],
            expand=True,
        )

        # Carrega os contatos após a interface ser renderizada
        self.carregar_contatos()

        return layout

