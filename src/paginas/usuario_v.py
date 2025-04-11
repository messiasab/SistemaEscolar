import flet as ft
from model import UsuariosM  # Importa a classe de acesso ao MongoDB
import bcrypt  # Para criptografar senhas

def UsuariosView(page):
    # Instância do banco de dados
    usuarios_db = UsuariosM()

    if not page.session.get("usuario_logado"):
        page.go("/login")
        return
    if page.session.get("usuario_logado")["tipo"] != "Administrador":
        page.open(ft.SnackBar(ft.Text("Acesso negado!"), bgcolor=ft.colors.RED))
        page.update()
        # Se o usuário não for administrador, redireciona para a página inicial
        page.go("/")
        return
    # Controles da interface
    nome = ft.TextField(label="Nome")
    rf = ft.TextField(label="RF", keyboard_type=ft.KeyboardType.NUMBER)
    email = ft.TextField(label="E-mail", keyboard_type=ft.KeyboardType.EMAIL)
    senha = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        hint_text="Insira uma senha segura (opcional na edição)"
    )
    tipo_dropdown = ft.Dropdown(
        label="Tipo",
        autofocus=True,
        options=[
            ft.dropdown.Option("Professor"),
            ft.dropdown.Option("Secretario"),
            ft.dropdown.Option("Coordenador"),
            ft.dropdown.Option("Diretor"),
            ft.dropdown.Option("Administrador"),
        ],
    )

    # Variável para armazenar o ID do usuário sendo editado
    editando_id = None

    # Botão "Cancelar Edição"
    cancelar_edicao_button = ft.ElevatedButton(
        "Cancelar Edição",
        on_click=lambda e: cancelar_edicao(),
        visible=False,
    )

    # Lista de usuários
    usuarios_list = ft.ListView(spacing=10, height=300, auto_scroll=True)

    def carregar_usuarios():
        """
        Carrega e exibe os usuários cadastrados.
        """
        usuarios = usuarios_db.ler()
        usuarios_list.controls.clear()
        if usuarios:
            for usuario in usuarios:
                usuarios_list.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text(f"Nome: {usuario['nome']}", weight=ft.FontWeight.BOLD),
                                ft.Text(f"RF: {usuario['rf']}"),
                                ft.Text(f"E-mail: {usuario['email']}"),
                                ft.Text(f"Tipo: {usuario['tipo']}"),
                                ft.Row([
                                    ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar", on_click=lambda e, u=usuario: editar_usuario(u)),
                                    ft.IconButton(icon=ft.icons.DELETE, tooltip="Excluir", on_click=lambda e, u_id=usuario["_id"]: apagar_usuario(u_id)),
                                ], alignment=ft.MainAxisAlignment.END),
                            ], spacing=5),
                            padding=10,
                        ),
                        elevation=3,
                    )
                )
        else:
            usuarios_list.controls.append(
                ft.Text("Nenhum usuário cadastrado.", italic=True, color=ft.colors.GREY_500)
            )
        page.update()

    def mostrar_mensagem(mensagem, cor=ft.colors.GREEN):
        """
        Exibe uma mensagem usando SnackBar.
        """
        print(f"Mensagem a ser exibida: {mensagem}")  # Debugging
        page.open(ft.SnackBar(ft.Text(mensagem), bgcolor=cor))
        
        page.update()

    def salvar_usuario(e):
        """
        Salva ou atualiza um usuário no banco de dados.
        """
        if not nome.value or not rf.value or not email.value or not tipo_dropdown.value:
            mostrar_mensagem("Preencha todos os campos obrigatórios.", ft.colors.RED)
            return

        # Monta os dados do usuário
        usuario_data = {
            "nome": nome.value,
            "rf": rf.value,
            "email": email.value,
            "tipo": tipo_dropdown.value,
        }

        # Criptografa a senha apenas se ela for fornecida
        if senha.value:
            senha_criptografada = bcrypt.hashpw(senha.value.encode('utf-8'), bcrypt.gensalt())
            usuario_data["senha"] = senha_criptografada.decode('utf-8')  # Armazena a senha como string

        if editando_id:  # Se estiver editando um usuário existente
            query = {"_id": editando_id}
            modificados = usuarios_db.atualiza(query=query, update_data=usuario_data)
            if modificados > 0:
                mostrar_mensagem("Usuário atualizado com sucesso!")
            else:
                mostrar_mensagem("Erro ao atualizar o usuário.", ft.colors.RED)
        else:  # Se estiver criando um novo usuário
            if not senha.value:
                mostrar_mensagem("Senha é obrigatória para novos usuários.", ft.colors.RED)
                return
            resultado = usuarios_db.cria(usuario_data)
            if resultado:
                mostrar_mensagem("Usuário salvo com sucesso!")
            else:
                mostrar_mensagem("Erro ao salvar o usuário.", ft.colors.RED)

        # Limpa o formulário e redefine o estado
        limpar_formulario()
        carregar_usuarios()  # Atualiza a lista de usuários

    def editar_usuario(usuario):
        """
        Carrega os dados de um usuário no formulário para edição.
        """
        nonlocal editando_id
        nome.value = usuario["nome"]
        rf.value = usuario["rf"]
        email.value = usuario["email"]
        tipo_dropdown.value = usuario["tipo"]

        # Define o ID do usuário sendo editado
        editando_id = usuario["_id"]

        # Desativa o campo de senha inicialmente
        senha.value = ""
        senha.disabled = False  # Habilita o campo de senha para edição

        # Ativa o botão "Cancelar Edição"
        cancelar_edicao_button.visible = True

        # Altera o texto do botão "Salvar Usuário" para "Salvar Alterações"
        salvar_usuario_button.text = "Salvar Alterações"

        page.update()

    def cancelar_edicao():
        """
        Cancela a edição e limpa o formulário.
        """
        nonlocal editando_id
        editando_id = None
        limpar_formulario()

        # Desativa o botão "Cancelar Edição"
        cancelar_edicao_button.visible = False

        page.update()

    def apagar_usuario(usuario_id):
        """
        Remove um usuário do banco de dados.
        """
        apagados = usuarios_db.apaga({"_id": usuario_id})
        if apagados > 0:
            mostrar_mensagem("Usuário removido com sucesso!")
        else:
            mostrar_mensagem("Erro ao remover o usuário.", ft.colors.RED)
        carregar_usuarios()  # Atualiza a lista de usuários

    def limpar_formulario():
        """
        Limpa os campos do formulário.
        """
        nome.value = ""
        rf.value = ""
        email.value = ""
        senha.value = ""
        senha.disabled = False  # Habilita o campo de senha novamente
        tipo_dropdown.value = None  # Redefine o Dropdown para o estado inicial

        # Redefine o estado de edição
        nonlocal editando_id
        editando_id = None

        # Retorna o texto do botão "Salvar Usuário" para "Salvar Usuário"
        salvar_usuario_button.text = "Salvar Usuário"

        # Desativa o botão "Cancelar Edição"
        cancelar_edicao_button.visible = False

        page.update()

    # Botão "Salvar Usuário"
    salvar_usuario_button = ft.ElevatedButton("Salvar Usuário", on_click=salvar_usuario)

    # Carrega os usuários existentes
    carregar_usuarios()

    return ft.Column([
        ft.Text("Formulário de Usuários", size=24, weight=ft.FontWeight.BOLD),
        nome,
        rf,
        email,
        senha,
        tipo_dropdown,
        ft.Row([
            salvar_usuario_button,  # Botão Salvar Usuário
            cancelar_edicao_button,  # Botão Cancelar Edição
        ]),
        ft.Divider(height=20, color=ft.colors.GREY_300),
        ft.Text("Usuários Cadastrados", size=20, weight=ft.FontWeight.BOLD),
        usuarios_list,
    ])