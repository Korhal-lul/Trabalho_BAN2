from config.database import db
from models.endereco_model import Endereco
from models.cliente_model import Cliente, PF, PJ, ClienteContratado, VDetalhesCliente
from models.pedido_model import Pedido

__all__ = ['db', 'Endereco', 'Cliente', 'PF', 'PJ', 'ClienteContratado', 'VDetalhesCliente', 'Pedido']