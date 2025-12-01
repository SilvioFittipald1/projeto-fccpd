# Desafio 4 — Microsserviços Independentes

## Objetivo
Criar dois microsserviços independentes que se comunicam via HTTP, demonstrando arquitetura de microsserviços sem gateway.

## Arquitetura

A solução consiste em **2 microsserviços independentes** que se comunicam via requisições HTTP:

### Microsserviço A - API de Usuários
- **Porta:** 5000
- **Função:** Fornece dados de usuários via API REST
- **Endpoints:**
  - `GET /usuarios` - Lista todos os usuários
  - `GET /usuarios/<id>` - Retorna usuário específico
  - `GET /health` - Health check

### Microsserviço B - Agregador de Informações
- **Porta:** 5001
- **Função:** Consome o Microsserviço A e adiciona informações combinadas
- **Endpoints:**
  - `GET /usuarios-completos` - Lista usuários com informações adicionais
  - `GET /usuario/<id>` - Retorna usuário específico com informações combinadas
  - `GET /health` - Health check (verifica conexão com Microsserviço A)

### Comunicação

```
Cliente → Microsserviço B (porta 5001)
           ↓ HTTP Request
           Microsserviço A (porta 5000)
           ↓ HTTP Response
           Microsserviço B processa e adiciona dados
           ↓ HTTP Response
           Cliente recebe dados combinados
```

## Estrutura do Projeto

```
desafio4/
├── docker-compose.yml              # Orquestração dos microsserviços
├── microservico-a/
│   ├── Dockerfile                  # Dockerfile do Microsserviço A
│   ├── app.py                      # Aplicação Flask do Microsserviço A
│   └── requirements.txt            # Dependências Python
├── microservico-b/
│   ├── Dockerfile                  # Dockerfile do Microsserviço B
│   ├── app.py                      # Aplicação Flask do Microsserviço B
│   └── requirements.txt            # Dependências Python
├── testar-microsservicos.ps1      # Script de teste
└── README.md                       # Este arquivo
```

## Como Executar

### Pré-requisitos
- Docker instalado
- Docker Compose instalado

### Passo 1: Iniciar os microsserviços

```powershell
cd desafio4
docker-compose up -d
```

### Passo 2: Verificar se os serviços estão rodando

```powershell
docker-compose ps
```

Você deve ver 2 containers:
- `microservico-a` (status: Up, healthy)
- `microservico-b` (status: Up, healthy)

### Passo 3: Testar os microsserviços

**Opção 1: Usando o script de teste**
```powershell
.\testar-microsservicos.ps1
```

**Opção 2: Testar manualmente**

**Microsserviço A (diretamente):**
```powershell
# Listar todos os usuários
Invoke-RestMethod -Uri "http://localhost:5000/usuarios" | ConvertTo-Json

# Obter usuário específico
Invoke-RestMethod -Uri "http://localhost:5000/usuarios/1" | ConvertTo-Json

# Health check
Invoke-RestMethod -Uri "http://localhost:5000/health" | ConvertTo-Json
```

**Microsserviço B (consome o A):**
```powershell
# Listar usuários com informações combinadas
Invoke-RestMethod -Uri "http://localhost:5001/usuarios-completos" | ConvertTo-Json

# Obter usuário específico com informações combinadas
Invoke-RestMethod -Uri "http://localhost:5001/usuario/1" | ConvertTo-Json

# Health check (verifica conexão com Microsserviço A)
Invoke-RestMethod -Uri "http://localhost:5001/health" | ConvertTo-Json
```

**Opção 3: Acessar no navegador**
- Microsserviço A: http://localhost:5000
- Microsserviço B: http://localhost:5001

## Endpoints Detalhados

### Microsserviço A

#### GET /
Informações sobre o serviço.

**Resposta:**
```json
{
  "servico": "Microsserviço A - API de Usuários",
  "versao": "1.0.0",
  "endpoints": {
    "/usuarios": "Lista todos os usuários",
    "/usuarios/<id>": "Retorna um usuário específico",
    "/health": "Health check"
  }
}
```

#### GET /usuarios
Retorna lista completa de usuários.

**Resposta:**
```json
{
  "total": 5,
  "usuarios": [
    {
      "id": 1,
      "nome": "Renato Moicano",
      "email": "renato@email.com",
      "cargo": "Desenvolvedor",
      "departamento": "TI"
    }
  ]
}
```

#### GET /usuarios/<id>
Retorna um usuário específico por ID.

**Resposta:**
```json
{
  "id": 1,
  "nome": "Renato Moicano",
  "email": "renato@email.com",
  "cargo": "Desenvolvedor",
  "departamento": "TI"
}
```

#### GET /health
Health check do serviço.

**Resposta:**
```json
{
  "status": "healthy",
  "servico": "microservico-a",
  "timestamp": "2024-01-01T12:00:00"
}
```

### Microsserviço B

#### GET /
Informações sobre o serviço.

**Resposta:**
```json
{
  "servico": "Microsserviço B - Agregador de Informações",
  "versao": "1.0.0",
  "endpoints": {
    "/usuarios-completos": "Lista usuários com informações combinadas",
    "/usuario/<id>": "Retorna usuário específico com informações combinadas",
    "/health": "Health check"
  },
  "microservico_a_url": "http://microservico-a:5000"
}
```

