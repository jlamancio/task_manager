# GUIDE — Diário Técnico do Projeto Task Manager

Este arquivo registra as atividades desenvolvidas em cada sessão do projeto,
servindo como material de referência e estudo.

---

## Sessão 1 — Setup do Ambiente
**Data:** 15/06/2025
**Branch:** feature/setup_do_projeto
**Objetivo:** Configurar o ambiente de desenvolvimento e estruturar o projeto.

*(conteúdo já registrado anteriormente — ver histórico do repositório)*

### Resumo da Sessão 1

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
**Objetivo:** Criar o schema de Tarefa, as primeiras rotas (GET e POST) e conectá-las ao main.py.

---

### 2.1 Modelagem da Tarefa

Antes de codar, definimos os campos da entidade `Tarefa`:

| Campo | Tipo | Obrigatório? | Descrição |
|---|---|---|---|
| `id` | inteiro | Gerado automaticamente | Identificador único |
| `titulo` | texto | Sim | Nome curto da tarefa |
| `descricao` | texto | Não | Detalhes adicionais |
| `status` | enum | Sim, com valor padrão | pendente, em_andamento, concluida |
| `prioridade` | enum | Sim, com valor padrão | baixa, media, alta |
| `data_criacao` | data/hora | Gerado automaticamente | Quando a tarefa foi criada |
| `data_vencimento` | data | Não | Prazo opcional para conclusão |

---

### 2.2 Criação do Schema (Pydantic)

**Conceito: Pydantic e Schemas** — o Pydantic valida e estrutura os dados que
entram e saem da API. Um schema define o formato esperado desses dados.

Arquivo criado: `app/models/tarefa.py`

```python
from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel


class StatusTarefa(str, Enum):
    pendente = "pendente"
    em_andamento = "em_andamento"
    concluida = "concluida"


class PrioridadeTarefa(str, Enum):
    baixa = "baixa"
    media = "media"
    alta = "alta"


class Tarefa(BaseModel):
    id: int
    titulo: str
    descricao: str | None = None
    status: StatusTarefa = StatusTarefa.pendente
    prioridade: PrioridadeTarefa = PrioridadeTarefa.media
    data_criacao: datetime
    data_vencimento: date | None = None
```

**Erro encontrado e corrigido:** as linhas `status: StatusTarefa.pendente` e
`prioridade: PrioridadeTarefa.media` estavam sem o sinal `=`, fazendo o Python
interpretar um valor do Enum como se fosse o próprio tipo. Correção: declarar
o tipo antes do `=` e o valor padrão depois (`status: StatusTarefa = StatusTarefa.pendente`).

**Validação do arquivo (sem rodar o servidor inteiro):**

```bash
python -c 'from app.models.tarefa import Tarefa; print("Schema carregado com sucesso!")'
```

> Nota: usamos aspas simples por fora e duplas por dentro para evitar o erro
> `event not found` do Bash, causado pelo `!` dentro de aspas duplas (history expansion).

---

### 2.3 Criação das Rotas

**Conceito: Router (Roteador) no FastAPI** — agrupa rotas relacionadas em um
arquivo separado, mantendo a organização por camada técnica (routes/services/models)
e por domínio dentro de cada camada (um arquivo por assunto, ex: tarefas.py).

Arquivo criado: `app/routes/tarefas.py`

```python
from datetime import datetime

from fastapi import APIRouter

from app.models.tarefa import Tarefa

router = APIRouter(prefix="/v1/tarefas", tags=["Tarefas"])

tarefas_db: list[Tarefa] = []


@router.get("/")
def listar_tarefas():
    return tarefas_db


@router.post("/")
def criar_tarefa(tarefa: Tarefa):
    tarefa.data_criacao = datetime.now()
    tarefas_db.append(tarefa)
    return tarefa
```

**Importante:** o `prefix` definido no `APIRouter()` já se aplica
automaticamente a todas as rotas declaradas dentro dele. Por isso os decorators
usam apenas `"/"` — usar `@router.post("/v1/tarefas")` aqui causaria duplicação
do caminho (`/v1/tarefas/v1/tarefas`).

> `tarefas_db` é uma lista Python em memória — simula um banco de dados
> temporariamente. Os dados se perdem ao reiniciar o servidor. O SQLite será
> conectado em uma sessão futura.

---

### 2.4 Conectar as Rotas ao main.py

O `main.py` precisa importar e registrar o router para que o FastAPI saiba
que essas rotas existem.

```python
from fastapi import FastAPI

from app.routes import tarefas

app = FastAPI(title="Task Manager API")

app.include_router(tarefas.router)


@app.get("/")
def read_root():
    return {"message": "Task Manager API está no ar!"}
```

