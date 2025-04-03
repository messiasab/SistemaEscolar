from pymongo import MongoClient
from pymongo.collection import Collection
from typing import List, Dict, Optional
import certifi

# Conexão com o MongoDB
client = MongoClient("mongodb+srv://dadosaranhabandeirademello:nKXae2x6u8uwK_6@cluster0.apg3x.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
                     tlsCAFile=certifi.where(),
                     tlsAllowInvalidCertificates=True 
                     )
try:
    db = client["escola"]
    print(db.list_collection_names())  # Lista as coleções no banco de dados
except Exception as e:
    print(f"Erro ao conectar: {e}")


class BaseCollection:
    """
    Classe base para representar uma coleção no MongoDB.
    """
    def __init__(self, collection_name: str):
        # Inicializa a coleção como um atributo de instância
        self.collection: Collection = db[collection_name]

    def cria(self, data: Dict) -> str:
        """
        Insere um novo documento na coleção.
        """
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def ler(self, query: Dict = {},projection: dict = None) -> List[Dict]:
        """
        Retorna todos os documentos que correspondem à consulta.
        """
        if projection:
            return list(self.collection.find(query, projection))
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


class AlunosM(BaseCollection):
    def __init__(self):
        super().__init__("alunos")


class NotasM(BaseCollection):
    def __init__(self):
        super().__init__("Notas")


class ContatosM(BaseCollection):
    def __init__(self):
        super().__init__("Contatos")


class AtestadosM(BaseCollection):
    def __init__(self):
        super().__init__("Atestados")


class OcorrenciasM(BaseCollection):
    def __init__(self):
        super().__init__("Ocorrencias")

    def create_with_aluno_id(self, aluno_id: str, data: Dict) -> str:
        """
        Insere uma nova ocorrência associada a um aluno específico.
        """
        data['aluno_id'] = aluno_id
        return self.cria(data)


class RegistrosM(BaseCollection):
    def __init__(self):
        super().__init__("Registros")


