from flask import Flask, render_template, request, redirect

from models import db, Tarefa


app = Flask(__name__)


# Configuração do banco
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Inicializa banco
db.init_app(app)



# Página inicial
@app.route("/")
def index():

    tarefas = Tarefa.query.all()

    return render_template(
        "index.html",
        tarefas=tarefas
    )



# Adicionar tarefa
@app.route("/adicionar", methods=["POST"])
def adicionar():

    titulo = request.form["titulo"]

    descricao = request.form["descricao"]


    nova_tarefa = Tarefa(
        titulo=titulo,
        descricao=descricao
    )


    db.session.add(nova_tarefa)

    db.session.commit()


    return redirect("/")



# Excluir tarefa
@app.route("/excluir/<int:id>")
def excluir(id):

    tarefa = Tarefa.query.get(id)

    db.session.delete(tarefa)

    db.session.commit()


    return redirect("/")



# Marcar como concluída
@app.route("/concluir/<int:id>")
def concluir(id):

    tarefa = Tarefa.query.get(id)

    tarefa.concluida = True

    db.session.commit()


    return redirect("/")



# Criar banco
with app.app_context():

    db.create_all()



if __name__ == "__main__":

    app.run(debug=True)