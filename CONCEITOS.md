# CONCEITOS — Glossário de Consulta Rápida

Documento de referência pessoal, organizado por tema. Não é cronológico
(isso é papel do `GUIDE.md`) — é para abrir, buscar (`Ctrl+F`), e fechar.

> Este arquivo é de uso pessoal/estudo. Não faz parte da documentação
> "oficial" do projeto (README/ARCHITECTURE) por ora.

---

## 1. Termos parecidos que geram confusão

A tabela mais importante deste documento — volte aqui sempre que se perder
entre `Tarefa`, `tarefa_id`, `tarefa.id`.

| Termo | O que é, exatamente | Exemplo |
|---|---|---|
| `Tarefa` (maiúscula) | O **schema** Pydantic — formato dos dados na API | `def criar_tarefa(tarefa: Tarefa)` |
| `TarefaDB` | O **modelo ORM** — representa a tabela real no banco | `class TarefaDB(Base)` |
| `tarefa.py` | **Arquivo** que contém a classe `Tarefa` | `app/models/tarefa.py` |
| `tarefa_id` | Variável simples (`int`), vem da **URL** | `/v1/tarefas/{tarefa_id}` |
| `tarefa` (minúscula, dentro de uma rota) | **Objeto já buscado no banco**, via `.first()` | `tarefa = db.query(TarefaDB)...first()` |
| `tarefa.id` | **Atributo** `id` de um objeto que já existe | só existe depois do objeto ser buscado/criado |
| `tarefa_atualizada` | Objeto que chega no **corpo** do PUT — dados novos | `def alterar_tarefa(..., tarefa_atualizada: Tarefa)` |

**Regra para nunca mais confundir:** sempre pergunte "o que foi atribuído a
essa variável, algumas linhas atrás?" antes de usar `.algumacoisa` nela.

---

## 2. API e REST

**API** — Application Programming Interface. Um "contrato" que define como
dois sistemas conversam entre si.

**REST** — conjunto de princípios/regras para construir APIs usando HTTP.
Não é uma tecnologia, é um estilo arquitetural. Os 6 princípios: Cliente-
Servidor, Stateless, Cache, Interface Uniforme, Sistema em Camadas, Código
sob Demanda.

**RESTful** — adjetivo para uma API que segue os princípios REST de forma
fiel (todos os 6). Na prática, os termos são usados de forma intercambiável
no mercado.

**Stateless (sem estado)** — cada requisição deve conter tudo que o servidor
precisa para processá-la; o servidor não guarda memória da requisição
anterior. Analogia: pronto-socorro (cada atendimento começa do zero) vs
médico de família (lembra do histórico). É por isso que login usa **token**:
o servidor não guarda "fulano está logado", ele valida o token a cada
requisição.

**Métodos HTTP (verbos):**

| Método | Faz | Exemplo no projeto |
|---|---|---|
| GET | Busca dados | Listar tarefas |
| POST | Cria um registro | Criar tarefa |
| PUT | Atualiza um registro **completo** | Atualizar todos os campos |
| PATCH | Atualiza **parcialmente** | Só mudar o status |
| DELETE | Remove um registro | Apagar tarefa |

**Path vs Rota:** "ação" (verbo HTTP) + "caminho" (path) juntos = **rota**.
Ex: `GET /v1/tarefas/` é uma rota.

**Path Parameter** — parte variável da URL, capturada pela rota.
`/v1/tarefas/{tarefa_id}` → o `{tarefa_id}` precisa ter o mesmo nome do
parâmetro na função Python.

---

## 3. OpenAPI / Swagger

**OpenAPI** — especificação que descreve como documentar APIs REST (formato
JSON/YAML). Gerada automaticamente pelo FastAPI em `/openapi.json`.

**Swagger UI** — interface visual que **lê** o `openapi.json` e desenha a
tela interativa em `/docs`. Antigamente "Swagger" era o nome de toda a
especificação; em 2015 foi renomeada para OpenAPI, mas "Swagger" ainda é
usado para as ferramentas.

---

## 4. Pydantic e Schemas

**Pydantic** — biblioteca que o FastAPI usa para validar e estruturar dados.

**Schema** — definição de como os dados devem se parecer (uma classe que
herda de `BaseModel`).

**Validação estrita de Enum** — o Pydantic compara valor recebido caractere
por caractere com o Enum. `"concluída"` (com acento) é rejeitado se o Enum
só tem `"concluida"`. Evita inconsistência (`"Concluida"`, `"concluído"`,
etc. todos significando a mesma coisa).

