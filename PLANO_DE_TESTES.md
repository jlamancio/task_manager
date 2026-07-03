# Plano de Testes — Task Manager (Back-end)

Este documento define a estratégia, escopo e as condições de teste para o
back-end do projeto, antes da implementação em Pytest.

---

## 1. Escopo desta rodada

**Camada testada:** Rotas (via `TestClient`), cobrindo o caminho completo
Rota → Service → Banco. Testes de Service isolado ficam como evolução futura
(ver seção 5 — Fora de Escopo).

**Framework:** Pytest, com `TestClient` do FastAPI.

**Isolamento de dados:** banco SQLite **em memória** (`sqlite:///:memory:`),
recriado a cada execução. Garante que os testes não dependem de estado deixado
por execuções anteriores, e não tocam o banco real (`task_manager.db`).

---

## 1.1 Nota terminológica

Este documento usa **Condição de Teste**, não "Cenário de Teste", seguindo a
nomenclatura formal da ISTQB/ISO 29119-1:

| Termo | Definição | Exemplo no projeto |
|---|---|---|
| **Condição de Teste** | Ideia resumida do que testar — texto simples, sem estrutura formal | "Deletar tarefa com `tarefa_id` inexistente" |
| **Caso de Teste** | Artefato detalhado derivado da condição: dados exatos, entradas, resultado esperado | `DELETE /v1/tarefas/9999` → 404, `{"detail": "Tarefa não encontrada"}` |

"Cenário de Teste" é um termo popular no mercado, mas sem fundamentação na
ISTQB/ISO 29119-1 — por isso evitado aqui, em favor de "Condição de Teste".

**Nota separada — BDD não é sinônimo de Gherkin:** BDD (Behavior-Driven
Development) é uma metodologia; Gherkin é uma sintaxe (`Dado/Quando/Então`)
usada para *praticar* BDD, geralmente executada por uma ferramenta como o
Cucumber. Dizer "escrevo testes em BDD" quando se quer dizer "escrevo
arquivos `.feature` em Gherkin" confunde o guarda-chuva metodológico com uma
ferramenta específica dentro dele. Este projeto não usa BDD/Gherkin no
back-end (Pytest puro); a mentoria paralela de Cypress + Cucumber é onde esse
par metodologia/sintaxe se aplica de fato.

---

## 2. Estratégia de cobertura de status code

Para cada rota relevante, cobrimos três categorias de resultado:

| Categoria | Significado | Quando ocorre |
|---|---|---|
| **200** | Sucesso | Requisição válida, recurso existe (quando aplicável) |
| **404** | Não encontrado | Operação em um `tarefa_id` que não existe no banco |
| **422** | Erro de validação | Corpo da requisição não passa a validação do Pydantic (campo obrigatório faltando, tipo errado, valor de Enum inválido) |

**Erros 500 não são testados como esperados.** Representam falha não tratada;
o objetivo dos testes é garantir que cenários problemáticos sempre caiam em
404 ou 422 de forma controlada, nunca em um 500 inesperado.

---

## 3. Matriz de Condições de Teste

### 3.1 GET /v1/tarefas/

| # | Condição de Teste | Código esperado | Status |
|---|---|---|---|
| G1 | Listar tarefas com banco vazio | 200 (lista vazia `[]`) | ✅ |
| G2 | Listar tarefas com 1 ou mais registros | 200 (lista com os registros) | ✅ |

### 3.2 POST /v1/tarefas/

| # | Condição de Teste | Código esperado | Status |
|---|---|---|---|
| P1 | Criar tarefa com todos os campos obrigatórios válidos | 200, retorna `id` gerado | ✅ |
| P2 | Criar tarefa sem `titulo` (campo obrigatório faltando) | 422 | ✅ |
| P3 | Criar tarefa sem `data_vencimento` (obrigatório desde a Sessão 5) | 422 | ✅ |
| P4 | Criar tarefa com `status` inválido (ex: `"feito"`, fora do Enum) | 422 | ✅ |
| P5 | Criar tarefa com `prioridade` inválida | 422 | ✅ |
| P6 | Criar tarefa sem enviar `id` | 200 | N/A — comportamento já garantido pela correção do schema (`id: int \| None = None`) |

