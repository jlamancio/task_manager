# Plano de Testes — Lacunas (Front-end, E2E, Service Layer)

Este documento complementa `PLANO_DE_TESTES.md` (CRUD de Tarefas) e
`PLANO_DE_TESTES_AUTH.md` (Autenticação), ambos com 100% da matriz de rotas
coberta. Aqui o foco são as áreas explicitamente registradas como "Fora de
Escopo" nesses dois documentos, mais duas áreas sem nenhuma cobertura hoje:
front-end (JS) e E2E (Cypress).

---

## 1. Pirâmide de testes aplicada ao projeto

| Camada | Estado atual | Ferramenta |
|---|---|---|
| Unit (service isolado, JS puro) | Não existe | A definir (pytest / Vitest ou Jest) |
| Integration (rota → service → banco) | 100% coberto | Pytest + `TestClient` |
| E2E (fluxo completo no navegador) | Configurado, sem specs | Cypress (+ cucumber já no `package.json`) |

---

## 2. Áreas e estratégia

### 2.1 Service layer isolado (Python) — 0% hoje

Hoje os testes cobrem rota + service + banco juntos via `TestClient`. Um bug
de lógica pura no service (hash de senha, geração de token, regra de negócio)
só é pego indiretamente, através do resultado HTTP.

**Cobertura alvo:** `app/services/auth_service.py` (`criar_usuario`,
`verificar_senha`, `criar_token`) e `app/services/tarefa_service.py`
(todas as funções), chamadas diretamente, sem passar pela rota.

**Casos de exemplo:**

| Condição de Teste | Resultado esperado |
|---|---|
| `criar_token` com `expires_delta` negativo | Token já expirado ao decodificar |
| `verificar_senha` com hash corrompido/inválido | Retorna `False`, não lança exceção |
| `create_tarefa` com dados válidos | Grava no banco com `id` auto-incrementado |

### 2.2 Front-end JS (`frontend/js/*.js`) — 0% hoje

Não há test runner configurado — o script `test` do `package.json` é só um
placeholder (`"echo \"Error: no test specified\" && exit 1"`).

**Recomendação:** Vitest (mais leve, já compatível com o ESBuild usado pelo
preprocessor do Cypress) com jsdom para simular `localStorage` e `fetch`.

**Cobertura alvo:** funções de `api.js` (wrappers de `fetch`) e a lógica de
manipulação de DOM em `login.js` / `cadastro.js` / `index.js`, com `fetch`
mockado.

**Casos de exemplo:**

| Condição de Teste | Resultado esperado |
|---|---|
| `salvarToken` / `getToken` / `removeToken` | Leem e escrevem corretamente em `localStorage` |
| `login()` | Envia `form-urlencoded` com `username`/`password` (não JSON) |
| `logout()` | Limpa o token e redireciona para `login.html` |

### 2.3 E2E (Cypress) — configurado, sem specs

`cypress.config.js`, `cypress/fixtures` e `cypress/support` já existem, e o
`package.json` já tem `cypress-cucumber-preprocessor`, sugerindo intenção de
escrever os testes em Gherkin. A pasta `cypress/e2e` ainda não tem nenhum
arquivo `.feature` ou spec.

**Cobertura alvo — poucos fluxos, de alto valor:**

| Condição de Teste | Resultado esperado |
|---|---|
| Cadastro → Login → Criar tarefa → Editar → Concluir → Deletar → Logout | Cada etapa reflete corretamente na tela |
| Acessar `index.html` sem estar logado | Redireciona para `login.html` |
| Login com credenciais inválidas | Mensagem de erro visível, sem redirecionar |

### 2.4 Itens já registrados como "Fora de Escopo" nos planos existentes

Continuam fora desta rodada, mas ficam registrados aqui para rastreabilidade:

- Refresh token / logout no back-end (hoje o logout só limpa o token no front-end)
- Autorização por perfil (admin/usuário) — schema atual não tem campo de role
- Rate limiting
- Testes de carga e concorrência

---

## 3. Metas de cobertura sugeridas

- **Service layer:** 90%+ das funções públicas
- **Front-end JS:** 100% das funções de `api.js` (poucas e críticas); a lógica de DOM fica coberta principalmente via E2E
- **E2E:** os 3 fluxos críticos da seção 2.3, antes de qualquer expansão

---

## 4. Ordem de implementação recomendada

1. **Service layer isolado** — reaproveita as fixtures já existentes em `conftest.py`, menor esforço
2. **E2E dos 3 fluxos críticos** — Cypress já está configurado; é a maior lacuna de risco real hoje (nenhum teste toca o front-end)
3. **Front-end unit** — menor prioridade, já que o E2E cobre boa parte do comportamento observável
