from models.cliente_model import ClienteModel

class ClienteService:

    @staticmethod
    def listar():
        return ClienteModel.listar()

    @staticmethod
    def cadastrar(form):

        telefone = form['telefone']
        email = form['email']
        tipo_cliente = form['tipo_cliente']
        id_endereco = form['id_endereco']

        ClienteModel.inserir(
            telefone,
            email,
            tipo_cliente,
            id_endereco
        )