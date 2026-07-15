# Task Manager

Sistema de gerenciamento de tarefas com API back-end e front-end, com cobertura de testes em ambas as camadas.

GitHub: https://github.com/jlamancio/task_manager

---

## Tecnologias

| Camada | Tecnologia | Versão |
|---|---|---|
| Back-end | Python + FastAPI | Python 3.12.9 / FastAPI 0.115.14 |
| Banco de dados | SQLite + SQLAlchemy | SQLAlchemy 2.0.36 |
| Front-end | HTML + CSS + JavaScript puro | - |
| Testes back-end | Pytest + httpx (TestClient) | Pytest 8.3.5 / httpx 0.27.0 |
| Testes front-end | Cypress + Cucumber (Gherkin) | Cypress 15.18.1 / @badeball/cypress-cucumber-preprocessor ^26.0.0 |
| Servidor | Uvicorn | 0.34.3 |
| Ambiente | Node.js + npm | Node 22.22.3 / npm 10.9.8 |
| Clientes de API | Postman / Insomnia | - |
| Inspeção de banco | DB Browser for SQLite | 3.13.0 |
| Versionamento | Git + GitHub | Git 2.51.0 |

> Todas as versões estão travadas com `==` no requirements.txt. O package.json não utilizará `^` ou `~`.

---

## Pré-requisitos

- Python 3.12+: https://www.python.org/downloads
- Node.js LTS: https://nodejs.org/en/download
- Git: https://git-scm.com/downloads
- Postman: https://www.postman.com/downloads
- Insomnia: https://insomnia.rest/download
- DB Browser for SQLite: https://sqlitebrowser.org/dl/

### Validação do ambiente

```bash
python --version
pip --version
node -v
npm -v
git --version
```

