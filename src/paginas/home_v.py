import flet as ft

from paginas.aluno_v import AlunosView
from paginas.atestado_v import AtestadosView
from paginas.contatos_v import ContatosView
from paginas.documentos_v import DocumentosView
from paginas.ocorrencias_v import OcorrenciasView
from paginas.registros_v import RegistroTelefonicoView
from paginas.contatos_v import ContatosM

from model import AlunosM

class HomeView:
    def __init__(self, page):
        self.page = page
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
            # Instanciar e chamar a classe AlunosView para busca
            alunos_view = AlunosView(self.page)
            self.content_area.controls.append(alunos_view.build())
        elif index == 1:
            # Instanciar e chamar a classe AlunosView para inserção de novos alunos
            alunos_view = AlunosView(self.page)
            self.content_area.controls.append(alunos_view.build_new_aluno_form())
        elif index == 2:
            # Página de contatos
            contato = ContatosView(self.page)
            self.content_area.controls.append(verificar_aluno_selecionado(self.page, contato))
        elif index == 3:
            # Documentos
            documentos = DocumentosView(self.page)
            self.content_area.controls.append(verificar_aluno_selecionado(self.page, documentos))
        elif index == 4:
            # Página de atestados
            atestado = AtestadosView(self.page)
            self.content_area.controls.append(verificar_aluno_selecionado(self.page, atestado))
        elif index == 5:
            # Outra página de ocorrências
            ocorrencia = OcorrenciasView(self.page)
            self.content_area.controls.append(verificar_aluno_selecionado(self.page, ocorrencia))
        elif index == 6:
            # Página de registro telefônico
            registro = RegistroTelefonicoView(self.page)
            self.content_area.controls.append(verificar_aluno_selecionado(self.page, registro))
        else:
             # Instanciar e chamar a classe AlunosView para busca
            alunos_view = AlunosView(self.page)
            self.content_area.controls.append(alunos_view.build())
            
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

def verificar_aluno_selecionado(page, componente):
    """Verifica se há um aluno selecionado na sessão e retorna o conteúdo apropriado."""
    aluno_selecionado = page.session.get("aluno_selecionado")
    if aluno_selecionado:
        return componente.build()
    else:
        return ft.Text(
            "Nenhum aluno selecionado. Por favor, selecione um aluno.",
            style="headlineMedium",
            color=ft.colors.RED,
        )