**`str | None = None`** — sintaxe moderna (Python 3.10+) para "tipo opcional,
nulo por padrão". Equivalente ao antigo `Optional[str]`.

---

## 5. SQLAlchemy e Banco de Dados

**SQLAlchemy** — ORM (Object-Relational Mapping): traduz objetos Python em
comandos SQL, sem precisar escrever SQL manualmente.

**Engine** — sabe **como conversar** com o banco (tipo, caminho do arquivo).

**Session / SessionLocal** — "fábrica" de sessões; usada no dia a dia para
ler/escrever dados através do Engine.

**Base** — classe-base da qual todo modelo ORM herda; conecta classes Python
a tabelas reais.

**Modelo ORM** (`TarefaDB`) — representa a tabela de fato; existe sempre,
independente de haver requisição.

**Schema vs Modelo ORM — a analogia da casa:**
- Schema (Pydantic) = planta arquitetônica (existe só durante a requisição).
- Modelo ORM (SQLAlchemy) = fundação e estrutura (existe sempre, é a tabela
  persistida).
- Mudar a "pintura" (schema) não exige reforçar a "fundação" (tabela).

**Os dois NÃO se conversam diretamente.** A ponte é o código — hoje, o
**service** — que copia campo a campo:
```python
nova_tarefa = TarefaDB(titulo=tarefa.titulo, descricao=tarefa.descricao, ...)
```

**`db.add()`** — marca um objeto novo como "a ser inserido" (ainda não
grava).

**`db.commit()`** — efetiva a gravação no banco.

**`db.refresh(objeto)`** — busca de volta dados gerados pelo banco (como o
`id` autoincrementado) e atualiza o objeto Python.

**`db.query(Modelo).filter(...).first()`** — monta um SELECT com WHERE,
retorna o primeiro resultado ou `None`.

**`db.delete(objeto)` + `db.commit()`** — remove de fato.

**PUT não usa `db.add()`** — só `db.commit()`, porque o objeto já foi buscado
e já está vinculado à sessão; o SQLAlchemy detecta a mudança nos atributos
automaticamente.

**Consistência entre schema e banco (`nullable`)** — todo campo `nullable=False`
no modelo ORM precisa ter um equivalente obrigatório no schema Pydantic (sem
`| None = None`), e vice-versa. Se o schema permite `None` mas o banco exige
preenchido, a requisição passa pela validação do Pydantic e só falha mais
tarde, no SQLAlchemy, com um erro menos claro. Vale revisar os dois arquivos
lado a lado sempre que um campo for adicionado ou alterado.

---

## 5.1 Camada de Services

