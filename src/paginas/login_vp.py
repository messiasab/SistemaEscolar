import flet as ft
from model import UsuariosM  # Importa a classe de acesso ao MongoDB
import bcrypt  # Para verificar senhas criptografadas

def LoginView(page):
    # Instância do banco de dados
    usuarios_db = UsuariosM()

    # Controles da interface
    usuario = ft.TextField(label="Usuário", autofocus=True)
    senha = ft.TextField(label="Senha", password=True, can_reveal_password=True)
    mensagem = ft.Text("", size=14, color=ft.colors.RED)

    def autenticar_usuario(e):
        """
        Verifica se as credenciais fornecidas são válidas.
        """
        usuario_value = usuario.value.strip()
        senha_value = senha.value.strip()

        if not usuario_value or not senha_value:
            mensagem.value = "Preencha todos os campos."
            page.update()
            return

        # Busca o usuário no banco de dados
        query = {"rf": usuario_value}
        usuario_encontrado = usuarios_db.ler(query=query)

        if usuario_encontrado:
            # Recupera o hash da senha armazenado no banco de dados
            hash_senha_armazenada = usuario_encontrado[0].get("senha")

            # Verifica se a senha fornecida corresponde ao hash armazenado
            if hash_senha_armazenada and bcrypt.checkpw(senha_value.encode('utf-8'), hash_senha_armazenada.encode('utf-8')):
                # Credenciais válidas: Redireciona para a tela principal
                mensagem.value = ""
                page.session.set("usuario_logado", usuario_encontrado[0])  # Armazena o usuário logado na sessão
                page.go("/home")  # Redireciona para a tela principal
            else:
                # Senha inválida
                mensagem.value = "Usuário ou senha incorretos."
                page.update()
        else:
            # Usuário não encontrado
            mensagem.value = "Usuário ou senha incorretos."
            page.update()

    # Botão "Entrar"
    entrar_button = ft.ElevatedButton("Entrar", on_click=autenticar_usuario)

    return ft.Column(
        [
            ft.Text("Login", size=24, weight=ft.FontWeight.BOLD),
            usuario,
            senha,
            mensagem,
            entrar_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )