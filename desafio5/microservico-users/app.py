from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

USUARIOS = [
    {
        "id": 1,
        "nome": "Renato Moicano",
        "email": "renato@email.com",
        "telefone": "(11) 98765-4321",
        "cidade": "São Paulo"
    },
    {
        "id": 2,
        "nome": "Edson Barboza",
        "email": "edson@email.com",
        "telefone": "(21) 97654-3210",
        "cidade": "Rio de Janeiro"
    },
    {
        "id": 3,
        "nome": "Diego Lopes",
        "email": "diego@email.com",
        "telefone": "(31) 96543-2109",
        "cidade": "Belo Horizonte"
    },
    {
        "id": 4,
        "nome": "Alexandre Pantoja",
        "email": "alexandre@email.com",
        "telefone": "(41) 95432-1098",
        "cidade": "Curitiba"
    },
    {
        "id": 5,
        "nome": "Valter Walker",
        "email": "valter@email.com",
        "telefone": "(51) 94321-0987",
        "cidade": "Porto Alegre"
    }
]

@app.route('/')
def index():
    return jsonify({
        "servico": "Microsserviço de Usuários",
        "versao": "1.0.0",
        "endpoints": {
            "/usuarios": "Lista todos os usuários",
            "/usuarios/<id>": "Retorna um usuário específico",
            "/health": "Health check"
        }
    })

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    return jsonify({
        "total": len(USUARIOS),
        "usuarios": USUARIOS
    })

@app.route('/usuarios/<int:usuario_id>', methods=['GET'])
def obter_usuario(usuario_id):
    usuario = next((u for u in USUARIOS if u["id"] == usuario_id), None)
    
    if usuario:
        return jsonify(usuario)
    else:
        return jsonify({"erro": "Usuário não encontrado"}), 404

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "servico": "microservico-users",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

