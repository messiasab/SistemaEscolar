import flet as ft
from datetime import datetime
from model.relat import RelatMatricula, RelatFrequencia
import locale
from datetime import datetime

# Configura o locale para português do Brasil

class DocumentosView:
    def __init__(self, page):
        self.page = page
        # Corrigir a obtenção do aluno selecionado
        aluno_selecionado = self.page.session.get("aluno_selecionado")
        locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
        if aluno_selecionado:
            # Verifica se o aluno selecionado existe    
            if  aluno_selecionado['Período']== "Manhã":
                horario = "07:00 às 12:00"
            elif aluno_selecionado['Período']== "Tarde":
                horario = "13:00 às 18:00"
            elif aluno_selecionado['Período']== "Noite":
                horario = "19:00 às 23:00"

            edata_hoje = {"D_hoje" : str(datetime.now().strftime("%d de %B de %Y")), "D_ano" : str(datetime.now().strftime("%Y")), "D_hororio" : str(horario)}
            print(type(aluno_selecionado))
            print(aluno_selecionado)
           
            self.meualuno = aluno_selecionado['Nome']
            prefixo = "D_"
            self.dados= {f"{prefixo}{key}": value for key, value in aluno_selecionado.items()}
            self.dados.update(edata_hoje)
            

            # Supondo que self.dados["D_Data_Nascimento"] possa ser uma string ou um objeto datetime
            if "D_Data_Nascimento" in self.dados:
                try:
                    # Verifica se o valor é uma string
                    if isinstance(self.dados["D_Data_Nascimento"], str):
                        # Converte a string para um objeto datetime
                        data_nascimento = datetime.strptime(self.dados["D_Data_Nascimento"], "%Y-%m-%d")
                    elif isinstance(self.dados["D_Data_Nascimento"], datetime):
                        # Se já for um objeto datetime, usa diretamente
                        data_nascimento = self.dados["D_Data_Nascimento"]
                    else:
                        raise ValueError("Formato inesperado para D_Data_Nascimento.")

                    # Formata a data no formato "dia/mês/ano"
                    self.dados["D_Data_Nascimento"] = data_nascimento.strftime("%d/%m/%Y")
                except ValueError as e:
                    print(f"Erro ao formatar a data de nascimento: {e}")
            print(f"dados dp relatorio: {self.dados}")

    def gerar_frequencia(self, e):
        """Gera a declaração de frequência."""
        print("Gerando declaração de frequência...")


    def gerar_transferencia(self, e):
        """Gera a declaração de transferência."""
        print("Gerando declaração de transferência...")


    def gerar_metricula(self, e):
        """Gera a declaração de matrícula."""
        print("Gerando declaração de matrícula...")
        matri=RelatMatricula(self.page)
        matri.salvar_relatorio(self.dados)
        
        
    def build(self):
        """Constrói a interface da página."""
        ft.ListView


        return ft.Column(
            [
                ft.Text(
                    f" Documentos para  o Aluno: {self.meualuno}",
                    style="headlineMedium",
                ),
                ft.FilledButton("Delaração de Frequencia", on_click=self.gerar_frequencia),
                ft.FilledButton("Declaração de Transferência", on_click=self.gerar_transferencia),
                ft.FilledButton("Declaração de Matrícula", on_click=self.gerar_metricula),
                
               
            ],
            expand=True,
        )

