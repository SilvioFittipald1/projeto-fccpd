# Desafio 5 — Microsserviços com API Gateway

## Objetivo
Criar uma arquitetura com API Gateway centralizando o acesso a dois microsserviços, demonstrando padrão de gateway como ponto único de entrada.

## Arquitetura

A solução consiste em **3 serviços** orquestrados:

### API Gateway
- **Porta:** 8080 (exposta ao cliente)
- **Função:** Ponto único de entrada que orquestra chamadas aos microsserviços
- **Endpoints:**
  - `GET /users` - Proxy para lista de usuários
  - `GET /users/<id>` - Proxy para usuário específico
  - `GET /orders` - Proxy para lista de pedidos
  - `GET /orders/<id>` - Proxy para pedido específico
  - `GET /orders/user/<user_id>` - Proxy para pedidos de um usuário
  - `GET /health` - Health check do gateway e serviços
  - `GET /status` - Status detalhado de todos os serviços

### Microsserviço de Usuários
- **Porta:** 5000 (apenas interna)
- **Função:** Fornece dados de usuários via API REST
- **Endpoints:**
  - `GET /usuarios` - Lista todos os usuários
  - `GET /usuarios/<id>` - Retorna usuário específico
  - `GET /health` - Health check

### Microsserviço de Pedidos
- **Porta:** 5001 (apenas interna)
- **Função:** Fornece dados de pedidos via API REST
- **Endpoints:**
  - `GET /pedidos` - Lista todos os pedidos
  - `GET /pedidos/<id>` - Retorna pedido específico
  - `GET /pedidos/usuario/<usuario_id>` - Retorna pedidos de um usuário
  - `GET /health` - Health check

### Fluxo de Comunicação

```
Cliente
  ↓ HTTP Request
API Gateway (porta 8080)
  ↓ HTTP Request (rede interna)
Microsserviço de Usuários (porta 5000) OU
Microsserviço de Pedidos (porta 5001)
  ↓ HTTP Response
API Gateway processa e adiciona metadados
  ↓ HTTP Response
Cliente recebe resposta
```

## Estrutura do Projeto

```
desafio5/
├── docker-compose.yml              # Orquestração de todos os serviços
├── gateway/
│   ├── Dockerfile                  # Dockerfile do Gateway
│   ├── app.py                      # Aplicação Flask do Gateway
│   └── requirements.txt            # Dependências Python
├── microservico-users/
│   ├── Dockerfile                  # Dockerfile do Microsserviço de Usuários
│   ├── app.py                      # Aplicação Flask
│   └── requirements.txt            # Dependências Python
├── microservico-orders/
│   ├── Dockerfile                  # Dockerfile do Microsserviço de Pedidos
│   ├── app.py                      # Aplicação Flask
│   └── requirements.txt            # Dependências Python
├── testar-gateway.ps1              # Script de teste
└── README.md                       # Este arquivo
```

## Como Executar

### Pré-requisitos
- Docker instalado
- Docker Compose instalado

### Passo 1: Iniciar todos os serviços

```powershell
cd desafio5
docker-compose up -d
```

### Passo 2: Verificar se os serviços estão rodando

```powershell
docker-compose ps
```

Você deve ver 3 containers:
- `api-gateway` (status: Up, healthy)
- `microservico-users` (status: Up, healthy)
- `microservico-orders` (status: Up, healthy)

### Passo 3: Testar o Gateway

**Opção 1: Usando o script de teste**
```powershell
.\testar-gateway.ps1
```

**Opção 2: Testar manualmente**

