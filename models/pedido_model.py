from config.database import db

class Pedido(db.Model):
    __tablename__ = 'pedido'
    
    id_pedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'))
    descricao_carga = db.Column(db.String(200))
    valor_declarado = db.Column(db.Numeric(10, 2))
    prazo_entrega = db.Column(db.Date)
    status = db.Column(db.String(50)) # No Postgres mapeia o ENUM nativo como String
    
    # Se quiser, pode mapear os outros campos do seu SQL aqui depois...