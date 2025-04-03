import flet as ft
from datetime import datetime
import math
from model.colecao import AlunosM
alunos_db = AlunosM()

# Função para criar o conteúdo da página "Alunos"
def Alunos_v(page):
    form_fields = {}
    def handle_change(e):
            valor = e.control.value
            if len(valor) > 3:
                
                query = {'Nome': {"$regex": valor, "$options": "i"}}
                print(f"Valor digitado: {valor}")
                print(f"Query gerada: {query}")
                sugestoes = alunos_db.ler(query)
                nomes = [sugestao['Nome'] for sugestao in sugestoes]  # Extrai apenas os nomes
                print(f"Sugestões retornadas: {nomes}")
                
                suggestions_column.controls.clear()
                        
                for nome in nomes:
                    suggestions_column.controls.append(
                        ft.ListTile(
                            title=ft.Text(nome),
                            on_click=lambda e, nome=nome: select_suggestion(nome),
                        )
                    )
               
                page.update()
                
    def select_suggestion(nome):
       
         # Preenche o campo de pesquisa com o valor selecionado
        bnome.value = nome

        # Recupera todos os dados do aluno selecionado usando o método ler
        aluno_selecionado = alunos_db.ler(query={"Nome": nome})
        print(f"EOL do alino selecionado : {aluno_selecionado[0]['EOL']}")
        
        if aluno_selecionado:
            aluno_selecionado = aluno_selecionado[0]  # Assume que só há um aluno com esse nome
           
            print(f"Dados do aluno selecionado: {aluno_selecionado}")
            
            # Exibe os dados do aluno no formulário
            display_aluno_form(aluno_selecionado)
        
        # Limpa as sugestões

        suggestions_column.controls.clear()
        page.update()

    # Cria o TextField para pesquisa
    bnome = ft.TextField(
        hint_text="Pesquise por nome...",
        on_change=lambda e: handle_change(e),
        
        expand=True,
    )      
    beol = ft.TextField(
        hint_text="Pesquise por EOL...",
        
        on_submit=lambda e: handle_submit(e),
        expand=True,
    )      

    def format_value(value):
        """
        Formata valores especiais para exibição no formulário.
        - Converte NaN para string vazia.
        - Formata datas como 'DD/MM/YYYY'.
        - Converte números para string.
        """
        if isinstance(value, float) and math.isnan(value):  # Verifica se é NaN
            return ""
        elif isinstance(value, datetime):  # Formata datas
            return value.strftime("%d/%m/%Y")
        else:
            return str(value)
    # Cria o ListView para o formulário (com barra de rolagem)
    form_scroll_view = ft.ListView(
        controls=[],  # Inicialmente vazio
        spacing=10,   # Espaçamento entre os controles
        height=400,   # Altura máxima do formulário (ajustável)
        auto_scroll=True,  # Rola automaticamente ao adicionar novos controles
    )

    # Cria o container para o formulário
    form_container = ft.Container(
        content=form_scroll_view,  # O conteúdo é o ListView com barra de rolagem
        padding=20,
        border=ft.border.all(1, ft.colors.BLUE),
        border_radius=10,
        visible=False,  # Inicialmente invisível
    )


    def display_aluno_form(aluno):
        # Limpa o formulário anterior, se existir
        page.session.set("aluno_id", aluno['_id'])
        form_scroll_view.controls.clear()
        beol.visible=False
        # Cria os campos do formulário com base nos dados do aluno
        for key, value in aluno.items():
            formatted_value = format_value(value)  # Formata o valor para exibição
            form_fields[key] = ft.TextField(
                label=key,
                value=formatted_value,
                multiline=(key == "Endereço" or key == "Observações"),  # Permite múltiplas linhas para campos longos
            )
            form_scroll_view.controls.append(form_fields[key])

        # Adiciona um botão para salvar as alterações
        form_scroll_view.controls.append(
            ft.ElevatedButton("Salvar Alterações", on_click=lambda e: save_changes(aluno))
        )

        # Torna o formulário visível
        form_container.visible = True
        page.update()

    def save_changes(aluno):
        # Recupera os valores atualizados dos campos do formulário
        updated_data = {key: field.value for key, field in form_fields.items()}
        updated_data.pop("_id", None)
        print(f"Dados atualizados: {updated_data}")

        # Atualiza os dados no MongoDB usando o método atualiza
        query = {"_id": aluno["_id"]}
        modificados = alunos_db.atualiza(query=query, update_data=updated_data)

        # Feedback ao usuário
        if modificados > 0:
            page.snack_bar = ft.SnackBar(ft.Text("Alterações salvas com sucesso!"))
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Erro ao salvar alterações."))
        page.snack_bar.open = True
        page.update()

    # Cria o TextField para pesquisa
    

    def handle_submit(e):
        """
        Manipula o evento on_submit para realizar a busca final.
        - campo: Nome do campo ("nome" ou "EOL")
        """
        valor = e.control.value
        print(f"esse foi o eol selecionado: {valor}")
        if len(valor) > 6:
            print(type(valor))
            query = {"EOL": valor}
            print(f"Query gerada: {query}")
            # Projeção para retornar apenas o campo 'nome'
            resultados = alunos_db.ler(query)
            print(f"Dados do aluno selecionado: {resultados}")
            if resultados:
                resultados = resultados[0]  # Assume que só há um aluno com esse nome
                print(f"Dados do aluno selecionado: {resultados}")
                bnome.value = resultados['Nome']
                display_aluno_form(resultados)

           
           
    
    
    

    

    # Criação do primeiro campo de pesquisa (bnome - 55% da largura)
    suggestions_column = ft.Column(
        controls=[],
        spacing=2,
    )
    suggestions_column_eol = ft.Column(
        controls=[],
        spacing=2,
    )
    boxNome=ft.Column(
            expand=True,
            controls=[
                bnome,
                suggestions_column,
            ],
        )
    
    boxeol=ft.Column(
            expand=True,
            controls=[
                beol,
                suggestions_column_eol,
            ],

        )
    

    # Criação do segundo campo de pesquisa (beol - 35% da largura)
    

   

    # Layout principal com os campos de pesquisa lado a lado
    return ft.Column(
        expand=True,  # Ocupa todo o espaço disponível na página
        controls=[
            # Botões para abrir os campos de pesquisa
           
            ft.Row(
                expand=True,  # Ocupa toda a largura disponível
                controls=[
                    ft.Container(
                        expand=5,  # Proporção 5/8 (55%)
                        content=boxNome,
                    ),
                    ft.Container(
                        expand=3,  # Proporção 3/8 (35%)
                        content=boxeol,
                    ),
                ],
            ),
            ft.Row(
                expand=True,  # Ocupa toda a largura disponível
                controls=[
                    ft.Container(
                        expand=5,  # Proporção 5/8 (55%)
                        content=form_container,
                    ),
                    
                ],


            )
        ],
    )