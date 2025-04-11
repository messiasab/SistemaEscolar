# views/import_view.py
import flet as ft
from pathlib import Path
from model.mongodb_importer import import_data_to_mongodb
from model.colecao import AlunosM, NotasM, ContatosM, AtestadosM, OcorrenciasM, UsuariosM

def Importes_v(page):
    file_path = None
    selected_collection_class = AlunosM  # Valor padrão para a coleção

    # Função para lidar com a seleção do Dropdown
    def on_collection_change(e):
        nonlocal selected_collection_class
        collection_name = e.control.value

        # Mapeia o nome da coleção para a classe correspondente
        selected_collection_class = {
            "Alunos": AlunosM,
            "Notas": NotasM,
            "Contatos": ContatosM,
            "Atestados": AtestadosM,
            "Ocorrencias": OcorrenciasM,
            "Usuarios": UsuariosM,
        }[collection_name]

        # Instancia a classe da coleção selecionada
        collection_instance = selected_collection_class()
        print(f"Classe selecionada: {collection_instance.__class__.__name__}")
        print(f"campos: {collection_instance.campos}")
        # Obtém os campos da coleção (supondo que a classe tenha um método ou atributo `get_campos`)
        campos = collection_instance.campos # Ajuste conforme a implementação da classe
        print(f"Campos da coleção {collection_name}: {campos}")
        # Atualiza o texto do modelo com os campos da coleção selecionada
        modelo.value = f"Modelo de colunas: {campos}"
        modelo.update()

    # Função para selecionar o arquivo
    def pick_file(e: ft.FilePickerResultEvent):
        nonlocal file_path
        if e.files:
            file_path = e.files[0].path
            file_name.value = f"Arquivo selecionado: {Path(file_path).name}"
            file_name.update()
        else:
            file_name.value = "Nenhum arquivo selecionado."
            file_name.update()

    # Função para importar os dados
    def import_data(e):
        if not file_path:
            status.value = "Por favor, selecione um arquivo primeiro."
            status.color = "red"
            status.update()
            return

        try:
            # Instanciar a classe da coleção selecionada
            collection_instance = selected_collection_class()
            
            # Importar os dados para a coleção selecionada
            success, message = import_data_to_mongodb(file_path, collection_instance.collection)
            if success:
                status.value = message
                status.color = "green"
            else:
                status.value = message
                status.color = "red"
            status.update()
        except Exception as ex:
            status.value = f"Erro ao conectar ao MongoDB: {str(ex)}"
            status.color = "red"
            status.update()

    # Componentes da interface
    file_picker = ft.FilePicker(on_result=pick_file)
    file_name = ft.Text("Nenhum arquivo selecionado.", size=16)

    # Dropdown para escolher a coleção
    collection_dropdown = ft.Dropdown(
        label="Escolha a Coleção",
        options=[
            ft.dropdown.Option("Alunos"),
            ft.dropdown.Option("Notas"),
            ft.dropdown.Option("Contatos"),
            ft.dropdown.Option("Atestados"),
            ft.dropdown.Option("Ocorrencias"),
            ft.dropdown.Option("Usuarios"),
        ],
        value="Alunos",  # Valor padrão
        on_change=on_collection_change,
    )

    import_button = ft.ElevatedButton("Importar Dados", on_click=import_data)
    status = ft.Text("", size=16)
    modelo = ft.Text(f"Modelo de colunas: ", size=16)  # Inicializa o texto do modelo
    page.overlay.append(file_picker)

    return ft.Column(
        [
            ft.Text("Importador de Planilha para MongoDB", size=24, weight="bold"),
            collection_dropdown,  # Adiciona o Dropdown à interface
            modelo,
            file_name,
            ft.ElevatedButton("Selecionar Planilha", on_click=lambda _: file_picker.pick_files(allow_multiple=False)),
            import_button,
            status,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )