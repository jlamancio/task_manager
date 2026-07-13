# Plano de Testes — Autenticação (Back-end)

Este documento define as condições de teste para a fase de Autenticação,
complementando o `PLANO_DE_TESTES.md` original (que cobria só o CRUD de Tarefas).

---

## 1. Escopo

**Camada testada:** Rotas de autenticação (`/auth/cadastro`, `/auth/login`) e
proteção das rotas de tarefas via token JWT.

**Framework:** Pytest, com `TestClient` do FastAPI.

**Isolamento de dados:** banco SQLite em memória (`sqlite:///:memory:`),
recriado a cada teste — mesmo padrão já adotado nos testes de Tarefas.

---

## 2. Estratégia de cobertura

| Categoria | Códigos cobertos |
|---|---|
| Sucesso | 200 |
| Credenciais inválidas | 401 |
| Email duplicado | 400 |
| Campos faltando/inválidos | 422 |

---

## 3. Matriz de Condições de Teste

### 3.1 POST /auth/cadastro

| # | Condição de Teste | Código esperado | Status |
|---|---|---|---|
| C1 | Cadastrar usuário com email e senha válidos | 200 — retorna `id` e `email` (sem senha_hash) | ⏳ |
| C2 | Cadastrar com email já existente | 400 — "Email já cadastrado" | ⏳ |
| C3 | Cadastrar sem `email` | 422 | ⏳ |
| C4 | Cadastrar sem `senha` | 422 | ⏳ |

### 3.2 POST /auth/login

| # | Condição de Teste | Código esperado | Status |
|---|---|---|---|
| L1 | Login com credenciais válidas | 200 — retorna `access_token` e `token_type` | ⏳ |
| L2 | Login com email inexistente | 401 — "Email ou senha inválidos" | ⏳ |
| L3 | Login com senha incorreta | 401 — "Email ou senha inválidos" | ⏳ |
| L4 | Login sem `username` | 422 | ⏳ |
| L5 | Login sem `password` | 422 | ⏳ |

### 3.3 Proteção das rotas de Tarefas

| # | Condição de Teste | Código esperado | Status |
|---|---|---|---|
| P1 | Acessar GET /v1/tarefas/ sem token | 401 — "Not authenticated" | ⏳ |
| P2 | Acessar GET /v1/tarefas/ com token válido | 200 | ⏳ |
| P3 | Acessar GET /v1/tarefas/ com token inválido (adulterado) | 401 — "Token inválido" | ⏳ |
| P4 | Acessar GET /v1/tarefas/ com token expirado | 401 — "Token inválido" | ⏳ |

### 3.4 Segurança

| # | Condição de Teste | Código esperado | Status |
|---|---|---|---|
| S1 | Verificar que `senha_hash` não aparece na resposta do cadastro | 200 — resposta só tem `id` e `email` | ⏳ |
| S2 | Verificar que a mensagem de erro é genérica no login (não revela se é email ou senha incorretos) | 401 — mesma mensagem para email inexistente e senha incorreta | ⏳ |

---

## 4. Observações técnicas

**C2 — Email duplicado:**
O banco tem `unique=True` no campo `email` da tabela `usuarios`. O teste
precisa cadastrar um usuário via POST antes de tentar cadastrar outro com
o mesmo email.

**L1 — Formato do login:**
A rota `/auth/login` usa `OAuth2PasswordRequestForm` — os campos se chamam
`username` e `password` (padrão OAuth2), não `email` e `senha`. O TestClient
precisa enviar no formato de formulário, não JSON:

```python
resposta = client.post("/auth/login", data={
    "username": "usuario@teste.com",
    "password": "123456"
})
```

**P3 — Token adulterado:**
Basta passar qualquer string inválida no header de autorização:
```python
headers = {"Authorization": "Bearer token_invalido_qualquer"}
resposta = client.get("/v1/tarefas/", headers=headers)
```

**P4 — Token expirado:**
O mais complexo — requer gerar um token com expiração no passado.
Solução: chamar `criar_token` diretamente com `timedelta(minutes=-1)`:

```python
from app.services.auth_service import criar_token
from datetime import timedelta

token_expirado = criar_token({"sub": "usuario@teste.com"}, expires_delta=timedelta(minutes=-1))
```

> Isso requer um pequeno ajuste na função `criar_token` para aceitar
> `expires_delta` como parâmetro opcional.

**S2 — Mensagem genérica:**
Propositalmente, a API retorna "Email ou senha inválidos" tanto para email
inexistente quanto para senha incorreta — não revela qual dos dois está errado,
dificultando ataques de enumeração de usuários.

---

## 5. Fixture necessária

Os testes C2, L1, L2, L3, P2, P3, P4 e S1 precisam de um usuário já cadastrado
no banco antes de rodar. Criar fixture `usuario_cadastrado` no `conftest.py`:

```python
@pytest.fixture
def usuario_cadastrado(client):
    resposta = client.post("/auth/cadastro", json={
        "email": "teste@teste.com",
        "senha": "123456"
    })
    return resposta.json()
```

Para testes que precisam do token (P2, P3, P4):

```python
@pytest.fixture
def token_valido(client, usuario_cadastrado):
    resposta = client.post("/auth/login", data={
        "username": "teste@teste.com",
        "password": "123456"
    })
    return resposta.json()["access_token"]
```

---

## 6. Fora de Escopo (nesta rodada)

- Testes de refresh token — não implementado
- Testes de logout — não implementado
- Testes de autorização por perfil (admin/usuário) — não implementado
- Testes de rate limiting — fora do propósito de aprendizado atual

---

## 7. Critério de conclusão

Considera-se esta fase de testes concluída quando:
- Todas as 14 condições de teste estiverem implementadas e passando
- `pytest` retornar sucesso para 100% dos casos
- Resultado registrado no `GUIDE.md`
