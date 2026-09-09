# Sistema JMC

Sistema de gestão comercial e industrial da JMC, construído inicialmente com FastAPI, PostgreSQL e uma base para frontend web.

## Stack
- Backend: Python + FastAPI
- Banco: PostgreSQL
- Autenticação: JWT (access token) + bcrypt
- Infra: Docker Compose

## Estrutura
```text
backend/       API e autenticação
frontend/      aplicação web (base)
database/      scripts SQL
infra/         configuração de infraestrutura
docs/          documentação
```

## Desenvolvimento
1. Copie `.env.example` para `.env`.
2. Suba os serviços com `docker compose up --build`.
3. API: `http://localhost:8000`
4. Documentação: `http://localhost:8000/docs`

A primeira etapa implementa usuários, login, JWT e rota protegida.
