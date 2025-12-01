from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import requests
import os
import random

app = Flask(__name__)

MICROSERVICO_A_URL = os.getenv('MICROSERVICO_A_URL', 'http://microservico-a:5000')

def obter_usuarios():
    try:
        response = requests.get(f"{MICROSERVICO_A_URL}/usuarios", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"erro": f"Não foi possível conectar ao Microsserviço A: {str(e)}"}

def obter_usuario_por_id(usuario_id):
    try:
        response = requests.get(f"{MICROSERVICO_A_URL}/usuarios/{usuario_id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"erro": f"Não foi possível conectar ao Microsserviço A: {str(e)}"}

def calcular_data_ativo(dias_ativo):
    data_inicio = datetime.now() - timedelta(days=dias_ativo)
    return data_inicio.strftime('%Y-%m-%d')

@app.route('/')
def index():
    return jsonify({
        "servico": "Microsserviço B - Agregador de Informações",
        "versao": "1.0.0",
        "endpoints": {
            "/usuarios-completos": "Lista usuários com informações combinadas",
            "/usuario/<id>": "Retorna usuário específico com informações combinadas",
            "/health": "Health check"
        },
        "microservico_a_url": MICROSERVICO_A_URL
    })

@app.route('/usuarios-completos', methods=['GET'])
def listar_usuarios_completos():
    dados_a = obter_usuarios()
    
    if "erro" in dados_a:
        return jsonify(dados_a), 503
    
    usuarios_completos = []
    for usuario in dados_a.get("usuarios", []):
        dias_ativo = usuario["id"] * 30 + random.randint(1, 30)
        data_ativo_desde = calcular_data_ativo(dias_ativo)
        
        usuario_completo = {
            **usuario,
            "status": "ativo",
            "ativo_desde": data_ativo_desde,
            "dias_ativo": dias_ativo,
            "ultima_atualizacao": datetime.now().isoformat()
        }
        usuarios_completos.append(usuario_completo)
    
    return jsonify({
        "total": len(usuarios_completos),
        "fonte": "Microsserviço A + B (combinado)",
        "usuarios": usuarios_completos
    })

@app.route('/usuario/<int:usuario_id>', methods=['GET'])
def obter_usuario_completo(usuario_id):
    dados_a = obter_usuario_por_id(usuario_id)
    
    if "erro" in dados_a:
        return jsonify(dados_a), 404 if "não encontrado" in dados_a.get("erro", "").lower() else 503
    
    dias_ativo = usuario_id * 30 + random.randint(1, 30)
    data_ativo_desde = calcular_data_ativo(dias_ativo)
    
    usuario_completo = {
        **dados_a,
        "status": "ativo",
        "ativo_desde": data_ativo_desde,
        "dias_ativo": dias_ativo,
        "ultima_atualizacao": datetime.now().isoformat(),
        "informacoes_adicionais": {
            "processado_por": "Microsserviço B",
            "timestamp": datetime.now().isoformat()
        }
    }
    
    return jsonify(usuario_completo)

@app.route('/health', methods=['GET'])
def health():
    status_a = "desconhecido"
    try:
        response = requests.get(f"{MICROSERVICO_A_URL}/health", timeout=3)
        if response.status_code == 200:
            status_a = "conectado"
        else:
            status_a = "erro"
    except:
        status_a = "desconectado"
    
    return jsonify({
        "status": "healthy" if status_a == "conectado" else "degraded",
        "servico": "microservico-b",
        "microservico_a": status_a,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

