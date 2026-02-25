from infrastructure.db.schema import Base
from infrastructure.db.units_of_work import engine
from infrastructure.messaging.rep_gateway import start_rpc_server

# Creation des tables au demarrage
Base.metadata.create_all(bind=engine)

print("Order Service starting...")

# Le serveur RPC tourne dans le thread principal (blocking)
# Le publisher PUB est initialise lazily a la premiere creation de commande
start_rpc_server()
