# Projeto FCCPD - Desafios com Docker e Microsserviços

Este projeto contém 5 desafios práticos demonstrando conceitos fundamentais de Docker, Docker Compose, volumes, redes e arquitetura de microsserviços.

## Visão Geral

O projeto é dividido em duas categorias principais:

### Desafios com Docker (3 desafios)
1. **Desafio 1** - Containers em Rede
2. **Desafio 2** - Volumes e Persistência
3. **Desafio 3** - Docker Compose Orquestrando Serviços

### Desafios com Microsserviços (2 desafios)
4. **Desafio 4** - Microsserviços Independentes
5. **Desafio 5** - Microsserviços com API Gateway

## Estrutura do Projeto

```
projeto-fccpd/
├── desafio1/          # Containers em Rede
├── desafio2/          # Volumes e Persistência
├── desafio3/          # Docker Compose Orquestrando Serviços
├── desafio4/          # Microsserviços Independentes
├── desafio5/          # Microsserviços com API Gateway
└── README.md          # Este arquivo
```

## Pré-requisitos

Requisitos necessários para execução dos desafios:

- **Docker** (versão 20.10 ou superior)
- **Docker Compose** (versão 2.0 ou superior)
- **PowerShell** (para scripts de teste no Windows)

Verificação das instalações:
```powershell
docker --version
docker-compose --version
```

## Desafios

### Desafio 1 — Containers em Rede
**Objetivo:** Demonstrar comunicação entre containers através de uma rede Docker customizada.

**Conceitos abordados:**
- Criação de rede Docker customizada
- Comunicação entre containers usando hostnames
- Servidor web Flask
- Cliente HTTP com requisições periódicas

**Como executar:**
```powershell
cd desafio1
docker-compose up -d --build
```

**Documentação completa:** [desafio1/README.md](desafio1/README.md)

---

### Desafio 2 — Volumes e Persistência
**Objetivo:** Demonstrar persistência de dados usando volumes Docker com PostgreSQL.

**Conceitos abordados:**
- Volumes Docker nomeados
- Persistência de dados de banco de dados
- Inicialização de banco com scripts SQL
- Demonstração de persistência após remoção de containers

**Como executar:**
```powershell
cd desafio2
docker-compose up -d postgres
```

**Documentação completa:** [desafio2/README.md](desafio2/README.md)

---

### Desafio 3 — Docker Compose Orquestrando Serviços
**Objetivo:** Orquestrar múltiplos serviços dependentes usando Docker Compose.

**Conceitos abordados:**
- Orquestração de 3 serviços (web, db, cache)
- Dependências entre serviços com `depends_on`
- Health checks
- Variáveis de ambiente
- Rede interna para comunicação

**Como executar:**
```powershell
cd desafio3
docker-compose up -d
```

**Documentação completa:** [desafio3/README.md](desafio3/README.md)

---

### Desafio 4 — Microsserviços Independentes
**Objetivo:** Criar dois microsserviços independentes que se comunicam via HTTP.

**Conceitos abordados:**
- Arquitetura de microsserviços
- Comunicação HTTP entre serviços
- Isolamento de serviços com Dockerfiles separados
- Agregação de dados entre microsserviços

**Como executar:**
```powershell
cd desafio4
docker-compose up -d --build
```

**Documentação completa:** [desafio4/README.md](desafio4/README.md)

---

### Desafio 5 — Microsserviços com API Gateway
**Objetivo:** Criar uma arquitetura com API Gateway centralizando o acesso a microsserviços.

**Conceitos abordados:**
- Padrão API Gateway
- Ponto único de entrada para múltiplos serviços
- Orquestração de chamadas
- Isolamento de microsserviços (portas internas)

**Como executar:**
```powershell
cd desafio5
docker-compose up -d --build
```

**Documentação completa:** [desafio5/README.md](desafio5/README.md)

## Testando os Desafios

Cada desafio possui scripts de teste em PowerShell para facilitar a validação:

- `desafio2/testar-persistencia.ps1`
- `desafio3/testar-servicos.ps1`
- `desafio4/testar-microsservicos.ps1`
- `desafio5/testar-gateway.ps1`

Execução dos scripts dentro do diretório de cada desafio:
```powershell
cd desafioX
.\testar-*.ps1
```

## Limpeza

Parar e remover todos os containers, redes e volumes de um desafio:

```powershell
docker-compose down
```

Remover também os volumes (apaga dados persistidos):

```powershell
docker-compose down -v
```

## Documentação

Cada desafio possui um README.md completo contendo:

- **Descrição da solução, arquitetura e decisões técnicas**
- **Explicação detalhada do funcionamento** (containers, rede, microsserviços, fluxos)
- **Instruções de execução passo a passo** (como subir os containers e testar)

## Tecnologias Utilizadas

- **Docker** - Containerização
- **Docker Compose** - Orquestração de containers
- **Flask** - Framework web Python
- **PostgreSQL** - Banco de dados relacional
- **Redis** - Cache em memória
- **Python** - Linguagem de programação
- **PowerShell** - Scripts de teste

## Notas Importantes

- Todos os desafios foram testados no Windows com PowerShell
- As portas utilizadas podem conflitar com outros serviços em execução
- Os volumes Docker persistem dados mesmo após remover containers
- O comando `docker-compose down -v` remove volumes e apaga dados persistidos

## Objetivos de Aprendizado

Conceitos abordados neste projeto:

1. **Rede Docker:** Criação e uso de redes customizadas para comunicação entre containers
2. **Volumes:** Uso de volumes para persistência de dados
3. **Docker Compose:** Orquestração de múltiplos serviços com dependências
4. **Microsserviços:** Criação e comunicação de microsserviços independentes
5. **API Gateway:** Implementação de gateway como ponto único de entrada

## Licença

Este projeto é parte de um curso/avaliação acadêmica.
