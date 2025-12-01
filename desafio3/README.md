# Desafio 3 — Docker Compose Orquestrando Serviços

## Objetivo
Demonstrar orquestração de múltiplos serviços usando Docker Compose, com comunicação entre serviços, dependências e rede interna.

## Arquitetura

A aplicação é composta por **3 serviços** que se comunicam através de uma rede Docker customizada:

### Serviços

1. **Web (Flask)** - Aplicação web na porta 8080
   - Conecta ao PostgreSQL para ler dados
   - Conecta ao Redis para cache/contador de visitas
   - Expõe endpoints REST para verificar status dos serviços

2. **PostgreSQL** - Banco de dados relacional
   - Armazena dados de usuários
   - Volume persistente para dados
   - Health check configurado

3. **Redis** - Cache em memória
   - Armazena contador de visitas
   - Volume persistente para dados
   - Health check configurado

### Rede

- **desafio3-network**: Rede bridge customizada que conecta todos os serviços
- Os serviços se comunicam usando os nomes dos containers como hostnames

## Estrutura do Projeto

```
desafio3/
├── docker-compose.yml          # Orquestração dos 3 serviços
├── Dockerfile                  # Dockerfile do serviço web
├── app.py                      # Aplicação Flask
├── requirements.txt            # Dependências Python
├── init.sql                    # Script de inicialização do banco
├── testar-servicos.ps1         # Script de teste (PowerShell)
└── README.md                   # Este arquivo
```

## Como Executar

### Pré-requisitos
- Docker instalado
- Docker Compose instalado

### Passo 1: Iniciar todos os serviços

```powershell
cd desafio3
docker-compose up -d
```

### Passo 2: Verificar se os serviços estão rodando

```powershell
docker-compose ps
```

Você deve ver 3 containers:
- `desafio3-web` (status: Up)
- `desafio3-postgres` (status: Up, healthy)
- `desafio3-redis` (status: Up, healthy)

### Passo 3: Testar a aplicação

**Opção 1: Usando o script de teste**
```powershell
.\testar-servicos.ps1
```

**Opção 2: Acessar no navegador**
- Abra: http://localhost:8080
- Endpoint principal: http://localhost:8080/
- Banco de dados: http://localhost:8080/db
- Cache: http://localhost:8080/cache
- Health check: http://localhost:8080/health

**Opção 3: Usando PowerShell**
```powershell
# Endpoint principal
Invoke-RestMethod -Uri "http://localhost:8080/" | ConvertTo-Json

# Banco de dados
Invoke-RestMethod -Uri "http://localhost:8080/db" | ConvertTo-Json

# Cache
Invoke-RestMethod -Uri "http://localhost:8080/cache" | ConvertTo-Json

# Health check
Invoke-RestMethod -Uri "http://localhost:8080/health" | ConvertTo-Json
```

## Endpoints da Aplicação

### GET /
Endpoint principal que verifica o status de todos os serviços.

**Resposta:**
```json
{
  "mensagem": "Aplicação funcionando!",
  "timestamp": "2024-01-01 12:00:00",
  "servicos": {
    "web": {
      "status": "online",
      "porta": 8080
    },
    "postgresql": {
      "status": "conectado",
      "host": "postgres",
      "registros": 5
    },
    "redis": {
      "status": "conectado",
      "host": "redis",
      "visitas": 1
    }
  }
}
```

### GET /db
Lista todos os usuários do banco de dados.

**Resposta:**
```json
{
  "total": 5,
  "usuarios": [
    {
      "id": 1,
      "nome": "Renato Moicano",
      "email": "renato@email.com",
      "data_criacao": "2024-01-01 12:00:00"
    }
  ]
}
```

### GET /cache
Retorna informações do cache Redis (contador de visitas).

**Resposta:**
```json
{
  "visitas": 5,
  "status": "conectado"
}
```

### GET /health
Health check da aplicação.

**Resposta:**
```json
{
  "status": "healthy",
  "postgresql": "ok",
  "redis": "ok"
}
```

## Detalhes Técnicos

### Dependências entre Serviços

O `docker-compose.yml` configura dependências usando `depends_on`:

- **web** depende de:
  - `postgres` (condição: `service_healthy`)
  - `redis` (condição: `service_started`)

Isso garante que:
1. O PostgreSQL esteja saudável antes do web iniciar
2. O Redis esteja iniciado antes do web iniciar

### Variáveis de Ambiente

O serviço web recebe variáveis de ambiente para conectar aos outros serviços:

```yaml
environment:
  DB_HOST: postgres          # Nome do serviço PostgreSQL
  DB_PORT: 5432
  DB_NAME: desafio3_db
  DB_USER: usuario
  DB_PASSWORD: senha123
  REDIS_HOST: redis          # Nome do serviço Redis
  REDIS_PORT: 6379
```

### Comunicação entre Serviços

Os serviços se comunicam usando os **nomes dos serviços** como hostnames:
- `postgres` → acessa o container PostgreSQL
- `redis` → acessa o container Redis

Isso é possível porque todos estão na mesma rede Docker (`desafio3-network`).

### Health Checks

Ambos PostgreSQL e Redis possuem health checks configurados:

**PostgreSQL:**
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U usuario -d desafio3_db"]
  interval: 5s
  timeout: 5s
  retries: 5
```

**Redis:**
```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 5s
  timeout: 3s
  retries: 5
```

## Comandos Úteis

### Ver logs de todos os serviços
```powershell
docker-compose logs -f
```

### Ver logs de um serviço específico
```powershell
docker-compose logs -f web
docker-compose logs -f postgres
docker-compose logs -f redis
```

### Parar todos os serviços
```powershell
docker-compose down
```

### Parar e remover volumes (apaga dados)
```powershell
docker-compose down -v
```

### Reiniciar um serviço específico
```powershell
docker-compose restart web
```

### Ver status dos serviços
```powershell
docker-compose ps
```

### Verificar a rede
```powershell
docker network inspect desafio3-network
```

### Conectar ao banco de dados manualmente
```powershell
docker-compose exec postgres psql -U usuario -d desafio3_db
```

### Conectar ao Redis manualmente
```powershell
docker-compose exec redis redis-cli
```

## Fluxo de Comunicação

1. **Inicialização:**
   - PostgreSQL inicia e executa `init.sql`
   - Redis inicia
   - Web aguarda PostgreSQL ficar healthy
   - Web inicia e conecta aos serviços

2. **Requisição HTTP:**
   - Cliente → Web (porta 8080)
   - Web → PostgreSQL (via rede interna)
   - Web → Redis (via rede interna)
   - Web → Resposta JSON ao cliente

3. **Comunicação Interna:**
   - Todos os serviços na rede `desafio3-network`
   - Comunicação usando nomes de serviços como hostnames
   - Portas internas não expostas ao host

```

#


