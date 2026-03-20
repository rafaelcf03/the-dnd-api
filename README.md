# D&D Character Sheet API

API de referência para criação de fichas de personagem de D&D, suportando as edições **2014 (5e)** e **2024 (5.5e)**.

## Tech Stack

- **Python 3.11** + **FastAPI**
- **GraphQL** via Graphene 3
- **MongoDB 7** com Beanie (ODM async)
- **Docker** + **Docker Compose**

## Quick Start

```bash
cp .env.example .env
docker compose up --build -d
```

### Seed do banco de dados

```bash
docker compose exec api python -m scripts.seed_db
```

### Endpoints GraphQL

| Edição | URL                            | GraphiQL (browser) |
|--------|--------------------------------|---------------------|
| 2014   | `http://localhost:8000/api/5e/`    | GET no browser      |
| 2024   | `http://localhost:8000/api/5_5e/`  | GET no browser      |

### Exemplo de query

```graphql
{
  classes {
    name
    hitDie
    subclasses {
      name
    }
  }
  spells(level: 1, school: "evocation") {
    name
    castingTime
    range
  }
}
```

## Estrutura do Projeto

```
dnd-api/
├── app/
│   ├── main.py            # FastAPI app + lifespan
│   ├── config.py          # Settings (Pydantic)
│   ├── database.py        # MongoDB init
│   ├── models/            # Beanie Documents
│   └── graphql/           # Schema, types, queries
├── scripts/
│   └── seed_db.py         # Popular banco via JSON
├── seed/                  # Dados estáticos por edição
├── docker-compose.yml
└── Dockerfile
```
