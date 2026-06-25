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
| Testes back-end | Pytest | 8.3.5 |
| Testes front-end | Cypress | A definir no setup front-end |
| Servidor | Uvicorn | 0.34.3 |
| Ambiente | Node.js + npm | Node 22.22.3 / npm 10.9.8 |
| Clientes de API | Postman / Insomnia | A mais atual |
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

## Estrutura do Projeto

```
task_manager/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   └── tarefas.py          → rotas (GET, POST, PUT, PATCH, DELETE) — só orquestra
│   ├── services/
│   │   └── tarefa_service.py   → regras de negócio: busca, criação, atualização, remoção
│   └── models/
│       ├── tarefa.py           → Schema Pydantic (contrato da API) + TarefaPatch
│       └── tarefa_db.py        → Modelo ORM SQLAlchemy (tabela real)
├── database/
│   ├── db.py                   → Engine, Session, Base e get_db() (Dependency Injection)
│   └── task_manager.db         → arquivo do banco SQLite
├── tests/                       → testes automatizados com Pytest
├── venv/                        → ambiente virtual (não vai para o GitHub)
├── start.sh                     → script para subir a API
├── .gitignore
├── requirements.txt             → dependências com versões travadas
├── README.md
├── GUIDE.md                     → diário técnico do projeto
└── CONCEITOS.md                 → glossário de consulta rápida (uso pessoal)
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

**Front-end:** testes seguem o padrão Page Object Model (POM) com Cypress.

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
- [ ] Testes automatizados com Pytest
- [ ] Etapa 2 — Front-end: Páginas + Testes (Cypress)

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
- Pytest: https://docs.pytest.org
- Postman: https://www.postman.com
- Insomnia: https://insomnia.rest
- DB Browser for SQLite: https://sqlitebrowser.org
- Git: https://git-scm.com
- GitHub: https://github.com
