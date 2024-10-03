from app import db

class Usuarios(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_usuario = db.Column(db.String(50), nullable=False)
    email_usuario = db.Column(db.String(155), nullable=False)
    senha_usuario = db.Column(db.String(20), nullable=False)

    def __repr__(self) -> str:
        return '<Usuário %r>' % self.nome_usuario



class Equipamentos(db.Model):  
    id_equipamento = db.Column(db.Integer, primary_key=True)
    nome_equipamento = db.Column(db.String(80), nullable=False)
    tipo_recurso = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(200))
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    placa = db.Column(db.String(10), nullable=False)


