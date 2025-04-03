import flet as ft
#from paginas.aluno_v import AlunosView
from paginas.contatos_v import ContatosView
from paginas.atestado_v import AtestadosView
from paginas.ocorrencias_v import OcorrenciasView
from paginas.registros_v import RegistroTelefonicoView
from paginas.aluno_v import Alunos_v
from model import AlunosM

class AlunosView:
    def __init__(self, page):
        self.page = page
        self.alunos_db = AlunosM()
        self.content_area = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,  # Garante que o conteúdo ocupe o espaço disponível
        )
        self.rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.SEARCH,
                    selected_icon=ft.icons.SEARCH_OUTLINED,
                    label="Busca",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.ADD,
                    selected_icon=ft.icons.ADD_CIRCLE,
                    label="Novo",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.CONTACT_PHONE,
                    selected_icon=ft.icons.CONTACT_PHONE_OUTLINED,
                    label="Contatos",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.DOCUMENT_SCANNER,
                    selected_icon=ft.icons.DOCUMENT_SCANNER_OUTLINED,
                    label="Documentos",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.MEDICAL_SERVICES,
                    selected_icon=ft.icons.MEDICAL_SERVICES_OUTLINED,
                    label="Atestados",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.REPORT,
                    selected_icon=ft.icons.REPORT_PROBLEM,
                    label="Ocorrências",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.PHONE,
                    selected_icon=ft.icons.PHONE_CALLBACK,
                    label="Registro Telefônico",
                ),
            ],
            on_change=self.update_content,
        )

    def update_content(self, e):
        index = e.control.selected_index
        self.content_area.controls.clear()
        if index == 0:
            self.content_area.controls.append(Alunos_v(self.page))
        elif index == 1:
            
            self.content_area.controls.append(ft.Text('teste'))
        elif index == 2:
            contato= ContatosView()
            self.content_area.controls.append(contato.)    
        elif index == 3:
            ocorrencias=OcorrenciasView()
            self.content_area.controls.append(ocorrencias.create_view())
        elif index == 4:
            atestado= AtestadosView(self.page)
            self.content_area.controls.append(atestado.build())    
        elif index == 5:
            ocorrencia= OcorrenciasView(self.page)
            self.content_area.controls.append(ocorrencia.build())     
        elif index == 6:
            registro= RegistroTelefonicoView(self.page)
            self.content_area.controls.append(registro.build())    
        self.page.update()

    def create_view(self):
        return ft.Row(
            [
                # Envolve o NavigationRail em um Container com altura fixa
                ft.Container(
                    content=self.rail,
                    height=600,  # Define uma altura fixa para o NavigationRail
                    padding=ft.padding.all(10),
                ),
                ft.VerticalDivider(width=1),
                ft.Column([self.content_area], expand=True, alignment=ft.MainAxisAlignment.CENTER),
            ],
            expand=True,  # Faz o Row ocupar todo o espaço disponível
        )