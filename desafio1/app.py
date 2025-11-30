from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return jsonify({
        'message': 'Olá! Servidor Flask funcionando!',
        'timestamp': timestamp,
        'status': 'success'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

