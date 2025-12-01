# Desafio 2 — Volumes e Persistência

## Objetivo
Demonstrar persistência de dados usando volumes Docker com PostgreSQL.

## Arquitetura

- **postgres**: Container com PostgreSQL 15 usando volume nomeado para persistência
- **cliente-db**: Container opcional que lê dados do banco para demonstrar acesso
- **postgres_data**: Volume Docker nomeado que persiste os dados do banco

## Estrutura do Projeto

```
desafio2/
├── docker-compose.yml          # Configuração dos containers e volumes
├── init.sql                    # Script SQL de inicialização
├── testar-persistencia.ps1     # Script de teste (PowerShell)
└── README.md                   # Este arquivo
```

## Como Executar

### Pré-requisitos
- Docker instalado
- Docker Compose instalado

### Passo 1: Iniciar o banco de dados

```bash
cd desafio2
docker-compose up -d postgres
```

### Passo 2: Verificar os dados iniciais

```bash
docker-compose exec postgres psql -U usuario -d desafio2_db -c "SELECT * FROM usuarios;"
```

### Passo 3: Executar o container cliente (opcional)

```bash
docker-compose up cliente-db
```

Este container se conecta ao banco e lista todos os usuários.

## Demonstração de Persistência

### Método 1: Usando o script de teste

No PowerShell:
```powershell
.\testar-persistencia.ps1
```

### Método 2: Manual

1. **Iniciar o container:**
   ```bash
   docker-compose up -d postgres
   ```

2. **Adicionar um novo registro:**
   ```bash
   docker-compose exec postgres psql -U usuario -d desafio2_db -c "INSERT INTO usuarios (nome, email) VALUES ('Novo Usuário', 'novo@email.com');"
   ```

3. **Verificar os dados:**
   ```bash
   docker-compose exec postgres psql -U usuario -d desafio2_db -c "SELECT * FROM usuarios;"
   ```

4. **Parar e remover o container:**
   ```bash
   docker-compose down
   ```

5. **Verificar que o volume ainda existe:**
   ```powershell
   docker volume ls | Select-String "desafio2_postgres_data"
   ```

6. **Recriar o container:**
   ```bash
   docker-compose up -d postgres
   ```

7. **Verificar que os dados persistiram:**
   ```bash
   docker-compose exec postgres psql -U usuario -d desafio2_db -c "SELECT * FROM usuarios;"
   ```

   **Resultado esperado:** Todos os dados, incluindo o registro adicionado no passo 2, ainda estarão presentes!

## Comandos Úteis

### Conectar ao banco de dados manualmente
```bash
docker-compose exec postgres psql -U usuario -d desafio2_db
```

### Ver logs do PostgreSQL
```bash
docker-compose logs -f postgres
```

### Ver informações do volume
```bash
docker volume inspect desafio2_postgres_data
```

### Verificar uso de espaço do volume
```bash
docker system df -v
```

### Adicionar mais dados
```bash
docker-compose exec postgres psql -U usuario -d desafio2_db -c "INSERT INTO usuarios (nome, email) VALUES ('Seu Nome', 'seu@email.com');"
```

### Contar registros
```bash
docker-compose exec postgres psql -U usuario -d desafio2_db -c "SELECT COUNT(*) FROM usuarios;"
```

## Detalhes Técnicos

### Volume Docker
- **Nome:** `desafio2_postgres_data`
- **Tipo:** Volume nomeado (named volume)
- **Localização no host:** Gerenciado pelo Docker
- **Localização no container:** `/var/lib/postgresql/data`

### Banco de Dados
- **Usuário:** `usuario`
- **Senha:** `senha123`
- **Nome do banco:** `desafio2_db`
- **Porta:** `5432` (mapeada para localhost)

### Tabela de Exemplo
A tabela `usuarios` contém:
- `id`: Chave primária auto-incrementada
- `nome`: Nome do usuário
- `email`: Email único
- `data_criacao`: Timestamp automático

## Por que os dados persistem?

1. **Volume nomeado:** O Docker cria um volume nomeado que existe independentemente dos containers
2. **Mapeamento:** O diretório `/var/lib/postgresql/data` do container está mapeado para o volume
3. **Ciclo de vida:** Quando você remove o container com `docker-compose down`, o volume **não é removido** (a menos que use `-v`)
4. **Recriação:** Ao recriar o container, o mesmo volume é reutilizado, mantendo todos os dados

## Limpeza

### Parar containers (mantém o volume)
```bash
docker-compose down
```

### Remover containers E volume (apaga todos os dados!)
```bash
docker-compose down -v
```

### Remover apenas o volume manualmente
```bash
docker volume rm desafio2_postgres_data
```

## Resultados Esperados

Após executar o teste de persistência, você deve ver:

1.  Dados iniciais carregados do `init.sql` (5 usuários)
2.  Novo registro adicionado durante o teste
3.  Volume permanece após remover o container
4.  Todos os dados (6 registros) presentes após recriar o container



