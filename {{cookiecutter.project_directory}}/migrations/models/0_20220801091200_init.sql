-- upgrade --
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    "email" VARCHAR(50) NOT NULL UNIQUE,
    "password_hash" VARCHAR(128) NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_users_email_133a6f" ON "users" ("email");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
