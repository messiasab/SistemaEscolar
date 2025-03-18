# model/collections.py
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import List, Dict, Optional

# Conexão com o MongoDB
client = MongoClient("mongodb+srv://dadosaranhabandeirademello:GHO2q5ZYdd1oeKSW@cluster0.apg3x.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["escola"]

class BaseCollection:
    """
    Classe base para representar uma coleção no MongoDB.
    """
    def __init__(self, collection_name: str):
        self.collection: Collection = db[collection_name]

    def cria(self, data: Dict) -> str:
        """
        Insere um novo documento na coleção.
        """
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def ler(self, query: Dict = {}) -> List[Dict]:
        """
        Retorna todos os documentos que correspondem à consulta.
        """
        return list(self.collection.find(query))

    def atualiza(self, query: Dict, update_data: Dict) -> int:
        """
        Atualiza documentos que correspondem à consulta.
        """
        result = self.collection.update_many(query, {"$set": update_data})
        return result.modified_count

    def apaga(self, query: Dict) -> int:
        """
        Remove documentos que correspondem à consulta.
        """
        result = self.collection.delete_many(query)
        return result.deleted_count


class Alunos(BaseCollection):
    def __init__(self):
        super().__init__("Alunos")


class Notas(BaseCollection):
    def __init__(self):
        super().__init__("Notas")


class Contatos(BaseCollection):
    def __init__(self):
        super().__init__("Contatos")


class Atestados(BaseCollection):
    def __init__(self):
        super().__init__("Atestados")


class Ocorrencias(BaseCollection):
    def __init__(self):
        super().__init__("Ocorrencias")