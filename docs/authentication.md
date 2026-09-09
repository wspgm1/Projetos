# Autenticação e autorização

## Perfis

- `admin`: administração completa de usuários e sistema.
- `manager`: perfil de gestão; poderá acessar módulos administrativos conforme as regras de cada módulo.
- `employee`: usuário operacional; acesso somente às rotas permitidas pelo módulo.

## Fluxo

1. `POST /auth/login` recebe usuário e senha.
2. A API valida a senha contra o hash armazenado.
3. Um JWT é emitido com `sub`, `role`, `iat`, `exp` e `jti`.
4. O frontend envia `Authorization: Bearer <token>`.
5. `current_user` valida assinatura, expiração, existência do usuário, status ativo e revogação do `jti`.
6. Dependências como `admin_required` aplicam autorização por perfil.
7. `POST /auth/logout` grava o `jti` na tabela `revoked_tokens`, invalidando o token antes do vencimento.

## Endpoints

- `POST /auth/login` — entrar.
- `POST /auth/logout` — sair e revogar o token atual.
- `GET /auth/me` — usuário autenticado.
- `POST /auth/users` — criar usuário (admin).
- `GET /auth/users` — listar usuários (admin).
- `PATCH /auth/users/{user_id}` — alterar usuário (admin).
- `DELETE /auth/users/{user_id}` — desativar usuário (admin).

## Segurança

- Senhas são armazenadas somente como hash Argon2 via `pwdlib`.
- Nunca versionar `.env` ou segredos reais.
- Usar uma chave JWT forte e exclusiva em produção.
- Usar HTTPS em produção.
- O logout é implementado por revogação do `jti`; tokens já emitidos não devem ser reutilizados depois do logout.
