from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = Flask(__name__)


app.config["SECRET_KEY"] = "sistema_tarefas_secret"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tarefas.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)



login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"




# =====================
# MODELOS
# =====================


class Usuario(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100))

    email = db.Column(db.String(100), unique=True)

    senha = db.Column(db.String(200))



class Tarefa(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(db.String(100))

    descricao = db.Column(db.String(300))

    concluida = db.Column(db.Boolean, default=False)

    usuario_id = db.Column(db.Integer)



@login_manager.user_loader
def carregar_usuario(id):

    return db.session.get(Usuario, int(id))





# =====================
# LOGIN
# =====================


@app.route("/login", methods=["GET","POST"])
def login():


    if request.method=="POST":


        email=request.form["email"]

        senha=request.form["senha"]


        usuario=Usuario.query.filter_by(email=email).first()



        if usuario and check_password_hash(usuario.senha, senha):

            login_user(usuario)

            return redirect(url_for("dashboard"))



        flash("Login inválido")


    return render_template("login.html")





@app.route("/cadastro", methods=["GET","POST"])
def cadastro():


    if request.method=="POST":


        nome=request.form["nome"]

        email=request.form["email"]

        senha=request.form["senha"]



        usuario=Usuario(

            nome=nome,

            email=email,

            senha=generate_password_hash(senha)

        )


        db.session.add(usuario)

        db.session.commit()



        return redirect("/login")



    return render_template("cadastro.html")







@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/login")





# =====================
# DASHBOARD
# =====================


@app.route("/")
@login_required
def dashboard():


    tarefas=Tarefa.query.filter_by(usuario_id=current_user.id).all()


    total=len(tarefas)


    concluidas=len(
        [t for t in tarefas if t.concluida]
    )


    pendentes=total-concluidas



    return render_template(

        "dashboard.html",

        tarefas=tarefas,

        total=total,

        concluidas=concluidas,

        pendentes=pendentes

    )





# =====================
# TAREFAS
# =====================


@app.route("/adicionar",methods=["POST"])
@login_required
def adicionar():


    tarefa=Tarefa(

        titulo=request.form["titulo"],

        descricao=request.form["descricao"],

        usuario_id=current_user.id

    )


    db.session.add(tarefa)

    db.session.commit()



    return redirect("/")





@app.route("/concluir/<int:id>")
@login_required
def concluir(id):


    tarefa=db.session.get(Tarefa,id)


    tarefa.concluida=True


    db.session.commit()


    return redirect("/")





@app.route("/excluir/<int:id>")
@login_required
def excluir(id):


    tarefa=db.session.get(Tarefa,id)


    db.session.delete(tarefa)


    db.session.commit()


    return redirect("/")






@app.route("/sobre")
def sobre():

    return render_template("sobre.html")







if __name__=="__main__":


    with app.app_context():

        db.create_all()


    print("Sistema de Gerenciamento de Tarefas")


    app.run(debug=True)