---

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/jlamancio/task_manager.git
cd task_manager
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv venv
source venv/Scripts/activate
```

> No Windows com Git Bash use `source venv/Scripts/activate`.
> No Mac/Linux use `source venv/bin/activate`.

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

---

## Subindo a API

A forma recomendada é usando o script `start.sh`, que ativa o ambiente virtual e sobe o servidor em um único comando:

```bash
./start.sh
```

Se o arquivo não tiver permissão de execução, rode uma vez:

```bash
chmod +x start.sh
```

**Alternativa manual** (equivalente ao que o script faz):

```bash
source venv/Scripts/activate
uvicorn main:app --reload
```

Depois de subir, acesse:
- API: http://127.0.0.1:8000
- Documentação interativa (Swagger/OpenAPI): http://127.0.0.1:8000/docs

---

## Subindo o front-end

O front-end (`frontend/`) é HTML/CSS/JS puro — não tem build nem
dependência própria. Basta servir a pasta com um servidor estático
enquanto a API estiver rodando (ex: extensão Live Server do VS Code,
clicando com o botão direito em `frontend/login.html` → "Open with Live
Server").

Fluxo: `cadastro.html` (criar conta) → `login.html` (autenticar) →
`index.html` (CRUD de tarefas).

---

## Rodando os testes

### Back-end (Pytest)

Os testes usam um banco SQLite em memória, isolado do banco real
(`task_manager.db`) — não é necessário a API estar rodando.

```bash
python -m pytest -v
```

36 testes no total (auth + CRUD de tarefas). Ver `PLANO_DE_TESTES.md` e
`PLANO_DE_TESTES_AUTH.md` para a matriz completa de condições planejadas.

### End-to-end (Cypress + Cucumber)

Requer a API **e** o front-end rodando (ver seções acima).

```bash
npx cypress open      # interface gráfica, um spec por vez
npx cypress run       # modo headless, todos os specs
```

16 cenários no total, em Gherkin/português, cobrindo login, cadastro e
CRUD de tarefas. Ver `GUIDE.md` (Sessões 12–14) para a tabela de decisão
de cobertura e o processo de construção dos testes.

---

## Estrutura do Projeto

```
task_manager/
├── app/
│   ├── __init__.py
│   ├── dependencies.py         → get_current_user (dependência de autenticação JWT)
│   ├── routes/
│   │   ├── tarefas.py          → rotas (GET, POST, PUT, PATCH, DELETE) — só orquestra
│   │   └── auth.py             → rotas de cadastro e login
│   ├── services/
│   │   ├── tarefa_service.py   → regras de negócio: busca, criação, atualização, remoção
│   │   └── auth_service.py     → hash de senha, criação/validação de token JWT
│   └── models/
│       ├── tarefa.py           → Schema Pydantic (contrato da API) + TarefaPatch
│       ├── tarefa_db.py        → Modelo ORM SQLAlchemy (tabela real)
│       ├── usuario.py          → Schema Pydantic de usuário
│       └── usuario_db.py       → Modelo ORM SQLAlchemy de usuário
├── database/
│   ├── db.py                   → Engine, Session, Base e get_db() (Dependency Injection)
│   └── task_manager.db         → arquivo do banco SQLite (não versionado)
├── frontend/
│   ├── index.html              → lista/CRUD de tarefas (tela principal)
│   ├── login.html
│   ├── cadastro.html
│   ├── css/style.css
│   └── js/
│       ├── api.js              → camada de integração com a API
│       ├── index.js / login.js / cadastro.js  → lógica de cada página
├── tests/                       → testes automatizados com Pytest
├── cypress/
│   └── e2e/                    → testes E2E: *.feature (Gherkin) + step_definitions/
├── docs/
│   ├── GUIDE.md                 → diário técnico do projeto, sessão a sessão
│   ├── HISTORICO_INCIDENTE_GIT.md → incidentes reais de Git, documentados em detalhe
│   ├── LICOES_APRENDIDAS.md    → checklist de atenção para o próximo projeto
│   ├── CONCEITOS.md            → glossário de consulta rápida (uso pessoal)
│   └── PLANO_DE_TESTES*.md, ARCHITECTURE.md, REFERENCIA_COMANDOS.md
├── venv/                        → ambiente virtual (não vai para o GitHub)
├── start.sh                     → script para subir a API
├── cypress.config.js
├── package.json
├── .gitignore
├── requirements.txt             → dependências com versões travadas
└── README.md
```

---

## Arquitetura

**Back-end — Arquitetura em Camadas:**

| Camada | Responsabilidade |
|---|---|
| Routes | Recebe as requisições |
| Services | Contém as regras de negócio |
| Models (Schema) | Valida o formato dos dados da API (Pydantic) |
| Models (ORM) | Representa a tabela real no banco (SQLAlchemy) |

**Front-end:** testes E2E com Cypress + Cucumber — cenários escritos em
Gherkin/português (`.feature`), cada frase ligada a uma função JavaScript
em `step_definitions/`. (O plano inicial previa Page Object Model puro;
na prática, o preprocessador do Cucumber cobriu essa necessidade de
organização de forma mais direta, então esse foi o padrão adotado.)

**Banco de dados:** SQLite, acessado via SQLAlchemy (ORM). Pode ser inspecionado visualmente com o DB Browser for SQLite, abrindo `database/task_manager.db`.

---

## Etapas

- [x] Definição de escopo e stack
- [x] Criação do repositório e README
- [x] Etapa 0 — Setup do ambiente
- [x] Primeira rota da API (Tarefas) com armazenamento em memória
- [x] Conexão com SQLite via SQLAlchemy (Engine, Session, modelo ORM)
- [x] Conectar rotas ao banco real via Dependency Injection
- [x] CRUD completo (GET, POST, PUT, PATCH, DELETE)
- [x] Camada de Services (lógica de negócio fora das rotas)
- [x] Validação cruzada via Swagger e Postman
- [x] Testes automatizados com Pytest — 36 testes (auth + CRUD de tarefas)
- [x] Autenticação (JWT) — cadastro, login, proteção das rotas
- [x] Correção dos testes de tarefas (quebrados após proteção com JWT)
- [x] Front-end — 3 páginas (login, cadastro, index) com estética
      azul-acinzentada, integradas à API via `api.js`
- [x] CORS configurado para integração front-end (porta 5500) + API
      (porta 8000)
- [x] Testes E2E com Cypress + Cucumber — 16 cenários (login, cadastro,
      CRUD de tarefas)
- [x] Bug real encontrado via teste automatizado (título vazio aceito
      pela API) e corrigido em duas camadas (JS + Pydantic)
- [x] Documentação de incidentes reais de Git (`HISTORICO_INCIDENTE_GIT.md`)
- [x] Lições aprendidas registradas para o próximo projeto
      (`LICOES_APRENDIDAS.md`)
- [x] **Projeto encerrado** — pendências remanescentes avaliadas e
      mantidas como decisões conscientes de escopo (ver seção abaixo)

---

## Decisões e limitações conhecidas

Registradas conscientemente ao final do projeto — não são pendências
esquecidas:

- Não existe rota `GET /{tarefa_id}` — o front-end reaproveita os dados
  já carregados pela listagem para a tela de edição.
- `SECRET_KEY` do JWT está fixa no código (`auth_service.py`) — aceitável
  para projeto local de portfólio; em produção real seria variável de
  ambiente (ver `LICOES_APRENDIDAS.md`).
- O CRUD de tarefas não é multiusuário de fato — qualquer usuário
  autenticado acessa e edita as tarefas de todos.
- 3 vulnerabilidades reportadas por `npm audit` (internas ao `mocha`,
  dependência transitiva do Cypress) mantidas sem correção forçada —
  risco de quebrar a ferramenta de teste maior que o benefício, para
  uma dependência de desenvolvimento local.

---

## Referências

- Python: https://www.python.org
- FastAPI: https://fastapi.tiangolo.com
- SQLite: https://sqlite.org
- SQLAlchemy: https://www.sqlalchemy.org
- JavaScript: https://developer.mozilla.org/pt-BR/docs/Web/JavaScript
- Node.js: https://nodejs.org
- npm: https://www.npmjs.com
- ECMAScript: https://ecma-international.org
- Cypress: https://www.cypress.io
- Cucumber (Gherkin): https://cucumber.io/docs/gherkin
- Pytest: https://docs.pytest.org
- Postman: https://www.postman.com
- Insomnia: https://insomnia.rest
- DB Browser for SQLite: https://sqlitebrowser.org
- Git: https://git-scm.com
- GitHub: https://github.com
