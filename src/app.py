print("Sistema de Gerenciamento de Tarefas")
from flask import Flask, jsonify, request

app = Flask(__name__)

tarefas = []


@app.route("/")
def inicio():
    return "Sistema de Gerenciamento de Tarefas"


@app.route("/tarefas", methods=["GET"])
def listar_tarefas():
    return jsonify(tarefas)


@app.route("/tarefas", methods=["POST"])
def criar_tarefa():

    dados = request.json

    tarefa = {
        "id": len(tarefas) + 1,
        "titulo": dados["titulo"],
        "status": "Pendente"
    }

    tarefas.append(tarefa)

    return jsonify(tarefa)


if __name__ == "__main__":
   app.run(debug=True)