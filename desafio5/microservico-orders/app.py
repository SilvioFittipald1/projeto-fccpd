from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import random

app = Flask(__name__)

PEDIDOS = [
    {
        "id": 1,
        "usuario_id": 1,
        "produto": "Notebook",
        "valor": 3500.00,
        "status": "entregue",
        "data": (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
    },
    {
        "id": 2,
        "usuario_id": 1,
        "produto": "Mouse",
        "valor": 89.90,
        "status": "entregue",
        "data": (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    },
    {
        "id": 3,
        "usuario_id": 2,
        "produto": "Teclado",
        "valor": 250.00,
        "status": "em_transito",
        "data": (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
    },
    {
        "id": 4,
        "usuario_id": 2,
        "produto": "Monitor",
        "valor": 1200.00,
        "status": "processando",
        "data": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    },
    {
        "id": 5,
        "usuario_id": 3,
        "produto": "Webcam",
        "valor": 350.00,
        "status": "entregue",
        "data": (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    },
    {
        "id": 6,
        "usuario_id": 4,
        "produto": "Headset",
        "valor": 450.00,
        "status": "em_transito",
        "data": datetime.now().strftime('%Y-%m-%d')
    },
    {
        "id": 7,
        "usuario_id": 5,
        "produto": "SSD 1TB",
        "valor": 600.00,
        "status": "processando",
        "data": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    }
]

@app.route('/')
def index():
    return jsonify({
        "servico": "Microsserviço de Pedidos",
        "versao": "1.0.0",
        "endpoints": {
            "/pedidos": "Lista todos os pedidos",
            "/pedidos/<id>": "Retorna um pedido específico",
            "/pedidos/usuario/<usuario_id>": "Retorna pedidos de um usuário",
            "/health": "Health check"
        }
    })

@app.route('/pedidos', methods=['GET'])
def listar_pedidos():
    usuario_id = None
    if 'usuario_id' in request.args:
        try:
            usuario_id = int(request.args.get('usuario_id'))
        except:
            pass
    
    if usuario_id:
        pedidos_filtrados = [p for p in PEDIDOS if p["usuario_id"] == usuario_id]
        return jsonify({
            "total": len(pedidos_filtrados),
            "usuario_id": usuario_id,
            "pedidos": pedidos_filtrados
        })
    
    return jsonify({
        "total": len(PEDIDOS),
        "pedidos": PEDIDOS
    })

@app.route('/pedidos/<int:pedido_id>', methods=['GET'])
def obter_pedido(pedido_id):
    pedido = next((p for p in PEDIDOS if p["id"] == pedido_id), None)
    
    if pedido:
        return jsonify(pedido)
    else:
        return jsonify({"erro": "Pedido não encontrado"}), 404

@app.route('/pedidos/usuario/<int:usuario_id>', methods=['GET'])
def obter_pedidos_usuario(usuario_id):
    pedidos_usuario = [p for p in PEDIDOS if p["usuario_id"] == usuario_id]
    
    return jsonify({
        "usuario_id": usuario_id,
        "total": len(pedidos_usuario),
        "pedidos": pedidos_usuario
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "servico": "microservico-orders",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

