# Arquitetura inicial

## Autenticação
1. Cliente envia `username` e `password` para `POST /auth/login`.
2. A API procura o usuário no PostgreSQL.
3. A senha é comparada com um hash Argon2; a senha original não é armazenada.
4. Em caso de sucesso, a API cria um JWT assinado com validade configurável.
5. O cliente envia `Authorization: Bearer <token>` nas próximas requisições.
6. `current_user` valida assinatura/expiração, identifica o usuário e bloqueia tokens inválidos.
7. `GET /auth/me` demonstra uma rota protegida.

## Segurança
- Não colocar `.env` no Git.
- Em produção, substituir imediatamente os valores de desenvolvimento por segredos fortes.
- Não armazenar senhas em texto puro.
- HTTPS deve ser obrigatório em produção.
