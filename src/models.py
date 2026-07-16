from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(
        db.String(100),
        nullable=False
    )

    descricao = db.Column(
        db.Text,
        nullable=True
    )

    concluida = db.Column(
        db.Boolean,
        default=False
    )


    def __repr__(self):
        return f"<Tarefa {self.titulo}>"