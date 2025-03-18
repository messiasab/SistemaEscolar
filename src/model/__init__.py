# model/__init__.py
from .mongodb_importer import import_data_to_mongodb
from .collections import Alunos, Notas, Contatos, Atestados, Ocorrencias

__all__ = ["import_data_to_mongodb", "Alunos", "Notas", "Contatos", "Atestados", "Ocorrencias"]