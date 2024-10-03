from flask import render_template, request, redirect, session, url_for 
from models import Usuarios, Equipamentos
from app import app, db
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_logado' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(
        email_usuario=request.form['login']
    ).first()

    if usuario and request.form['senha'] == usuario.senha_usuario:
        session['usuario_logado'] = usuario.nome_usuario
        return redirect('/dashboard')
    return redirect('/login')

@app.route('/dashboard')
@login_required
def dashboard():
    num_equipamentos = Equipamentos.query.count()
    num_veiculos = Equipamentos.query.filter_by(tipo_recurso='Veículo').count()
    num_dispositivos = Equipamentos.query.filter_by(tipo_recurso='Dispositivo de Segurança').count()

    return render_template('dashboard.html', 
                           num_equipamentos=num_equipamentos, 
                           num_veiculos=num_veiculos, 
                           num_dispositivos=num_dispositivos)




@app.route('/cadastrar')
@login_required
def cadastrar():
    return render_template('cadastrar_equipamento.html')

@app.route('/adicionar', methods=['POST',])
@login_required
def adicionar_equipamento():
    nome = request.form['nome']
    tipo_recurso = request.form['tipo_recurso']
    descricao = request.form['descricao']

  
    print("Usuário logado:", session.get('usuario_logado'))  
    print("Nome do equipamento:", nome)

    
    equipamento_existente = Equipamentos.query.filter_by(nome_equipamento=nome).first()
    if equipamento_existente:
        print("Equipamento já existe. Redirecionando...")
        return redirect(url_for('equipamentos')) 

    novo_equipamento = Equipamentos(nome_equipamento=nome, tipo_recurso=tipo_recurso, descricao=descricao)
    db.session.add(novo_equipamento)
    db.session.commit()

    print("Novo equipamento adicionado:", novo_equipamento.nome_equipamento)
    return redirect(url_for('equipamentos'))

@app.route('/cadastrar-usuario')
def cadastrar_usuario():
    return render_template('cadastrar_usuario.html')

@app.route('/adicionar-usuario', methods=['POST',])
def adicionar_usuario():
    nome_usuario = request.form['nomeUsuario']
    email_usuario = request.form['emailUsuario']
    senha_usuario = request.form['senhaUsuario']

    usuario = Usuarios.query.filter_by(nome_usuario=nome_usuario).first()

    if usuario:
        return redirect('/cadastrar-usuario')

    novo_usuario = Usuarios(nome_usuario=nome_usuario, email_usuario=email_usuario, senha_usuario=senha_usuario)
    db.session.add(novo_usuario)
    db.session.commit()

    return redirect('/login')

@app.route('/sair')
def sair():
    session.pop('usuario_logado', None)
    return redirect('/login')

#########################################################################################################################
@app.route('/add-equipamento', methods=['GET', 'POST'])
@login_required
def add_equipamento():
    if request.method == 'POST':
        nome = request.form['nome']
        tipo_recurso = request.form['tipo_recurso']
        descricao = request.form['descricao']

       
        equipamento_existente = Equipamentos.query.filter_by(nome_equipamento=nome).first()
        if equipamento_existente:
           
            print("Equipamento já existe ao adicionar.")
            return redirect(url_for('equipamentos'))

        
        novo_equipamento = Equipamentos(nome_equipamento=nome, tipo_recurso=tipo_recurso, descricao=descricao)
        db.session.add(novo_equipamento)
        db.session.commit()

        return redirect(url_for('equipamentos'))
    
    
    return render_template('adicionar_equipamento.html')

