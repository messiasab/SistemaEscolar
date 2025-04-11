# model/__init__.py

from .mongodb_importer import import_data_to_mongodb
from .colecao import AlunosM, NotasM, ContatosM, AtestadosM, OcorrenciasM, RegistrosM,UsuariosM
from .relat import RelatOcorrencia, RelatMatricula, RelatFrequencia
__all__ = ["import_data_to_mongodb", "AlunosM", "NotasM", "ContatosM", "AtestadosM", "OcorrenciasM", "RegistrosM","UsuariosM", "RelatOcorrencia"]