import flet as ft
import os
from dotenv import set_key, dotenv_values

# Caminho para o arquivo .env
ENV_FILE = ".env"

def main(page: ft.Page):
    # Configuração inicial
    page.title = "Configurações"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Carrega as variáveis do arquivo .env
    env_vars = dotenv_values(ENV_FILE)

    # Variáveis para armazenar o nome do arquivo e o tipo de arquivo
    pasta_selecionada = ""
    tipo_arquivo = ""
    print(f"Variáveis do .env: {env_vars['DOC_WEB_URL_O']}")
    # Função para alternar visibilidade com base no Switch
    def toggle_visibility(e):
        if db_nuvem.value:
            coluna_mongo.visible = True
            selecionar_pasta_btn.visible = False
        else:
            coluna_mongo.visible = False
            selecionar_pasta_btn.visible = True
        page.update()

    # Opções de banco de dados
    db_nuvem = ft.Switch(
        label="Banco de dados na nuvem",
        value=False,
        on_change=toggle_visibility,
    )

    opçaodb = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("Banco de dados Local"),
                ]
            ),
            ft.Column(
                [
                    db_nuvem,
                ]
            ),
        ]
    )

    link_mongo = ft.TextField(label="Link MongoDB", width=300)

    coluna_mongo = ft.Row(
        controls=[
            ft.Column(controls=[link_mongo]),
            ft.Column(
                controls=[
                    ft.ElevatedButton(
                        "Conectar ao MongoDB",
                        on_click=lambda e: salva_mongo(e),
                    )
                ]
            ),
        ],
        visible=False,  # Inicialmente invisível
    )

    # Função para tratar o resultado da seleção de arquivo
    def diretorio_tiny(e):
        file_picker = ft.FilePicker(on_result=salva_diretorio)
        page.overlay.append(file_picker)
        page.update()
        file_picker.get_directory_path()

    # Configuração do FilePicker
    def salva_diretorio(e: ft.FilePickerResultEvent):
        if e.path:
            pasta_selecionada = e.path
            print(f"Pasta selecionada: {pasta_selecionada}")
        else:
            print("Nenhuma pasta selecionada.")

    def salva_mongo(e):
        if link_mongo.value:
            print(f"Conectando ao MongoDB: {link_mongo.value}")
        else:
            print("Nenhum link fornecido.")

    # Função para baixar arquivos
    def download_file(file_name):
        file_path = os.path.join(os.getcwd(), file_name)
        with open(file_path, "w") as f:
            f.write(f"Conteúdo do arquivo {file_name}")
        page.launch_url(file_path)

    # Função para tratar o upload de arquivos
    def upload_files(e):
        if file_picker.result and file_picker.result.files:
            arquivo = file_picker.result.files[0]
            if tipo_arquivo == "DECLARACAO_MATRICULA":
                salvar_no_env("DECLARACAO_MATRICULA", arquivo.path)
            elif tipo_arquivo == "DECLARACAO_FREQUENCIA":
                salvar_no_env("DECLARACAO_FREQUENCIA", arquivo.path)
            elif tipo_arquivo == "OCORRENCIA":
                salvar_no_env("OCORRENCIA", arquivo.path)
        else:
            print("Nenhum arquivo enviado.")

    # Função para salvar o caminho do arquivo no .env
    def salvar_no_env(chave, caminho):
        set_key(ENV_FILE, chave, caminho)
        page.snack_bar = ft.SnackBar(
            ft.Text(f"Caminho salvo no .env: {chave} = {caminho}"), bgcolor=ft.Colors.GREEN
        )
        page.snack_bar.open = True
        page.update()

    # Função para definir o tipo de arquivo e abrir o FilePicker
    def set_tipo_arquivo(tipo):
        nonlocal tipo_arquivo
        tipo_arquivo = tipo
        file_picker.pick_files()

    # Botões para download de arquivos
    download_btns = ft.Row(
        controls=[
            ft.ElevatedButton("Baixar arquivo 1", on_click=lambda e: download_file("arquivo1.txt")),
            ft.ElevatedButton("Baixar arquivo 2", on_click=lambda e: download_file("arquivo2.txt")),
            ft.ElevatedButton("Baixar arquivo 3", on_click=lambda e: download_file("arquivo3.txt")),
        ]
    )

    # Botão para upload de arquivos
    file_picker = ft.FilePicker(on_result=upload_files)
    page.overlay.append(file_picker)

    upload_btn = ft.ElevatedButton(
        "Fazer upload de arquivos",
        on_click=lambda _: file_picker.pick_files(allow_multiple=True),
    )

    # Botão para selecionar a pasta
    selecionar_pasta_btn = ft.ElevatedButton(
        "Selecionar pasta",
        on_click=diretorio_tiny,
        visible=True,  # Inicialmente visível
    )

    # Botões para upload de arquivos
    upload_matricula_btn = ft.ElevatedButton(
        "Upload Declaração de Matrícula",
        on_click=lambda _: set_tipo_arquivo("DECLARACAO_MATRICULA"),
    )

    upload_frequencia_btn = ft.ElevatedButton(
        "Upload Declaração de Frequência",
        on_click=lambda _: set_tipo_arquivo("DECLARACAO_FREQUENCIA"),
    )

    upload_ocorrencia_btn = ft.ElevatedButton(
        "Upload Ocorrência",
        on_click=lambda _: set_tipo_arquivo("OCORRENCIA"),
    )

    # Interface do usuário
    page.add(
        ft.Text("Configurações", size=24, weight="bold"),
        opçaodb,
        coluna_mongo,
        selecionar_pasta_btn,
       
        ft.Text("Upload de Modelos de Relatório:", size=18, weight="bold"),
        upload_matricula_btn,
        upload_frequencia_btn,
        upload_ocorrencia_btn,
    )

    page.update()


ft.app(target=main)