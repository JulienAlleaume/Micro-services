import threading

from infrastructure.db.schema import Base
from infrastructure.db.units_of_work import engine
from infrastructure.messaging.rep_gateway import start_rpc_server
from infrastructure.messaging.sub_product_created import start_subscriber

# Création des tables au démarrage
Base.metadata.create_all(bind=engine)

print("Pricing Service starting...")

# Le subscriber tourne dans un thread séparé (écoute product.created)
subscriber_thread = threading.Thread(target=start_subscriber, daemon=True)
subscriber_thread.start()

# Le serveur RPC tourne dans le thread principal (blocking)
start_rpc_server()