### 3.3 PUT /v1/tarefas/{tarefa_id}

| # | Condição de Teste | Código esperado | Status |
|---|---|---|---|
| U1 | Atualizar tarefa existente com todos os campos válidos | 200, campos refletem o novo valor | ✅ |
| U2 | Atualizar tarefa com `tarefa_id` inexistente | 404 | ✅ |
| U3 | Atualizar tarefa existente sem `titulo` (obrigatório no schema `Tarefa`) | 422 | ✅ |
| U4 | Atualizar tarefa existente com `status` inválido | 422 | ✅ |

### 3.4 PATCH /v1/tarefas/{tarefa_id}

| # | Condição de Teste | Código esperado | Status |
|---|---|---|---|
| A1 | Atualizar parcialmente só um campo (ex: `status`) em tarefa existente | 200, **só** aquele campo muda | ✅ |
| A2 | Atualizar parcialmente vários campos ao mesmo tempo | 200, todos os campos enviados mudam | ✅ |
| A3 | Atualizar parcialmente com `tarefa_id` inexistente | 404 | ✅ |
| A4 | Enviar corpo vazio `{}` (nenhum campo) | 200, nenhum campo muda | ✅ |
| A5 | Enviar valor de Enum inválido (ex: `"em andamento"` com espaço) | 422 | ✅ |

### 3.5 DELETE /v1/tarefas/{tarefa_id}

| # | Condição de Teste | Código esperado | Status |
|---|---|---|---|
| D1 | Deletar tarefa existente | 200, mensagem de sucesso | ✅ |
| D2 | Deletar `tarefa_id` inexistente | 404 | ✅ |
| D3 | Deletar a mesma tarefa duas vezes (segunda chamada) | 200 na primeira, 404 na segunda | ✅ |

### 3.6 Condição de teste de integração (fluxo completo)

| # | Condição de Teste | Código esperado | Status |
|---|---|---|---|
| F1 | Criar → Listar (aparece) → Atualizar (PATCH) → Listar (mudança refletida) → Deletar → Listar (não aparece mais) | 200 em cada etapa, dado refletido corretamente | ✅ |

---

## 4. Estrutura de implementação

```
tests/
├── __init__.py
├── conftest.py          → fixtures: db_session, client, tarefa_criada
└── test_tarefas.py      → 19 casos de teste cobrindo toda a matriz
```

**Fixtures disponíveis em `conftest.py`:**

| Fixture | Tipo | O que entrega |
|---|---|---|
| `db_session` | `yield` | Sessão do banco SQLite em memória (recriado a cada teste) |
| `client` | `yield` | TestClient com dependency override do banco de teste |
| `tarefa_criada` | `return` | JSON da tarefa criada via POST (para testes que precisam de dado existente) |

---

## 5. Fora de Escopo (nesta rodada)

- **Testes de Service isolado** (sem passar pela rota) — possível evolução
  futura, não necessária agora.
- **Testes de autenticação/autorização** — dependem da fase de Autenticação
  (JWT), planejada como etapa própria antes do front-end.
- **Testes de carga/performance** — fora do propósito de aprendizado atual.
- **Testes de concorrência** (múltiplas requisições simultâneas) — mesmo
  motivo.

---

## 6. Resultado final

**19 testes implementados, 19 passando — 100% da matriz coberta.**

```
19 passed in 0.24s
```

Condições notáveis identificadas durante a implementação:
- `data_criacao` estava obrigatório no schema (422 inesperado no POST) — corrigido para `datetime | None = None`
- `StaticPool` necessário para SQLite em memória — sem ele, `create_all()` e a sessão usam conexões diferentes
- Pydantic valida **antes** da consulta ao banco — 422 tem precedência sobre 404 quando ambos poderiam ocorrer
- Teste passando com assert ausente é falso positivo — todo teste precisa de pelo menos um `assert`
