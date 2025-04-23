import flet as ft

class HistoricoView():
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.historico_db = None  # Substitua por sua instância de banco de dados

        # Recupera o ID do aluno da sessão
        
        # Controles da interface
     

        # Carrega os históricos existentes
       

    def build(self):
        return ft.Column(
           
               [
                ft.Image(
                    src="SistemaEscolar/src/assets/g7.png",
                    width=300,
                    height=300,
                    fit=ft.ImageFit.CONTAIN,
                ),
                ft.Text(
                    "Histórico Escolar é um artigo em construção",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
               
                
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )