from flask import Flask, render_template, request, abort, redirect, url_for
from config.database import db, Config
from models import Cliente, PF, PJ, ClienteContratado, Pedido, VDetalhesCliente, Endereco
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
# ========================================================== Cliente =======================================================
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

@app.route('/cad_cliente')
def tela_cadastro_cliente():
    avatar_usuario = "https://github.com/identicons/marvin.png"
    return render_template('cad_cliente.html', user_avatar=avatar_usuario, aba_ativa='clientes')

@app.route('/salvar_cliente', methods=['POST'])
def salvar_cliente():
    tipo_cliente = request.form.get('tipo_cliente')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    
    rua = request.form.get('rua')
    numero = request.form.get('numero')
    cidade = request.form.get('cidade')
    estado = request.form.get('estado')

    try:
        novo_endereco = Endereco(rua=rua, numero=numero, cidade=cidade, estado=estado)
        db.session.add(novo_endereco)
        db.session.flush() 
        if tipo_cliente == 'PF':
            novo_cliente = PF(
                email=email,
                telefone=telefone,
                id_endereco=novo_endereco.id_endereco,
                nome=request.form.get('nome'),
                cpf=request.form.get('cpf')
            )
        elif tipo_cliente == 'PJ':
            novo_cliente = PJ(
                email=email,
                telefone=telefone,
                id_endereco=novo_endereco.id_endereco,
                razao_social=request.form.get('razao_social'),
                cnpj=request.form.get('cnpj'),
                inscricao_estadual=request.form.get('inscricao_estadual')
            )
        elif tipo_cliente == 'Contrato':
            id_tabela = request.form.get('id_tabela_precos')
            novo_cliente = ClienteContratado(
                email=email,
                telefone=telefone,
                id_endereco=novo_endereco.id_endereco,
                limite_credito=request.form.get('limite_credito'),
                id_tabela_precos=int(id_tabela) if id_tabela else None
            )

        db.session.add(novo_cliente)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback() 
        print(f"Erro ao salvar: {e}")
        return f"Erro ao salvar o cliente: {e}", 400

    return redirect(url_for('index'))

@app.route('/cliente/<string:id_criptografado>/editar')
def tela_editar_cliente(id_criptografado):
    try:
        id_real = serializador.loads(id_criptografado)
    except:
        abort(404)
        
    cliente_completo = VDetalhesCliente.query.get_or_404(id_real)
    avatar_usuario = "https://github.com/identicons/marvin.png"
    return render_template('editar_cliente.html', cliente=cliente_completo, user_avatar=avatar_usuario, aba_ativa='clientes')

@app.route('/cliente/<string:id_criptografado>/salvar', methods=['POST'])
def atualizar_cliente(id_criptografado):
    try:
        id_real = serializador.loads(id_criptografado)
    except:
        abort(404)

    cliente_pai = Cliente.query.get_or_404(id_real)
    
    try:
        cliente_pai.email = request.form.get('email')
        cliente_pai.telefone = request.form.get('telefone')
        
        endereco = Endereco.query.get(cliente_pai.id_endereco)
        if endereco:
            endereco.rua = request.form.get('rua')
            endereco.numero = request.form.get('numero')
            endereco.cidade = request.form.get('cidade')
            endereco.estado = request.form.get('estado')

        if cliente_pai.tipo_cliente == 'PF':
            cliente_filho = PF.query.get(id_real)
            cliente_filho.nome = request.form.get('nome')
            cliente_filho.cpf = request.form.get('cpf')
        elif cliente_pai.tipo_cliente == 'PJ':
            cliente_filho = PJ.query.get(id_real)
            cliente_filho.razao_social = request.form.get('razao_social')
            cliente_filho.cnpj = request.form.get('cnpj')
            cliente_filho.inscricao_estadual = request.form.get('inscricao_estadual')
        elif cliente_pai.tipo_cliente == 'Contrato':
            cliente_filho = ClienteContratado.query.get(id_real)
            cliente_filho.limite_credito = request.form.get('limite_credito')

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return f"Erro ao atualizar dados no banco: {e}", 400

    return redirect(url_for('detalhes_cliente', id_criptografado=id_criptografado))

@app.route('/cliente/<string:id_criptografado>/deletar', methods=['POST'])
def deletar_cliente(id_criptografado):
    try:
        id_real = serializador.loads(id_criptografado)
    except:
        abort(404)

    cliente_pai = Cliente.query.get_or_404(id_real)
    id_endereco_vinculado = cliente_pai.id_endereco
    
    try:
        if cliente_pai.tipo_cliente == 'PF':
            PF.query.filter_by(id_cliente=id_real).delete()
        elif cliente_pai.tipo_cliente == 'PJ':
            PJ.query.filter_by(id_cliente=id_real).delete()
        elif cliente_pai.tipo_cliente == 'Contrato':
            ClienteContratado.query.filter_by(id_cliente=id_real).delete()

        Cliente.query.filter_by(id_cliente=id_real).delete()

        if id_endereco_vinculado:
            Endereco.query.filter_by(id_endereco=id_endereco_vinculado).delete()

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return f"Erro ao deletar: Este cliente pode possuir Pedidos ativos vinculados a ele. {e}", 400

    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)