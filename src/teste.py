import flet as ft
from model.relat import RelatOcorrencia


def main(page: ft.Page):
    page.title = "Gerador de Relatórios"

    # Caminho para o modelo .docx
    

    # Dados fictícios para o relatório
    report_data = {
        "D_Nome": "João da Silva",
        "D_hoje": "01/10/2023",
        "D_Turma": "R$ 1.500,00",
        
    }

    # Instância da classe Relat
    relat = RelatOcorrencia(page)

    # Botão para salvar o relatório
    def btn_save_click(e):
        relat.salvar_relatorio(report_data)

    # Interface do usuário
    page.add(
        ft.Text("Gerador de Relatórios", size=24, weight="bold"),
        ft.ElevatedButton("Salvar Relatório", on_click=btn_save_click),
    )


ft.app(target=main)