**Via Gateway (ponto único de entrada):**
```powershell
# Informações do Gateway
Invoke-RestMethod -Uri "http://localhost:8080/" | ConvertTo-Json

# Listar usuários via Gateway
Invoke-RestMethod -Uri "http://localhost:8080/users" | ConvertTo-Json

# Obter usuário específico via Gateway
Invoke-RestMethod -Uri "http://localhost:8080/users/1" | ConvertTo-Json

# Listar pedidos via Gateway
Invoke-RestMethod -Uri "http://localhost:8080/orders" | ConvertTo-Json

# Obter pedido específico via Gateway
Invoke-RestMethod -Uri "http://localhost:8080/orders/1" | ConvertTo-Json

# Obter pedidos de um usuário via Gateway
Invoke-RestMethod -Uri "http://localhost:8080/orders/user/1" | ConvertTo-Json

# Health check
Invoke-RestMethod -Uri "http://localhost:8080/health" | ConvertTo-Json

# Status detalhado
Invoke-RestMethod -Uri "http://localhost:8080/status" | ConvertTo-Json
```

**Opção 3: Acessar no navegador**
- Gateway: http://localhost:8080
- Todos os endpoints estão disponíveis via Gateway

## Endpoints Detalhados

### API Gateway

#### GET /
Informações sobre o Gateway e endpoints disponíveis.

**Resposta:**
```json
{
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
    "users": "http://microservico-users:5000",
    "orders": "http://microservico-orders:5001"
  }
}
```

#### GET /users
Lista todos os usuários (orquestra chamada ao Microsserviço de Usuários).

**Resposta:**
```json
{
  "total": 5,
  "usuarios": [
    {
      "id": 1,
      "nome": "Renato Moicano",
      "email": "renato@email.com",
      "telefone": "(11) 98765-4321",
      "cidade": "São Paulo"
    }
  ],
  "_gateway": {
    "processado_por": "API Gateway",
    "timestamp": "2024-01-01T12:00:00",
    "servico_origem": "microservico-users"
  }
}
```

#### GET /users/<id>
Retorna um usuário específico.

**Resposta:**
```json
{
  "id": 1,
  "nome": "Renato Moicano",
  "email": "renato@email.com",
  "telefone": "(11) 98765-4321",
  "cidade": "São Paulo",
  "_gateway": {
    "processado_por": "API Gateway",
    "timestamp": "2024-01-01T12:00:00",
    "servico_origem": "microservico-users"
  }
}
```

#### GET /orders
Lista todos os pedidos (orquestra chamada ao Microsserviço de Pedidos).

**Resposta:**
```json
{
  "total": 7,
  "pedidos": [
    {
      "id": 1,
      "usuario_id": 1,
      "produto": "Notebook",
      "valor": 3500.00,
      "status": "entregue",
      "data": "2023-12-27"
    }
  ],
  "_gateway": {
    "processado_por": "API Gateway",
    "timestamp": "2024-01-01T12:00:00",
    "servico_origem": "microservico-orders"
  }
}
```

#### GET /orders/<id>
Retorna um pedido específico.

**Resposta:**
```json
{
  "id": 1,
  "usuario_id": 1,
  "produto": "Notebook",
  "valor": 3500.00,
  "status": "entregue",
  "data": "2023-12-27",
  "_gateway": {
    "processado_por": "API Gateway",
    "timestamp": "2024-01-01T12:00:00",
    "servico_origem": "microservico-orders"
  }
}
```

#### GET /orders/user/<user_id>
Retorna todos os pedidos de um usuário específico.

**Resposta:**
```json
{
  "usuario_id": 1,
  "total": 2,
  "pedidos": [
    {
      "id": 1,
      "usuario_id": 1,
      "produto": "Notebook",
      "valor": 3500.00,
      "status": "entregue",
      "data": "2023-12-27"
    },
    {
      "id": 2,
      "usuario_id": 1,
      "produto": "Mouse",
      "valor": 89.90,
      "status": "entregue",
      "data": "2023-12-29"
    }
  ],
  "_gateway": {
    "processado_por": "API Gateway",
    "timestamp": "2024-01-01T12:00:00",
    "servico_origem": "microservico-orders"
  }
}
```

#### GET /health
Health check do Gateway e verificação de conexão com microsserviços.

**Resposta:**
```json
{
  "status": "healthy",
  "servico": "api-gateway",
  "timestamp": "2024-01-01T12:00:00",
  "servicos": {
    "users": "conectado",
    "orders": "conectado"
  }
}
```

#### GET /status
Status detalhado de todos os serviços.

