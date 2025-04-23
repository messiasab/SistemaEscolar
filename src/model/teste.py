""" from colecao import *
import pprint
tt=OcorrenciasM()

#print(aluu)

aluu=tt.ler()
pprint.pprint(aluu)            
            
 """

from dotenv import dotenv_values

# Carrega variáveis de ambiente
ENV_FILE = ".env"
env_vars = dotenv_values(ENV_FILE)

LINK_MONGO = env_vars.get("LINK_MONGO", "").strip()
DB_LOCAL = env_vars.get("DB_LOCAL", "False").lower() == "true"

print(f"LINK_MONGO: {LINK_MONGO}")
print(f"DB_LOCAL: {DB_LOCAL}")