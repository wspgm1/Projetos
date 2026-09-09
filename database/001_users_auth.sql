-- Migração inicial de usuários e revogação de tokens.
-- Execute em instalações existentes; em bancos novos o SQLAlchemy também cria as tabelas.

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(120) NOT NULL DEFAULT '',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    role VARCHAR(30) NOT NULL DEFAULT 'employee',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_users_username ON users(username);
CREATE INDEX IF NOT EXISTS ix_users_role ON users(role);

CREATE TABLE IF NOT EXISTS revoked_tokens (
    id SERIAL PRIMARY KEY,
    jti VARCHAR(64) NOT NULL UNIQUE,
    expires_at TIMESTAMP NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS ix_revoked_tokens_jti ON revoked_tokens(jti);
CREATE INDEX IF NOT EXISTS ix_revoked_tokens_expires_at ON revoked_tokens(expires_at);
CREATE INDEX IF NOT EXISTS ix_revoked_tokens_user_id ON revoked_tokens(user_id);