**Resposta:**
```json
{
  "gateway": {
    "status": "online",
    "versao": "1.0.0",
    "timestamp": "2024-01-01T12:00:00"
  },
  "microsservicos": {
    "users": {
      "servico": "Microsserviço de Usuários",
      "versao": "1.0.0",
      "status": "online"
    },
    "orders": {
      "servico": "Microsserviço de Pedidos",
      "versao": "1.0.0",
      "status": "online"
    }
  }
}
```

## Detalhes Técnicos

### Isolamento e Portas

- **Gateway:** Porta 8080 exposta ao host (único ponto de entrada)
- **Microsserviço de Usuários:** Porta 5000 apenas interna (não exposta)
- **Microsserviço de Pedidos:** Porta 5001 apenas interna (não exposta)

**Benefício:** Clientes só precisam conhecer uma URL (Gateway), os microsserviços ficam isolados.

### Comunicação

- **Cliente → Gateway:** HTTP na porta 8080
- **Gateway → Microsserviços:** HTTP na rede interna usando nomes de containers:
  - `http://microservico-users:5000`
  - `http://microservico-orders:5001`

### Dependências

O `docker-compose.yml` configura:
- **Gateway** depende de ambos os microsserviços estarem healthy
- Usa `depends_on` com condição `service_healthy`

### Variáveis de Ambiente

O Gateway recebe URLs dos microsserviços:
```yaml
environment:
  MICROSERVICO_USERS_URL: http://microservico-users:5000
  MICROSERVICO_ORDERS_URL: http://microservico-orders:5001
```

### Metadados do Gateway

Todas as respostas do Gateway incluem metadados `_gateway`:
- `processado_por`: Identifica que passou pelo Gateway
- `timestamp`: Quando foi processado
- `servico_origem`: Qual microsserviço forneceu os dados

## Fluxo de Requisição Completo

### Exemplo: Obter usuário via Gateway

1. **Cliente faz requisição:**
   ```
   GET http://localhost:8080/users/1
   ```

2. **Gateway recebe e processa:**
   - Identifica que é uma requisição de usuário
   - Faz proxy para `http://microservico-users:5000/usuarios/1`

3. **Microsserviço de Usuários responde:**
   ```json
   {
     "id": 1,
     "nome": "Renato Moicano",
     "email": "renato@email.com",
     ...
   }
   ```

4. **Gateway adiciona metadados:**
   ```json
   {
     "id": 1,
     "nome": "Renato Moicano",
     ...
     "_gateway": {
       "processado_por": "API Gateway",
       "timestamp": "2024-01-01T12:00:00",
       "servico_origem": "microservico-users"
     }
   }
   ```

5. **Cliente recebe resposta final**

## Comandos Úteis

### Ver logs de todos os serviços
```powershell
docker-compose logs -f
```

### Ver logs de um serviço específico
```powershell
docker-compose logs -f gateway
docker-compose logs -f microservico-users
docker-compose logs -f microservico-orders
```

### Parar todos os serviços
```powershell
docker-compose down
```

### Reiniciar um serviço específico
```powershell
docker-compose restart gateway
docker-compose restart microservico-users
docker-compose restart microservico-orders
```

### Ver status dos serviços
```powershell
docker-compose ps
```

### Verificar a rede
```powershell
docker network inspect gateway-network
```

### Reconstruir as imagens
```powershell
docker-compose up -d --build
```

## Exemplo de Uso Completo

### Cenário: Obter informações de um usuário e seus pedidos

**1. Obter usuário via Gateway:**
```powershell
$usuario = Invoke-RestMethod -Uri "http://localhost:8080/users/1"
$usuario | ConvertTo-Json
```

**2. Obter pedidos do usuário via Gateway:**
```powershell
$pedidos = Invoke-RestMethod -Uri "http://localhost:8080/orders/user/1"
$pedidos | ConvertTo-Json
```

**3. Combinar informações:**
```powershell
$resultado = @{
    usuario = $usuario
    pedidos = $pedidos.pedidos
    total_pedidos = $pedidos.total
}
$resultado | ConvertTo-Json -Depth 10
```


