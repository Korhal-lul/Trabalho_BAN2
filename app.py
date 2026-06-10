from flask import Flask, render_template, request, abort
from config.database import db, Config
from models import Cliente, PF, PJ, ClienteContratado, Pedido, VDetalhesCliente
from itsdangerous import URLSafeSerializer

app = Flask(__name__)
app.config.from_object(Config)

serializador = URLSafeSerializer(app.config['SECRET_KEY'])

@app.template_filter('formatar_cpf')
def formatar_cpf(cpf):
    if not cpf or len(str(cpf)) != 11:
        return cpf
    cpf = str(cpf)
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

@app.template_filter('formatar_cnpj')
def formatar_cnpj(cnpj):
    if not cnpj or len(str(cnpj)) != 14:
        return cnpj
    cnpj = str(cnpj)
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

@app.template_filter('formatar_telefone')
def formatar_telefone(telefone):
    if not telefone or len(str(telefone)) != 11:
        return telefone
    telefone = str(telefone)
    return f"{telefone[:0]}({telefone[0:2]}) {telefone[2:7]}-{telefone[8:]}"

@app.context_processor
def utilitarios():
    return dict(ocultar_id=lambda id_real: serializador.dumps(id_real))

db.init_app(app)
# ========================================================== Comeco =======================================================
@app.route('/')
def index():
    tipo_filtro = request.args.get('tipo', 'TODOS').upper()
    
    if tipo_filtro == 'PF':
        lista_clientes = PF.query.all()
    elif tipo_filtro == 'PJ':
        lista_clientes = PJ.query.all()
    elif tipo_filtro == 'CONTRATO':
        lista_clientes = ClienteContratado.query.all()
    else:
        lista_clientes = Cliente.query.all()

    avatar_usuario = "https://github.com/identicons/marvin.png"
    return render_template('index.html', clientes=lista_clientes, 
                           filtro_atual=tipo_filtro, 
                           user_avatar=avatar_usuario,
                           aba_ativa='clientes')

@app.route('/cliente/<string:id_criptografado>')
def detalhes_cliente(id_criptografado):
    try:
        id_real = serializador.loads(id_criptografado)
    except:
        abort(404)
    
    cliente_completo = VDetalhesCliente.query.get_or_404(id_real)
    
    pedidos_cliente = Pedido.query.filter_by(id_cliente=id_real).order_by(Pedido.id_pedido.desc()).all()
    
    avatar_usuario = "https://github.com/identicons/marvin.png"
    
    return render_template(
        'detalhes_cliente.html', 
        cliente=cliente_completo, 
        pedidos=pedidos_cliente, 
        user_avatar=avatar_usuario
    )



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)