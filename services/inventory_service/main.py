import threading

from infrastructure.db.schema import Base
from infrastructure.db.units_of_work import engine
from infrastructure.messaging.rep_gateway import start_rpc_server
from infrastructure.messaging.sub_product_created import start_subscriber as start_product_sub
from infrastructure.messaging.sub_orderline_created import start_subscriber as start_orderline_sub

# Creation des tables au demarrage
Base.metadata.create_all(bind=engine)

print("Inventory Service starting...")

# Subscriber product.created dans un thread dedie
product_thread = threading.Thread(target=start_product_sub, daemon=True)
product_thread.start()

# Subscriber orderline.created dans un thread dedie
orderline_thread = threading.Thread(target=start_orderline_sub, daemon=True)
orderline_thread.start()

# Le serveur RPC tourne dans le thread principal (blocking)
start_rpc_server()
