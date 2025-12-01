from flask import Flask, jsonify, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

MICROSERVICO_USERS_URL = os.getenv('MICROSERVICO_USERS_URL', 'http://microservico-users:5000')
MICROSERVICO_ORDERS_URL = os.getenv('MICROSERVICO_ORDERS_URL', 'http://microservico-orders:5001')

def fazer_requisicao(url, timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json(), response.status_code
    except requests.exceptions.Timeout:
        return {"erro": "Timeout ao conectar ao serviço"}, 504
    except requests.exceptions.ConnectionError:
        return {"erro": "Não foi possível conectar ao serviço"}, 503
    except requests.exceptions.RequestException as e:
        return {"erro": f"Erro na requisição: {str(e)}"}, 500

@app.route('/')
def index():
    return jsonify({
        "servico": "API Gateway",
        "versao": "1.0.0",
        "descricao": "Gateway centralizado para acesso aos microsserviços",
        "endpoints": {
            "/users": "Lista todos os usuários (proxy para Microsserviço de Usuários)",
            "/users/<id>": "Retorna um usuário específico",
            "/orders": "Lista todos os pedidos (proxy para Microsserviço de Pedidos)",
            "/orders/<id>": "Retorna um pedido específico",
            "/orders/user/<user_id>": "Retorna pedidos de um usuário",
            "/health": "Health check do gateway e serviços",
            "/status": "Status de todos os serviços"
        },
        "servicos": {
            "users": MICROSERVICO_USERS_URL,
            "orders": MICROSERVICO_ORDERS_URL
        }
    })

@app.route('/users', methods=['GET'])
def listar_usuarios():
    url = f"{MICROSERVICO_USERS_URL}/usuarios"
    dados, status_code = fazer_requisicao(url)
    
    if status_code == 200:
        dados["_gateway"] = {
            "processado_por": "API Gateway",
            "timestamp": datetime.now().isoformat(),
            "servico_origem": "microservico-users"
        }
    
    return jsonify(dados), status_code

@app.route('/users/<int:usuario_id>', methods=['GET'])
def obter_usuario(usuario_id):
    url = f"{MICROSERVICO_USERS_URL}/usuarios/{usuario_id}"
    dados, status_code = fazer_requisicao(url)
    
    if status_code == 200:
        dados["_gateway"] = {
            "processado_por": "API Gateway",
            "timestamp": datetime.now().isoformat(),
            "servico_origem": "microservico-users"
        }
    
    return jsonify(dados), status_code

@app.route('/orders', methods=['GET'])
def listar_pedidos():
    usuario_id = request.args.get('user_id')
    
    if usuario_id:
        url = f"{MICROSERVICO_ORDERS_URL}/pedidos/usuario/{usuario_id}"
    else:
        url = f"{MICROSERVICO_ORDERS_URL}/pedidos"
    
    dados, status_code = fazer_requisicao(url)
    
    if status_code == 200:
        dados["_gateway"] = {
            "processado_por": "API Gateway",
            "timestamp": datetime.now().isoformat(),
            "servico_origem": "microservico-orders"
        }
    
    return jsonify(dados), status_code

@app.route('/orders/<int:pedido_id>', methods=['GET'])
def obter_pedido(pedido_id):
    url = f"{MICROSERVICO_ORDERS_URL}/pedidos/{pedido_id}"
    dados, status_code = fazer_requisicao(url)
    
    if status_code == 200:
        dados["_gateway"] = {
            "processado_por": "API Gateway",
            "timestamp": datetime.now().isoformat(),
            "servico_origem": "microservico-orders"
        }
    
    return jsonify(dados), status_code

@app.route('/orders/user/<int:usuario_id>', methods=['GET'])
def obter_pedidos_usuario(usuario_id):
    url = f"{MICROSERVICO_ORDERS_URL}/pedidos/usuario/{usuario_id}"
    dados, status_code = fazer_requisicao(url)
    
    if status_code == 200:
        dados["_gateway"] = {
            "processado_por": "API Gateway",
            "timestamp": datetime.now().isoformat(),
            "servico_origem": "microservico-orders"
        }
    
    return jsonify(dados), status_code

@app.route('/health', methods=['GET'])
def health():
    users_status = "desconhecido"
    orders_status = "desconhecido"
    
    try:
        response = requests.get(f"{MICROSERVICO_USERS_URL}/health", timeout=3)
        if response.status_code == 200:
            users_status = "conectado"
        else:
            users_status = "erro"
    except:
        users_status = "desconectado"
    
    try:
        response = requests.get(f"{MICROSERVICO_ORDERS_URL}/health", timeout=3)
        if response.status_code == 200:
            orders_status = "conectado"
        else:
            orders_status = "erro"
    except:
        orders_status = "desconectado"
    
    gateway_healthy = (users_status == "conectado" and orders_status == "conectado")
    
    return jsonify({
        "status": "healthy" if gateway_healthy else "degraded",
        "servico": "api-gateway",
        "timestamp": datetime.now().isoformat(),
        "servicos": {
            "users": users_status,
            "orders": orders_status
        }
    })

@app.route('/status', methods=['GET'])
def status():
    users_info = {}
    orders_info = {}
    
    try:
        response = requests.get(f"{MICROSERVICO_USERS_URL}/", timeout=3)
        if response.status_code == 200:
            users_info = response.json()
            users_info["status"] = "online"
        else:
            users_info = {"status": "erro", "codigo": response.status_code}
    except Exception as e:
        users_info = {"status": "offline", "erro": str(e)}
    
    try:
        response = requests.get(f"{MICROSERVICO_ORDERS_URL}/", timeout=3)
        if response.status_code == 200:
            orders_info = response.json()
            orders_info["status"] = "online"
        else:
            orders_info = {"status": "erro", "codigo": response.status_code}
    except Exception as e:
        orders_info = {"status": "offline", "erro": str(e)}
    
    return jsonify({
        "gateway": {
            "status": "online",
            "versao": "1.0.0",
            "timestamp": datetime.now().isoformat()
        },
        "microsservicos": {
            "users": users_info,
            "orders": orders_info
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

