import flet as ft
from dotenv import dotenv_values, set_key
import os

# Caminho para o arquivo .env
ENV_FILE = ".env"

# Dicionário com descrições para cada variável (labels explicativas)
VARIABLE_DESCRIPTIONS = {
    "LINK_MONGO": "URL de conexão com o banco de dados MongoDB",
    "DB_LOCAL": "Usar banco de dados local (TinyDB)",
    "TINYDB_DIR": "Diretório para salvar arquivos do TinyDB",
}

class Config:
    def __init__(self, page):
        self.page = page
        self.env_vars = dotenv_values(ENV_FILE)  # Carrega as variáveis do .env
        self.variable_inputs = {}  # Dicionário para armazenar os campos de entrada das variáveis
        self.db_nuvem = ft.Switch(
                label="Banco de dados na nuvem",
                value=False,
                on_change=self.toggle_visibility,
            )
            # Botões para upload de arquivos
        self.upload_matricula_btn = ft.ElevatedButton(
            "Upload Declaração de Matrícula",
            on_click=lambda _: self.set_tipo_arquivo("DECLARACAO_MATRICULA"),
        )

        self.upload_frequencia_btn = ft.ElevatedButton(
            "Upload Declaração de Frequência",
            on_click=lambda _: self.set_tipo_arquivo("DECLARACAO_FREQUENCIA"),
        )

        self.upload_ocorrencia_btn = ft.ElevatedButton(
            "Upload Ocorrência",
            on_click=lambda _: self.set_tipo_arquivo("OCORRENCIA"),
        )


        self.opçaodb = ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text("Banco de dados Local"),
                        ]
                    ),
                    ft.Column(
                        [
                            self.db_nuvem,
                        ]
                    ),
                ]
            )

        self.link_mongo = ft.TextField(label="Link MongoDB", width=300)

        self.coluna_mongo = ft.Row(
                controls=[
                    ft.Column(controls=[self.link_mongo]),
                    ft.Column(
                        controls=[
                            ft.ElevatedButton(
                                "Conectar ao MongoDB",
                                 on_click=lambda e: self.salva_mongo(e),
                            )
                        ]
                    ),
                ],
                visible=False,  # Inicialmente invisível
            )

        # Botão para selecionar a pasta
        self.selecionar_pasta_btn = ft.ElevatedButton(
            "Selecionar pasta",
            on_click=lambda e: self.diretorio_tiny(e),  # Corrigido para passar o argumento `e`
            visible=True,  # Inicialmente visível
        )

        self.tipo_arquivo = ""

        # Inicializa o FilePicker
        self.file_picker = ft.FilePicker(on_result=self.upload_files)
        self.page.overlay.append(self.file_picker)  # Adiciona o FilePicker ao overlay da página

    def salva_mongo(self,e):
        if self.link_mongo.value:
            print(f"Conectando ao MongoDB: {self.link_mongo.value}")
            set_key(ENV_FILE, "LINK_MONGO", self.link_mongo.value)
        else:
            print("Nenhum link fornecido.")

    def toggle_visibility(self,e):
        if self.db_nuvem.value:
            self.coluna_mongo.visible = True
            self.selecionar_pasta_btn.visible = False
        else:
            self.coluna_mongo.visible = False
            self.selecionar_pasta_btn.visible = True
        self.page.update()

    def diretorio_tiny(self,e):
        file_picker = ft.FilePicker(on_result=self.salva_diretorio)
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.get_directory_path()

    def salva_diretorio(self,e: ft.FilePickerResultEvent):
        tinydb_dir =e.path
        if tinydb_dir:
            if not os.path.exists(tinydb_dir):
                os.makedirs(tinydb_dir)
                self.page.open(ft.SnackBar(  ft.Text(f"Diretório criado: {tinydb_dir}"), bgcolor=ft.colors.GREEN)) 
            self.env_vars["TINYDB_DIR"] = tinydb_dir
            set_key(ENV_FILE, "TINYDB_DIR", tinydb_dir)
        else:
            self.page.open(ft.SnackBar(ft.Text("Informe um diretório válido!"), bgcolor=ft.colors.RED)) 

        self.page.update()
    
    def upload_files(self,e):
        if self.file_picker.result and self.file_picker.result.files:
            arquivo = self.file_picker.result.files[0]
            if self.tipo_arquivo == "DECLARACAO_MATRICULA":
                self.salvar_no_env("DECLARACAO_MATRICULA", arquivo.path)
            elif self.tipo_arquivo == "DECLARACAO_FREQUENCIA":
                self.salvar_no_env("DECLARACAO_FREQUENCIA", arquivo.path)
            elif self.tipo_arquivo == "OCORRENCIA":
                self.salvar_no_env("OCORRENCIA", arquivo.path)
        else:
            print("Nenhum arquivo enviado.")

    # Função para salvar o caminho do arquivo no .env
    def salvar_no_env(self,chave, caminho):
        set_key(ENV_FILE, chave, caminho)
        self.page.open(ft.SnackBar(
            ft.Text(f"Caminho salvo no .env: {chave} = {caminho}"), bgcolor=ft.Colors.GREEN
        )) 

        self.page.update()

    def set_tipo_arquivo(self,tipo):
        """
        Define o tipo de arquivo a ser enviado.
        """
        
        self.tipo_arquivo = tipo
        self.file_picker.pick_files()

    def build(self):
        """
        Constrói a interface da página de configuração.
        """
        return ft.Column([
           ft.Text("Configurações", size=24, weight="bold"),
            self.opçaodb,
            self.coluna_mongo,
            self.selecionar_pasta_btn,
            ft.Text("Upload de Modelos de Relatório:", size=18, weight="bold"),
            self.upload_matricula_btn,
            self.upload_frequencia_btn,
            self.upload_ocorrencia_btn,
        ], )


