from flask import Flask, jsonify
import psycopg2
import redis
import os
from datetime import datetime

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'postgres')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'desafio3_db')
DB_USER = os.getenv('DB_USER', 'usuario')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'senha123')

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        return None

def get_redis_connection():
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        r.ping()
        return r
    except Exception as e:
        return None

@app.route('/')
def index():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    db_status = "desconectado"
    db_data = None
    db_conn = get_db_connection()
    if db_conn:
        try:
            db_status = "conectado"
            cursor = db_conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM usuarios;")
            db_data = cursor.fetchone()[0]
            cursor.close()
            db_conn.close()
        except Exception as e:
            db_status = f"erro: {str(e)}"
    
    redis_status = "desconectado"
    cache_data = None
    redis_conn = get_redis_connection()
    if redis_conn:
        try:
            redis_status = "conectado"
            visitas = redis_conn.incr('visitas')
            cache_data = visitas
        except Exception as e:
            redis_status = f"erro: {str(e)}"
    
    return jsonify({
        'mensagem': 'Aplicação funcionando!',
        'timestamp': timestamp,
        'servicos': {
            'web': {
                'status': 'online',
                'porta': 8080
            },
            'postgresql': {
                'status': db_status,
                'host': DB_HOST,
                'registros': db_data
            },
            'redis': {
                'status': redis_status,
                'host': REDIS_HOST,
                'visitas': cache_data
            }
        }
    })

@app.route('/db')
def db_info():
    conn = get_db_connection()
    if not conn:
        return jsonify({'erro': 'Não foi possível conectar ao PostgreSQL'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios ORDER BY id;")
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
        
        usuarios_list = [
            {
                'id': u[0],
                'nome': u[1],
                'email': u[2],
                'data_criacao': str(u[3])
            }
            for u in usuarios
        ]
        
        return jsonify({
            'total': len(usuarios_list),
            'usuarios': usuarios_list
        })
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/cache')
def cache_info():
    redis_conn = get_redis_connection()
    if not redis_conn:
        return jsonify({'erro': 'Não foi possível conectar ao Redis'}), 500
    
    try:
        visitas = redis_conn.get('visitas') or 0
        return jsonify({
            'visitas': int(visitas),
            'status': 'conectado'
        })
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/health')
def health():
    db_ok = get_db_connection() is not None
    redis_ok = get_redis_connection() is not None
    
    return jsonify({
        'status': 'healthy' if (db_ok and redis_ok) else 'degraded',
        'postgresql': 'ok' if db_ok else 'erro',
        'redis': 'ok' if redis_ok else 'erro'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