**Service** — camada que concentra as regras de negócio (o "o que fazer com
os dados"), separada de quem recebe a requisição (rota) e de quem representa
os dados (models). Existe como função Python comum — **não** usa
`Depends()`, porque isso é mecanismo específico de rota do FastAPI.

**Por que extrair da rota:** sem essa separação, qualquer outra forma de
criar/alterar uma tarefa (ex: um script via linha de comando) precisaria
duplicar a lógica que hoje só existiria dentro da função da rota.

**Divisão de responsabilidade:**

| Camada | Função |
|---|---|
| Rota | Recebe a requisição HTTP, declara o path/método, e **chama** o service |
| Service | Busca, valida, cria, atualiza, remove — a lógica de fato |

**Convenção de nomes usada no projeto** (verbo HTTP na rota, verbo de negócio
no service):

| Rota | Service |
|---|---|
| `listar_tarefas` | `get_tarefas` |
| `criar_tarefa` | `create_tarefa` |
| `deletar_tarefa` | `delete_tarefa` |
| `alterar_tarefa` | `update_tarefa` |
| `atualizar_parcial` | `patch_tarefa` |

**Como a rota chama o service** — passa exatamente os parâmetros que recebeu,
incluindo a sessão do banco já injetada via `Depends(get_db)`:
```python
@router.delete("/{tarefa_id}")
def deletar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    return tarefa_service.delete_tarefa(tarefa_id, db)
```

**Erro comum ao refatorar:** chamar a função do service sem todos os
argumentos que ela espera (ex: `delete_tarefa(db)` em vez de
`delete_tarefa(tarefa_id, db)`). Sempre confira a assinatura (`def` no
arquivo de origem) e conte os parâmetros antes de chamar.

**Pendência de design conhecida:** hoje o service usa `HTTPException`
diretamente (um conceito de protocolo HTTP) — o ideal, a longo prazo, seria o
service levantar uma exceção própria de negócio (ex: `TarefaNaoEncontrada`) e
deixar a rota traduzir isso para o código HTTP. Simplificação aceitável por
ora; planejada para revisão antes do início do front-end.

---

## 6. Dependency Injection (FastAPI)

**Dependency Injection** — o FastAPI entrega automaticamente para a rota algo
que ela precisa (ex: sessão do banco), sem a rota precisar criar isso
manualmente. Abre no início da requisição, fecha no final — mesmo com erro.

```python
def listar_tarefas(db: Session = Depends(get_db)):
```

**`yield` / Generator Functions** — `yield` pausa a função, entrega um valor,
e pode continuar depois. No `get_db()`, o código antes do `yield` roda antes
da rota usar a sessão; o código depois (no `finally`) roda depois que a rota
termina:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**HTTPException + status_code 404** — interrompe a execução e devolve um
erro estruturado. Usado sempre que buscamos algo por id que pode não existir.

---

## 7. Ambiente Python

**venv (ambiente virtual)** — pasta isolada com instalação independente do
Python e bibliotecas, separada do Python do sistema. Evita conflito de
versões entre projetos diferentes.

**`requirements.txt`** — lista de dependências com versões exatas
(`pip freeze > requirements.txt`). Permite recriar o ambiente idêntico em
outra máquina. Regra: refazer o freeze toda vez que instalar/remover algo.

**Versões travadas (`==`)** — sem `^` ou `~`, para não permitir atualizações
automáticas que poderiam quebrar compatibilidade.

**`__init__.py`** — arquivo (geralmente vazio) que diz ao Python "esta pasta
é um pacote", permitindo `from app.models import algo`. Tecnicamente opcional
desde Python 3.3+, mas é boa prática manter.

**Black** — formatador automático de código Python (PEP 8). Se o autoformat
"não funcionar" ao salvar, suspeitar primeiro de erro de sintaxe no arquivo,
não da configuração da extensão.

**Aspas duplas vs simples** — Python aceita as duas; convenção de mercado
(via Black) é usar aspas duplas como padrão.

---

## 8. Arquitetura do Projeto

**Arquitetura em Camadas** — divisão por responsabilidade técnica:

| Camada | Pasta | Função |
|---|---|---|
| Routes | `app/routes/` | Recebe requisições e chama o service (o "porteiro") |
| Services | `app/services/` | Regras de negócio: busca, criação, atualização, remoção (o "cérebro") |
| Models | `app/models/` | Schema (Pydantic) + Modelo ORM (SQLAlchemy) |

**Organização por domínio dentro da camada** — um arquivo por assunto
(`tarefas.py`) dentro de cada pasta técnica, em vez de uma pasta completa por
domínio (como em NestJS/Spring).

**POM (Page Object Model)** — padrão para testes de front-end (Cypress),
separa a interação com a página (seletores) da lógica do teste.

---

## 9. Ferramentas Externas

**DB Browser for SQLite** — ferramenta visual para abrir e inspecionar
arquivos `.db`. Não cria tabelas "oficialmente" para o projeto — só o código
(SQLAlchemy) faz isso; a interface serve para inspecionar e rascunhar.

**Mermaid** — linguagem baseada em texto para diagramas dentro de markdown;
o GitHub renderiza automaticamente. Usado no `ARCHITECTURE.md`.

---

## 10. Git — comandos e lógica usados no projeto

| Comando | Quando usar |
|---|---|
| `git status` | Ver o que mudou antes de decidir o que commitar |
| `git add .` | Adicionar mudanças à área de staging |
| `git commit -m "..."` | Registrar no histórico local |
| `git push origin <branch>` | Enviar para o GitHub |
| `git pull origin main` | Trazer atualizações do `main` para a branch atual |
| `git checkout -b <nome>` | Criar e mudar para uma branch nova |

**`git pull` é necessário ao criar uma branch nova?** Só se o `main` puder
ter recebido mudanças entre a última sincronização local e agora (outra
pessoa, outra máquina, edição direta no GitHub). Se você acabou de
sincronizar, não há nada novo para trazer.

**Quando fazer um commit?** Quando o código representa uma unidade de
trabalho completa e coerente — não em qualquer parada no meio do caminho.