@app.route('/editar-equipamento/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_equipamento(id):
    
    equipamento = Equipamentos.query.get_or_404(id)
    if request.method == 'POST':
        equipamento.nome_equipamento = request.form['nome']
        equipamento.tipo_recurso = request.form['tipo_recurso']
        equipamento.descricao = request.form['descricao']
        db.session.commit()
        return redirect(url_for('equipamentos'))
    return render_template('editar_equipamento.html', equipamento=equipamento)




@app.route('/equipamentos', methods=['GET'])
@login_required
def listar_equipamentos():
    equipamentos = Equipamentos.query.all()
    return render_template('equipamentos.html', equipamentos=equipamentos)


@app.route('/deletar-equipamento/<int:id_equipamento>', methods=['POST'])
@login_required
def deletar_equipamento(id_equipamento):
    print(f"Tentando deletar equipamento com ID: {id_equipamento}") 
    equipamento = Equipamentos.query.get_or_404(id_equipamento)
    
    
    db.session.delete(equipamento)
    db.session.commit()
    
    print("Equipamento deletado com sucesso!")  
    
   
    return redirect(url_for('listar_equipamentos'))



@app.route('/equipamentos')
@login_required
def equipamentos():
    equipamentos = Equipamentos.query.all()
    print(equipamentos) 
    return render_template('equipamentos.html', equipamentos=equipamentos)

@app.route('/veiculos')
@login_required
def veiculos():
    veiculos = Equipamentos.query.filter_by(tipo_recurso='veiculo').all()
    return render_template('veiculos.html', veiculos=veiculos)




############################################################################################

@app.route('/veiculos/add', methods=['GET', 'POST'])
@login_required
def add_veiculo():
    if request.method == 'POST':
        nome = request.form['nome_equipamento']
        marca = request.form['marca']
        modelo = request.form['modelo']
        ano = request.form['ano']
        placa = request.form['placa']

        
        novo_veiculo = Equipamentos(
            nome_equipamento=nome,
            tipo_recurso='veiculo',
            marca=marca,
            modelo=modelo,
            ano=ano,
            placa=placa
        )
        db.session.add(novo_veiculo)
        db.session.commit()

        return redirect(url_for('veiculos'))

    return render_template('add_veiculo.html')




@app.route('/veiculos/editar/<int:id_equipamento>', methods=['GET', 'POST'])
@login_required
def editar_veiculo(id_equipamento):
    veiculo = Equipamentos.query.get_or_404(id_equipamento)

    if request.method == 'POST':
        veiculo.nome_equipamento = request.form['nome_equipamento']
        veiculo.marca = request.form['marca']
        veiculo.modelo = request.form['modelo']
        veiculo.ano = request.form['ano']
        veiculo.placa = request.form['placa']
        db.session.commit()
        return redirect(url_for('veiculos'))

    return render_template('editar_veiculo.html', veiculo=veiculo)



@app.route('/veiculos/deletar/<int:id_equipamento>', methods=['POST'])
@login_required
def deletar_veiculo(id_equipamento):
    veiculo = Equipamentos.query.get_or_404(id_equipamento)
    db.session.delete(veiculo)
    db.session.commit()
    return redirect(url_for('veiculos'))




####################################################################################################

@app.route('/dispositivos_seguranca', methods=['GET'])
@login_required
def dispositivos_seguranca():
    dispositivos = Equipamentos.query.filter_by(tipo_recurso='Dispositivo de Segurança').all()
    return render_template('dispositivos_seguranca.html', dispositivos=dispositivos)

@app.route('/dispositivos_seguranca/add', methods=['GET', 'POST'])
@login_required
def add_dispositivo():
    if request.method == 'POST':
        novo_dispositivo = Equipamentos(
            nome_equipamento=request.form['nome_equipamento'],
            tipo_recurso='Dispositivo de Segurança',
            descricao=request.form['descricao']
        )
        db.session.add(novo_dispositivo)
        db.session.commit()
        return redirect(url_for('dispositivos_seguranca'))

    return render_template('add_dispositivo.html')

@app.route('/dispositivos_seguranca/editar/<int:id_equipamento>', methods=['GET', 'POST'])
@login_required
def editar_dispositivo(id_equipamento):
    dispositivo = Equipamentos.query.get_or_404(id_equipamento)

    if request.method == 'POST':
        dispositivo.nome_equipamento = request.form['nome_equipamento']
        dispositivo.descricao = request.form['descricao']
        db.session.commit()
        return redirect(url_for('dispositivos_seguranca'))

    return render_template('editar_dispositivo.html', dispositivo=dispositivo)

@app.route('/dispositivos_seguranca/deletar/<int:id_equipamento>', methods=['POST'])
@login_required
def deletar_dispositivo(id_equipamento):
    dispositivo = Equipamentos.query.get_or_404(id_equipamento)
    db.session.delete(dispositivo)
    db.session.commit()
    return redirect(url_for('dispositivos_seguranca'))
