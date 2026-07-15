from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()



class Usuario(db.Model, UserMixin):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(100)
    )


    email = db.Column(
        db.String(100),
        unique=True
    )


    senha = db.Column(
        db.String(200)
    )





class Tarefa(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    titulo = db.Column(
        db.String(100)
    )


    descricao = db.Column(
        db.String(300)
    )


    concluida = db.Column(
        db.Boolean,
        default=False
    )


    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuario.id')
    )