#!/bin/sh

echo "Cliente iniciado. Fazendo requisiçoes para o servidor Flask..."
echo "Servidor: http://flask-server:8080"
echo ""

while true; do
    echo "=========================================="
    echo "Requisição em $(date '+%Y-%m-%d %H:%M:%S')"
    echo "=========================================="
    curl -s http://flask-server:8080/
    echo ""
    echo ""
    echo "Status da saúde:"
    curl -s http://flask-server:8080/health
    echo ""
    echo ""
    echo "Aguardando 5 segundos antes da proxima requisiçao..."
    sleep 5
done

