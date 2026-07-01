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

Seguindo a terminologia formalmente reconhecida pela ISTQB/ISO 29119-1: o que
está listado abaixo são **Condições de Teste** — a ideia resumida do que
testar. Cada linha será detalhada como um **Caso de Teste** na implementação
(seção 4), com dados concretos, payload exato e assert exato. "Cenário de
Teste" é um termo popular, sem fundamentação formal nesses padrões, e por
isso evitado neste documento.

### 3.1 GET /v1/tarefas/

| # | Condição de Teste | Código esperado | Status |
|---|---|---|---|
| G1 | Listar tarefas com banco vazio | 200 (lista vazia `[]`) | ✅ implementado (29/06) |
| G2 | Listar tarefas com 1 ou mais registros | 200 (lista com os registros) | ⏳ pendente |

### 3.2 POST /v1/tarefas/

| # | Condição de Teste | Código esperado |
|---|---|---|
| P1 | Criar tarefa com todos os campos obrigatórios válidos | 200, retorna `id` gerado |
| P2 | Criar tarefa sem `titulo` (campo obrigatório faltando) | 422 |
| P3 | Criar tarefa sem `data_vencimento` (obrigatório desde a Sessão 5) | 422 |
| P4 | Criar tarefa com `status` inválido (ex: `"feito"`, fora do Enum) | 422 |
| P5 | Criar tarefa com `prioridade` inválida | 422 |
| P6 | Criar tarefa sem enviar `id` (deve funcionar — `id` é opcional/gerado) | 200 |

### 3.3 PUT /v1/tarefas/{tarefa_id}

| # | Condição de Teste | Código esperado |
|---|---|---|
| U1 | Atualizar tarefa existente com todos os campos válidos | 200, campos refletem o novo valor |
| U2 | Atualizar tarefa com `tarefa_id` inexistente | 404 |
| U3 | Atualizar tarefa existente sem `titulo` (obrigatório no schema `Tarefa`) | 422 |
| U4 | Atualizar tarefa existente com `status` inválido | 422 |

### 3.4 PATCH /v1/tarefas/{tarefa_id}

| # | Condição de Teste | Código esperado |
|---|---|---|
| A1 | Atualizar parcialmente só um campo (ex: `status`) em tarefa existente | 200, **só** aquele campo muda |
| A2 | Atualizar parcialmente vários campos ao mesmo tempo | 200, todos os campos enviados mudam |
| A3 | Atualizar parcialmente com `tarefa_id` inexistente | 404 |
| A4 | Enviar corpo vazio `{}` (nenhum campo) | 200, nenhum campo muda |
| A5 | Enviar valor de Enum inválido (ex: `"em andamento"` com espaço) | 422 |

### 3.5 DELETE /v1/tarefas/{tarefa_id}

| # | Condição de Teste | Código esperado |
|---|---|---|
| D1 | Deletar tarefa existente | 200, mensagem de sucesso |
| D2 | Deletar `tarefa_id` inexistente | 404 |
| D3 | Deletar a mesma tarefa duas vezes (segunda chamada) | 200 na primeira, 404 na segunda |

### 3.6 Condição de teste de integração (fluxo completo)

| # | Condição de Teste | Código esperado |
|---|---|---|
| F1 | Criar → Listar (aparece) → Atualizar (PATCH) → Listar (mudança refletida) → Deletar → Listar (não aparece mais) | 200 em cada etapa, dado refletido corretamente a cada passo |

---

## 4. Estrutura de implementação prevista

```
tests/
├── __init__.py
├── conftest.py          → fixtures compartilhadas (banco em memória, TestClient)
└── test_tarefas.py       → os casos de teste da matriz acima
```

`conftest.py` é o arquivo onde o Pytest procura fixtures automaticamente,
sem precisar de import explícito em cada arquivo de teste.

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

## 6. Critério de conclusão desta fase

Considera-se esta fase de testes concluída quando:
- Todos os cenários da Matriz (seção 3) estiverem implementados e passando.
- `pytest` executado na raiz do projeto retornar sucesso para 100% dos casos.
- O resultado for registrado no `GUIDE.md`, incluindo eventuais bugs reais
  encontrados durante a escrita dos testes (como já ocorreu antes com a
  inconsistência de `data_vencimento`).
