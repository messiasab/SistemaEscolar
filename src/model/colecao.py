from abc import ABC, abstractmethod
from pymongo import MongoClient
from pymongo.collection import Collection
from tinydb import TinyDB, Query
from typing import List, Dict, Optional
import certifi
from dotenv import dotenv_values

# Carrega variáveis de ambiente
ENV_FILE = ".env"
env_vars = dotenv_values(ENV_FILE)

# Verifica as variáveis de ambiente
LINK_MONGO = env_vars.get("LINK_MONGO", "link não encontrado").strip()
DB_LOCAL = env_vars.get("DB_LOCAL", "False").lower()

# Classe base abstrata
class BaseCollection(ABC):
    """
    Classe base abstrata para representar uma coleção no banco de dados.
    """
    @abstractmethod
    def cria(self, data: Dict) -> str:
        pass

    @abstractmethod
    def ler(self, query: Dict = {}, projection: Optional[Dict] = None) -> List[Dict]:
        pass

    @abstractmethod
    def atualiza(self, query: Dict, update_data: Dict) -> int:
        pass

    @abstractmethod
    def apaga(self, query: Dict) -> int:
        pass


# Implementação para MongoDB
class MongoCollection(BaseCollection):
    def __init__(self, collection_name: str):
        LINK_MONGO = env_vars.get("LINK_MONGO", "link não encontrado")
        print(f"Conectando ao MongoDB em {LINK_MONGO}...")
        client = MongoClient(
            LINK_MONGO,
            tlsCAFile=certifi.where(),
            tlsAllowInvalidCertificates=True
        )
        self.collection: Collection = client["escola"][collection_name]

    def cria(self, data: Dict) -> str:
        """
        Insere um documento na coleção e retorna o ID do documento inserido.
        """
        result = self.collection.insert_one(data)
        return str(result.inserted_id)  # Retorna o ID como string

    def ler(self, query: Dict = {}, projection: Optional[Dict] = None) -> List[Dict]:
        if projection:
            return list(self.collection.find(query, projection))
        return list(self.collection.find(query))

    def atualiza(self, query: Dict, update_data: Dict) -> int:
        result = self.collection.update_many(query, {"$set": update_data})
        return result.modified_count

    def apaga(self, query: Dict) -> int:
        result = self.collection.delete_many(query)
        return result.deleted_count


# Implementação para TinyDB
class TinyDBCollection(BaseCollection):
    def __init__(self, collection_name: str):
        self.db = TinyDB(f"{collection_name}.json")
        self.query = Query()

    def cria(self, data: Dict) -> str:
        inserted_id = self.db.insert_one(data)
        return str(inserted_id)

    def ler(self, query: Dict = {}, projection: Optional[Dict] = None) -> List[Dict]:
        # Filtra os documentos com base na query
        if query:
            q = self._build_query(query)
            return self.db.search(q)
        return self.db.all()

    def atualiza(self, query: Dict, update_data: Dict) -> int:
        q = self._build_query(query)
        updated_ids = self.db.update(update_data, q)
        return len(updated_ids)

    def apaga(self, query: Dict) -> int:
        q = self._build_query(query)
        deleted_ids = self.db.remove(q)
        return len(deleted_ids)

    def _build_query(self, query_dict: Dict):
        """
        Constrói uma query do TinyDB a partir de um dicionário.
        """
        q = self.query
        for key, value in query_dict.items():
            q = getattr(q, key) == value
        return q


# Função para selecionar o banco de dados
def get_base_collection(collection_name: str) -> BaseCollection:
    if DB_LOCAL and not LINK_MONGO:
        print(f"Usando TinyDB (local) para '{collection_name}'.")
        return TinyDBCollection(collection_name)
    else:
        print(f"Usando MongoDB para '{collection_name}'.")
        return MongoCollection(collection_name)


# Classes Específicas
class AlunosM:
    def __init__(self):
        self.campos = [
            '_id', 'EOL', 'RA_Prodesp', 'Codigo_INEP', 'Nº', 'Nome', 'Filiação',
            'Data_Nascimento', 'Data_Matrícula', 'Situação', 'Origem', 'Série',
            'TEG', 'Turma', 'Periodo', 'Ensino'
        ]
        self.collection = get_base_collection("Alunos")

    def cria(self, aluno_id, aluno_data):
        aluno_data["aluno_id"] = aluno_id
        return self.collection.cria(aluno_data)  # Retorna diretamente o ID do documento inserido

    def ler(self, query: Dict = {}, projection: Optional[Dict] = None) -> List[Dict]:
        return self.collection.ler(query, projection)

    def atualiza(self, query: Dict, update_data: Dict) -> int:
        return self.collection.atualiza(query, update_data)

    def apaga(self, query: Dict) -> int:
        return self.collection.apaga(query)

    def inicializar_campos(self):
        return self.campos