#### GET /usuarios-completos
Consome o Microsserviço A e adiciona informações combinadas (status, data ativo desde, dias ativo).

**Resposta:**
```json
{
  "total": 5,
  "fonte": "Microsserviço A + B (combinado)",
  "usuarios": [
    {
      "id": 1,
      "nome": "Renato Moicano",
      "email": "renato@email.com",
      "cargo": "Desenvolvedor",
      "departamento": "TI",
      "status": "ativo",
      "ativo_desde": "2023-11-01",
      "dias_ativo": 61,
      "ultima_atualizacao": "2024-01-01T12:00:00"
    }
  ]
}
```

#### GET /usuario/<id>
Consome o Microsserviço A e retorna usuário específico com informações combinadas.

**Resposta:**
```json
{
  "id": 1,
  "nome": "Renato Moicano",
  "email": "renato@email.com",
  "cargo": "Desenvolvedor",
  "departamento": "TI",
  "status": "ativo",
  "ativo_desde": "2023-11-01",
  "dias_ativo": 61,
  "ultima_atualizacao": "2024-01-01T12:00:00",
  "informacoes_adicionais": {
    "processado_por": "Microsserviço B",
    "timestamp": "2024-01-01T12:00:00"
  }
}
```

#### GET /health
Health check do serviço e verificação de conexão com Microsserviço A.

**Resposta:**
```json
{
  "status": "healthy",
  "servico": "microservico-b",
  "microservico_a": "conectado",
  "timestamp": "2024-01-01T12:00:00"
}
```

## Detalhes Técnicos

### Isolamento

Cada microsserviço possui:
-  **Dockerfile próprio** - Isolamento completo
-  **Dependências próprias** - Cada serviço gerencia suas dependências
-  **Container separado** - Execução independente
-  **Porta própria** - 5000 (A) e 5001 (B)

### Comunicação HTTP

- **Protocolo:** HTTP REST
- **Formato:** JSON
- **Método:** GET
- **Rede:** Rede Docker customizada (`microsservicos-network`)
- **Hostname:** Os serviços se comunicam usando os nomes dos containers:
  - `microservico-a:5000` (interno)
  - `microservico-b:5001` (interno)

### Dependências

O `docker-compose.yml` configura:
- **Microsserviço B** depende de **Microsserviço A** estar healthy
- Usa `depends_on` com condição `service_healthy`

### Variáveis de Ambiente

O Microsserviço B recebe:
```yaml
environment:
  MICROSERVICO_A_URL: http://microservico-a:5000
```

Isso permite configurar a URL do Microsserviço A sem modificar código.

## Fluxo de Comunicação

1. **Cliente faz requisição ao Microsserviço B:**
   ```
   GET http://localhost:5001/usuarios-completos
   ```

2. **Microsserviço B faz requisição ao Microsserviço A:**
   ```
   GET http://microservico-a:5000/usuarios
   ```

3. **Microsserviço A retorna dados:**
   ```json
   {
     "total": 5,
     "usuarios": [...]
   }
   ```

4. **Microsserviço B processa e adiciona informações:**
   - Calcula dias ativo
   - Adiciona data "ativo desde"
   - Adiciona status
   - Adiciona timestamp

5. **Microsserviço B retorna dados combinados ao cliente:**
   ```json
   {
     "total": 5,
     "fonte": "Microsserviço A + B (combinado)",
     "usuarios": [...]
   }
   ```

## Comandos Úteis

### Ver logs de todos os serviços
```powershell
docker-compose logs -f
```

### Ver logs de um serviço específico
```powershell
docker-compose logs -f microservico-a
docker-compose logs -f microservico-b
```

### Parar todos os serviços
```powershell
docker-compose down
```

### Reiniciar um serviço específico
```powershell
docker-compose restart microservico-a
docker-compose restart microservico-b
```

### Ver status dos serviços
```powershell
docker-compose ps
```

### Verificar a rede
```powershell
docker network inspect microsservicos-network
```

### Reconstruir as imagens
```powershell
docker-compose up -d --build
```

## Exemplo de Uso

### Cenário: Obter informações completas de um usuário

**1. Requisição direta ao Microsserviço A:**
```powershell
$usuarioA = Invoke-RestMethod -Uri "http://localhost:5000/usuarios/1"
$usuarioA | ConvertTo-Json
```

**Resposta:**
```json
{
  "id": 1,
  "nome": "Renato Moicano",
  "email": "renato@email.com",
  "cargo": "Desenvolvedor",
  "departamento": "TI"
}
```

**2. Requisição ao Microsserviço B (com informações combinadas):**
```powershell
$usuarioB = Invoke-RestMethod -Uri "http://localhost:5001/usuario/1"
$usuarioB | ConvertTo-Json
```

**Resposta:**
```json
{
  "id": 1,
  "nome": "Renato Moicano",
  "email": "renato@email.com",
  "cargo": "Desenvolvedor",
  "departamento": "TI",
  "status": "ativo",
  "ativo_desde": "2023-11-01",
  "dias_ativo": 61,
  "ultima_atualizacao": "2024-01-01T12:00:00",
  "informacoes_adicionais": {
    "processado_por": "Microsserviço B",
    "timestamp": "2024-01-01T12:00:00"
  }
}
```

