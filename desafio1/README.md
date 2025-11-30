# Desafio 1 — Containers em Rede

## Objetivo
Demonstrar comunicação entre dois containers Docker através de uma rede customizada.

## Arquitetura

- **flask-server**: Container com servidor Flask rodando na porta 8080
- **curl-client**: Container que realiza requisições HTTP periódicas para o servidor
- **desafio1-network**: Rede Docker customizada que conecta ambos os containers

## Estrutura do Projeto

```
desafio1/
├── app.py                 # Aplicação Flask
├── requirements.txt       # Dependências Python
├── Dockerfile.server      # Dockerfile do servidor Flask
├── Dockerfile.client      # Dockerfile do cliente curl
├── client.sh              # Script do cliente (requisições periódicas)
├── docker-compose.yml     # Orquestração dos containers e rede
└── README.md             # Este arquivo
```

## Como Executar

### Pré-requisitos
- Docker instalado
- Docker Compose instalado

### Passos

1. **Navegue até o diretório do desafio:**
   ```bash
   cd desafio1
   ```

2. **Execute os containers:**
   ```bash
   docker-compose up --build
   ```

3. **Para executar em background:**
   ```bash
   docker-compose up -d --build
   ```

4. **Visualizar logs:**
   ```bash
   # Logs de todos os containers
   docker-compose logs -f
   
   # Logs apenas do servidor
   docker-compose logs -f flask-server
   
   # Logs apenas do cliente
   docker-compose logs -f curl-client
   ```

5. **Parar os containers:**
   ```bash
   docker-compose down
   ```

## Verificação

### 1. Verificar a rede customizada
```bash
docker network ls
```
Você deve ver a rede `desafio1-network` listada.

### 2. Verificar containers em execução
```bash
docker ps
```
Você deve ver os containers `flask-server` e `curl-client` rodando.

### 3. Verificar comunicação
- Os logs do `curl-client` mostrarão requisições periódicas sendo feitas ao servidor
- Os logs do `flask-server` mostrarão as requisições recebidas
- Você pode acessar o servidor diretamente em: http://localhost:8080

### 4. Testar manualmente
```bash
# Acessar o servidor diretamente
curl http://localhost:8080

# Verificar saúde
curl http://localhost:8080/health
```

## Detalhes Técnicos

### Rede Docker
- Nome: `desafio1-network`
- Driver: `bridge`
- Permite comunicação entre containers usando os nomes dos serviços como hostnames

### Servidor Flask
- Porta interna: 8080
- Porta exposta: 8080 (mapeada para localhost)
- Endpoints:
  - `GET /`: Retorna mensagem de boas-vindas com timestamp
  - `GET /health`: Retorna status de saúde

### Cliente Curl
- Faz requisições a cada 5 segundos
- Conecta ao servidor usando o hostname `flask-server` (resolvido pela rede Docker)
- Exibe logs formatados de cada requisição

## Logs Esperados

### Servidor Flask
```
 * Running on http://0.0.0.0:8080
 * Debug mode: on
127.0.0.1 - - [timestamp] "GET / HTTP/1.1" 200 -
```

### Cliente Curl
```
==========================================
Requisição em 2024-01-01 12:00:00
==========================================
{
  "message": "Olá! Servidor Flask funcionando!",
  "timestamp": "2024-01-01 12:00:00",
  "status": "success"
}
```

## Limpeza

Para remover tudo (containers, rede, volumes):
```bash
docker-compose down
```

Para remover também as imagens:
```bash
docker-compose down --rmi all
```

