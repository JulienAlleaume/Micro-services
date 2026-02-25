from infrastructure.db.schema import Base
from infrastructure.db.units_of_work import engine
from infrastructure.messaging.rep_gateway import start_rpc_server

# Creation des tables au demarrage
Base.metadata.create_all(bind=engine)

print("Customer Service starting...")

# Le serveur RPC tourne dans le thread principal (blocking)
start_rpc_server()
