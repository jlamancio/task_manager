# GUIDE — Diário Técnico do Projeto Task Manager

Este arquivo registra as atividades desenvolvidas em cada sessão do projeto,
servindo como material de referência e estudo.

---

## Sessão 1 — Setup do Ambiente
**Data:** 15/06/2025
**Branch:** feature/setup_do_projeto

### Resumo

| Atividade | Status |
|---|---|
| Mapeamento do ambiente | ✅ |
| Definição e escolha de versões | ✅ |
| Criação do ambiente virtual | ✅ |
| Instalação das dependências | ✅ |
| Geração do requirements.txt | ✅ |
| Estrutura de pastas criada | ✅ |
| Arquivos __init__.py criados | ✅ |
| .gitignore configurado | ✅ |
| Primeiro commit e push | ✅ |

---

## Sessão 2 — Primeira Rota da API (Tarefas)
**Branch:** feature/backend

Modelagem da entidade Tarefa, criação do schema Pydantic (`app/models/tarefa.py`)
e das rotas GET/POST (`app/routes/tarefas.py`), conectadas ao `main.py`.
Armazenamento temporário em lista Python (`tarefas_db = []`), sem persistência real.

**Problemas resolvidos:** erro de import no VS Code (interpretador errado),
`event not found` no Bash (`!` dentro de aspas duplas), rota duplicada por
prefixo repetido, rotas não aparecendo por falta de `include_router`, e erro de
sintaxe no Enum (`status: StatusTarefa.pendente` sem o `=`).

### Resumo

| Atividade | Status |
|---|---|
| Modelagem da entidade Tarefa | ✅ |
| Criação do schema Pydantic | ✅ |
| Criação das rotas GET e POST | ✅ |
| Conexão das rotas ao main.py | ✅ |
| Testes manuais via Swagger | ✅ |

---

## Sessão 3 — Conexão com SQLite via SQLAlchemy
**Branch:** feature/backend

---

### 3.1 Conceito-chave: Schema vs Modelo ORM

Antes de codar, estabelecemos a diferença entre dois modelos que representam
a mesma entidade (Tarefa), mas com papéis distintos:

| Modelo | Onde vive | Papel | Biblioteca | Quando existe |
|---|---|---|---|---|
| **Schema** | `app/models/tarefa.py` | Define o formato dos dados da **API** | Pydantic | Só durante a requisição |
| **Modelo ORM** | `app/models/tarefa_db.py` | Define a **tabela real** no banco | SQLAlchemy | Sempre — é a tabela persistida |

**Analogia usada:** o schema é como a planta arquitetônica de uma casa (mostra
o layout para quem visita); o modelo ORM é a fundação e estrutura real (existe
independente de haver visita ou não). Mudar a "pintura" (schema) não exige
reforçar a "fundação" (tabela), e vice-versa.

---

### 3.2 Instalação do SQLAlchemy

Consultamos a versão estável antes de instalar, seguindo o mesmo critério já
usado para FastAPI, Uvicorn e Pytest (série madura, bem testada).

**Versão escolhida:** SQLAlchemy 2.0.36 (série 2.0.x, sintaxe moderna, compatível
com Python 3.12 e FastAPI 0.115.14).

```bash
pip install sqlalchemy==2.0.36
pip freeze > requirements.txt
```

> A instalação trouxe a dependência `greenlet` automaticamente — usada
> internamente pelo SQLAlchemy para suportar operações assíncronas.

**Regra reforçada:** sempre que uma dependência é instalada ou removida, repetir
`pip freeze > requirements.txt` para manter o arquivo fiel ao ambiente real.

---

### 3.3 Configuração da Conexão (Engine, Session, Base)

Criada a pasta `database/` com seu próprio `__init__.py`, e o arquivo de
configuração central:

```python
# database/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./database/task_manager.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

**Conceitos:**
- `Engine` — sabe como conversar com o banco (tipo, caminho do arquivo).
- `SessionLocal` — "fábrica" de sessões, usada para ler/escrever dados.
- `Base` — classe-base da qual todo modelo ORM herda, conectando classes
  Python a tabelas reais.
- `connect_args={"check_same_thread": False}` — necessário porque o SQLite
  por padrão restringe o uso a uma única thread, mas o FastAPI atende
  requisições em paralelo.

Validação:
```bash
python -c 'from database.db import engine, SessionLocal, Base; print("Conexão configurada com sucesso!")'
```

---

### 3.4 Criação do Modelo ORM

```python
# app/models/tarefa_db.py
from sqlalchemy import Column, Integer, String, DateTime, Date

from database.db import Base


