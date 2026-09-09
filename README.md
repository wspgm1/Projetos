# Sistema JMC

Sistema de gestão comercial e industrial da JMC.

## Executar com Docker

Requisitos: Docker Desktop instalado e aberto.

```bash
git clone https://github.com/wspgm1/Projetos.git
cd Projetos
git checkout develop
docker compose up --build
```

Depois abra:

- Sistema: http://localhost:3000
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

## Acesso inicial

- Usuário: `admin`
- Senha: `admin12345`

A senha acima é somente para desenvolvimento local. Antes de usar em produção, altere as credenciais e o JWT secret.

## O que já está funcionando

- Frontend web responsivo
- Login e logout
- JWT com expiração
- Revogação de token no logout
- Banco PostgreSQL persistente
- Usuários e perfis: admin, manager e employee
- Proteção das rotas da API
- Cadastro, listagem, alteração e desativação de usuários pelo administrador
- Dashboard inicial
- Estrutura preparada para Clientes, Produtos/Estoque, Vendas, Entregas e Financeiro

## Parar

```bash
docker compose down
```

Para apagar também o banco de desenvolvimento e começar do zero:

```bash
docker compose down -v
```