class NotasM:
    def __init__(self):
        self.campos = ['_id', 'aluno_id', 'disciplina', 'nota', 'data']
        self.collection = get_base_collection("Notas")

    def cria(self, aluno_id, nota_data):
        nota_data["aluno_id"] = aluno_id
        return self.collection.cria(nota_data)  # Retorna diretamente o ID do documento inserido

    def ler(self, query: Dict = {}, projection: Optional[Dict] = None) -> List[Dict]:
        return self.collection.ler(query, projection)

    def atualiza(self, query: Dict, update_data: Dict) -> int:
        return self.collection.atualiza(query, update_data)

    def apaga(self, query: Dict) -> int:
        return self.collection.apaga(query)

    def inicializar_campos(self):
        return self.campos


class ContatosM:
    def __init__(self):
        self.campos = ['_id', 'nome', 'telefone', 'telefone_whatsapp', 'mail', 'link_redes', 'aluno_id']
        self.collection = get_base_collection("Contatos")

    def cria(self, aluno_id, contato_data):
        contato_data["aluno_id"] = aluno_id
        return self.collection.cria(contato_data)  # Retorna diretamente o ID do documento inserido

    def ler(self, query: Dict = {}, projection: Optional[Dict] = None) -> List[Dict]:
        return self.collection.ler(query, projection)

    def atualiza(self, query: Dict, update_data: Dict) -> int:
        return self.collection.atualiza(query, update_data)

    def apaga(self, query: Dict) -> int:
        return self.collection.apaga(query)

    def inicializar_campos(self):
        return self.campos


class AtestadosM:
    def __init__(self):
        self.campos = ['_id', 'tipo', 'data', 'numero_dias', 'conteudo', 'cid', 'observacao', 'aluno_id']
        self.collection = get_base_collection("Atestados")

    def cria(self, aluno_id, atestado_data):
        atestado_data["aluno_id"] = aluno_id
        return self.collection.cria(atestado_data)  # Retorna diretamente o ID do documento inserido

    def ler(self, query: Dict = {}, projection: Optional[Dict] = None) -> List[Dict]:
        return self.collection.ler(query, projection)

    def atualiza(self, query: Dict, update_data: Dict) -> int:
        return self.collection.atualiza(query, update_data)

    def apaga(self, query: Dict) -> int:
        return self.collection.apaga(query)

    def inicializar_campos(self):
        return self.campos


class RegistrosM:
    def __init__(self):
        self.campos = ['_id', 'tipo', 'nome_responsavel', 'data', 'acao_realizada', 'observacao', 'aluno_id']
        self.collection = get_base_collection("Registros")

    def cria(self, aluno_id, registro_data):
        registro_data["aluno_id"] = aluno_id
        return self.collection.cria(registro_data)  # Retorna diretamente o ID do documento inserido

    def ler(self, query: Dict = {}, projection: Optional[Dict] = None) -> List[Dict]:
        return self.collection.ler(query, projection)

    def atualiza(self, query: Dict, update_data: Dict) -> int:
        return self.collection.atualiza(query, update_data)

    def apaga(self, query: Dict) -> int:
        return self.collection.apaga(query)

    def inicializar_campos(self):
        return self.campos


class UsuariosM:
    def __init__(self):
        self.campos = ['_id', 'nome', 'rf', 'email', 'senha', 'tipo']
        self.collection = get_base_collection("Usuarios")

    def cria(self, usuario_id, usuario_data):
        usuario_data["usuario_id"] = usuario_id
        return self.collection.cria(usuario_data)  # Retorna diretamente o ID do documento inserido

    def ler(self, query: Dict = {}, projection: Optional[Dict] = None) -> List[Dict]:
        return self.collection.ler(query, projection)

    def atualiza(self, query: Dict, update_data: Dict) -> int:
        return self.collection.atualiza(query, update_data)

    def apaga(self, query: Dict) -> int:
        return self.collection.apaga(query)

    def inicializar_campos(self):
        return self.campos


class OcorrenciasM:
    def __init__(self):
        self.campos = [
            '_id', 'nome_responsavel', 'telefone', 'responsavel_registro',
            'rf_registro', 'data', 'relato', 'estrategia', 'encaminhamento', 'aluno_id'
        ]
        self.collection = get_base_collection("Ocorrencias")

    def cria(self, aluno_id, ocorrencia_data):
        ocorrencia_data["aluno_id"] = aluno_id
        return self.collection.cria(ocorrencia_data)  # Retorna diretamente o ID do documento inserido

    def ler(self, query: Dict = {}, projection: Optional[Dict] = None) -> List[Dict]:
        return self.collection.ler(query, projection)

    def atualiza(self, query: Dict, update_data: Dict) -> int:
        return self.collection.atualiza(query, update_data)

    def apaga(self, query: Dict) -> int:
        return self.collection.apaga(query)

    def inicializar_campos(self):
        return self.campos
