# model/mongodb_importer.py
import pandas as pd
from pymongo.collection import Collection

def import_data_to_mongodb(file_path: str, collection: Collection):
    """
    Importa os dados de uma planilha Excel para uma coleção do MongoDB.
    """
    try:
        # Ler a planilha usando pandas
        df = pd.read_excel(file_path)
        
        # Converter o DataFrame para uma lista de dicionários (JSON-like)
        data = df.to_dict(orient="records")
        
        # Inserir os dados no MongoDB
        collection.insert_many(data)
        return True, f"{len(data)} registros importados com sucesso!"
    except Exception as e:
        return False, f"Erro ao importar dados: {str(e)}"