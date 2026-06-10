from config.database import db

class Cliente(db.Model):
    __tablename__ = 'cliente'
    
    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(50))
    tipo_cliente = db.Column(db.String(20), nullable=False)
    id_endereco = db.Column(db.Integer, db.ForeignKey('endereco.id_endereco'))
    
    __mapper_args__ = {
        'polymorphic_on': tipo_cliente,
        'polymorphic_identity': 'cliente'
    }

class PF(Cliente):
    __tablename__ = 'pf'
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'), primary_key=True)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    nome = db.Column(db.String(100))
    
    __mapper_args__ = {
        'polymorphic_identity': 'PF'
    }

class PJ(Cliente):
    __tablename__ = 'pj'
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'), primary_key=True)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    razao_social = db.Column(db.String(100))
    inscricao_estadual = db.Column(db.String(20))
    
    __mapper_args__ = {
        'polymorphic_identity': 'PJ'
    }

class ClienteContratado(Cliente):
    __tablename__ = 'cliente_contratado'
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'), primary_key=True)
    limite_credito = db.Column(db.Numeric(10, 2))
    id_tabela_precos = db.Column(db.Integer)
    
    __mapper_args__ = {
        'polymorphic_identity': 'Contrato'
    }

class VDetalhesCliente(db.Model):
    __tablename__ = 'v_detalhes_clientes'
    
    id_cliente = db.Column(db.Integer, primary_key=True)
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(50))
    tipo_cliente = db.Column(db.String(20))
    
    pf_nome = db.Column(db.String(100))
    pf_cpf = db.Column(db.String(11))
    
    pj_razao_social = db.Column(db.String(100))
    pj_cnpj = db.Column(db.String(14))
    pj_inscricao_estadual = db.Column(db.String(20))
    
    contrato_limite_credito = db.Column(db.Numeric(10, 2))
    contrato_id_tabela_precos = db.Column(db.Integer)
    
    id_endereco = db.Column(db.Integer)
    rua = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(100))
    numero = db.Column(db.Integer)

    tabela_descricao = db.Column(db.String(200))
    tabela_regras = db.Column(db.Text)