class TarefaDB(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    status = Column(String, default="pendente", nullable=False)
    prioridade = Column(String, default="media", nullable=False)
    data_criacao = Column(DateTime, nullable=False)
    data_vencimento = Column(Date, nullable=True)
```

**Decisões tomadas:**
- Nome `TarefaDB` (não `Tarefa`) para não colidir com o schema Pydantic já
  existente — convenção comum de mercado (sufixo `DB` ou `Model`).
- `status` e `prioridade` armazenados como `String` simples no banco, mesmo
  sendo `Enum` no schema da API — simplificação válida neste estágio de
  aprendizado. SQLAlchemy suporta Enum nativo, fica como evolução futura.
- `primary_key=True` + `index=True` na coluna `id`.
- `nullable=True/False` equivale ao `str | None` do Pydantic.

Validação:
```bash
python -c 'from app.models.tarefa_db import TarefaDB; print("Modelo ORM carregado com sucesso!")'
```

---

### 3.5 Criação da Tabela no Banco

```bash
python -c 'from database.db import Base, engine; from app.models.tarefa_db import TarefaDB; Base.metadata.create_all(bind=engine); print("Tabela criada com sucesso!")'
```

Resultado: arquivo `database/task_manager.db` criado (12.288 bytes), com a
tabela `tarefas` e o índice `ix_tarefas_id` (gerado por `index=True`).

---

### 3.6 Inspeção Visual com DB Browser for SQLite

**Conceito:** ferramenta gráfica open source para abrir e inspecionar arquivos
`.db` do SQLite, sem precisar escrever código.

Instalado a partir de https://sqlitebrowser.org/dl/ (versão 3.13.0, win64).

**Uso no projeto:** abrir `database/task_manager.db` → aba "Database Structure"
para confirmar visualmente o que o SQLAlchemy criou. Aba "Browse Data" permite
ver as linhas salvas, útil para conferir os testes feitos via Swagger.

**Regra importante estabelecida:** criar uma tabela manualmente pela interface
do DB Browser não basta — o SQLAlchemy só reconhece tabelas que tenham um
modelo ORM correspondente declarado em Python. As duas formas (interface e
código) precisam estar sincronizadas; a interface serve para inspecionar e
rascunhar visualmente, mas a criação "oficial" continua vindo do código.

Confirmado visualmente: esquema da tabela
`CREATE TABLE tarefas (id INTEGER NOT NULL, titulo VARCHAR NOT NULL, descricao VARCHAR, status VARCHAR...)`
e o índice `ix_tarefas_id ON tarefas (id)`.

---

### 3.7 Script de Automação — start.sh

**Conceito:** script que agrupa comandos repetitivos (ativar venv + subir o
servidor) em um único comando executável.

```bash
# start.sh
#!/bin/bash
echo "Ativando ambiente virtual..."
source venv/Scripts/activate

echo "Subindo a API..."
uvicorn main:app --reload
```

```bash
chmod +x start.sh
./start.sh
```

`chmod +x` concede permissão de execução — sem isso o sistema trata o
arquivo como texto comum, não como programa executável.

---

### 3.8 Arquitetura Atual do Projeto

```
task_manager/
├── app/
│   ├── routes/
│   │   └── tarefas.py        → GET e POST de tarefas
│   ├── services/              → ainda vazio
│   └── models/
│       ├── tarefa.py          → Schema Pydantic (contrato da API)
│       └── tarefa_db.py       → Modelo ORM SQLAlchemy (tabela real)
├── database/
│   ├── db.py                  → Engine, Session, Base
│   └── task_manager.db        → arquivo do banco SQLite
├── tests/
├── start.sh                   → sobe a API com um comando
├── main.py
├── requirements.txt
├── README.md
└── GUIDE.md
```

**Fluxo planejado de uma requisição (parte ainda não implementada — ver pendência 3.9):**

1. Cliente (Swagger) envia requisição HTTP para `/v1/tarefas/`
2. `routes/tarefas.py` recebe a requisição
3. Dados validados pelo schema `Tarefa` (Pydantic) em `models/tarefa.py`
4. Dependency Injection do FastAPI fornece uma sessão do banco à rota
5. Sessão usa o modelo ORM `TarefaDB` (`models/tarefa_db.py`) para gravar/ler
6. Dados persistidos de fato em `database/task_manager.db`

**Hoje, na prática:** as rotas ainda usam a lista em memória (`tarefas_db = []`)
— a conexão real das rotas ao banco (passos 4-6) é a próxima etapa.

---

### 3.9 Pendência — Próxima Sessão

**Objetivo:** conectar `app/routes/tarefas.py` ao banco real, substituindo
`tarefas_db = []` por uma sessão SQLAlchemy via Dependency Injection do FastAPI.

Conceito a aprofundar: como o FastAPI usa `Depends()` para fornecer e encerrar
automaticamente uma sessão de banco a cada requisição.

---

### Resumo da Sessão 3

| Atividade | Status |
|---|---|
| Conceito Schema vs Modelo ORM esclarecido | ✅ |
| Instalação do SQLAlchemy (versão travada) | ✅ |
| Configuração de Engine, Session, Base | ✅ |
| Criação do modelo ORM TarefaDB | ✅ |
| Criação da tabela no SQLite | ✅ |
| Instalação e uso do DB Browser for SQLite | ✅ |
| Criação do script start.sh | ✅ |
| README atualizado | ✅ |
| Diagrama de arquitetura atualizado | ✅ |
| Conexão das rotas ao banco real (Dependency Injection) | ⏳ pendente |