**Erro encontrado:** o `main.py` ficou sem essas duas linhas (`from app.routes
import tarefas` e `app.include_router(tarefas.router)`) durante a edição —
por isso só a rota `/` aparecia no Swagger, e as rotas de tarefas pareciam não
existir. Diagnosticado comparando o conteúdo real do `main.py` com o esperado.

---

### 2.5 Rodando e Testando a API

```bash
uvicorn main:app --reload
```

- `uvicorn` → servidor que executa a API
- `main:app` → "no arquivo main.py, use o objeto chamado app"
- `--reload` → reinicia automaticamente ao detectar mudanças no código

Testado via Swagger (`http://127.0.0.1:8000/docs`):
- `GET /v1/tarefas/` → lista as tarefas em memória
- `POST /v1/tarefas/` → cria uma nova tarefa

---

### 2.6 Problemas Resolvidos Nesta Sessão

| Problema | Causa | Solução |
|---|---|---|
| `Import "fastapi" could not be resolved` no VS Code | Pylance usando interpretador Python diferente do venv | `Ctrl+Shift+P` → `Python: Select Interpreter` → apontar para `venv\Scripts\python.exe` |
| `bash: !": event not found` | History expansion do Bash interpretando `!` dentro de aspas duplas | Usar aspas simples por fora, duplas por dentro |
| Rota POST não aparecia corretamente no Swagger | Path duplicado (`@router.post("/v1/tarefas")` dentro de um router que já tem esse prefix) | Usar apenas `"/"` no decorator |
| Apenas a rota `/` aparecia no Swagger | `main.py` sem o `include_router` | Reescrever `main.py` com o import e o `include_router` |
| `PydanticUserError: not fully defined` | Enum usado como tipo sem o `=` (`status: StatusTarefa.pendente` em vez de `status: StatusTarefa = StatusTarefa.pendente`) | Corrigir a sintaxe de tipo + valor padrão |
| Edições feitas pelo terminal não apareciam no arquivo | Conflito entre o conteúdo em disco (escrito pelo terminal) e a versão aberta no VS Code | Fechar a aba antes de sobrescrever via terminal, ou editar direto no editor e salvar com `Ctrl+S` |

---

### 2.7 Arquitetura Atual do Projeto

```
task_manager/
├── app/
│   ├── routes/
│   │   └── tarefas.py     → GET e POST de tarefas (rotas = método HTTP + path)
│   ├── services/          → ainda vazio, sem lógica de negócio implementada
│   ├── models/
│   │   └── tarefa.py      → Enums (StatusTarefa, PrioridadeTarefa) + schema Tarefa
│   └── __init__.py
├── tests/
├── main.py                → ponto de entrada, conecta os routers
├── requirements.txt
├── README.md
└── GUIDE.md
```

**Fluxo atual de uma requisição:**

1. Cliente (Swagger/navegador) envia requisição HTTP para `/v1/tarefas/`
2. `routes/tarefas.py` recebe e processa diretamente (ainda sem passar por `services/`)
3. Os dados são validados pelo schema `Tarefa` em `models/tarefa.py`
4. A resposta é devolvida — armazenamento ainda em lista Python (memória), sem banco de dados real

**Nota de nomenclatura — domínio vs camada:**
Diferente de frameworks que organizam por domínio completo (uma pasta só para
"cadastro", outra para "vendas", cada uma com suas próprias rotas/regras/dados
dentro), aqui organizamos primeiro por **camada técnica** (routes/services/models)
e, dentro de cada camada, por **domínio** (um arquivo por assunto). Quando
surgir um novo domínio (ex: usuários), have um `usuarios.py` em cada uma das
três pastas.

**Nota — Schema (Pydantic) vs Tabela de banco de dados:**
O que existe hoje em `models/tarefa.py` é um schema que define o contrato de
dados da API, não uma tabela de banco real. Quando o SQLite for conectado,
provavelmente teremos dois modelos distintos: um para a API (schema) e outro
para a persistência (tabela) — conceito a ser detalhado na sessão de conexão
com o banco de dados.

---

### Resumo da Sessão 2

| Atividade | Status |
|---|---|
| Modelagem da entidade Tarefa | ✅ |
| Criação do schema Pydantic (tarefa.py) | ✅ |
| Criação das rotas GET e POST (tarefas.py) | ✅ |
| Conexão das rotas ao main.py | ✅ |
| Testes manuais via Swagger | ✅ |
| Resolução de 6 problemas práticos (ver tabela 2.6) | ✅ |
| Revisão conceitual: rotas, schema vs tabela, organização por camada | ✅ |

---

## Sessão 3 — A definir

**Objetivo sugerido:** Conectar o SQLite, criar o modelo de persistência e
implementar a camada de serviços (services/) com a lógica de negócio.