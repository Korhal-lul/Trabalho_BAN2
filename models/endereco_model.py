from config.database import db

class EnderecoModel(db.Model):
    __tablename__ = 'endereco'
    
    id_endereco = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rua = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(100))
    numero = db.Column(db.Integer)